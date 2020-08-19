from django.shortcuts import get_object_or_404,render,redirect,render_to_response
from django.utils import timezone
from howdy.models import Roll_cutting,coating_daily_report,coating_daily_report_two,coating_shift,cutting_daily_report_two,cutting_daily_report,cutting_shift,\
    Manger,Fiber_Code,order_sch,agreements_for_order_sch,Productio_order,Order_item,Customer,\
    Productio_order_test2,cutting_internal_order,coating_internal_order,printing_internal_order,\
    printing_daily_report,printing_daily_report_two,printing_shift,Roll_Coating,Roll_Identifier,Roll_weaving,Roll_printing,\
    waste_breach_cutting,waste_breach_printing,waste_breach_looms,User

from howdy.forms import order_sch_Form,agreements_for_order_sch_form,OrderForm,ItemForm,customerForm,\
    OrderForm_test2,cutting_internal_order_Form,coating_internal_order_Form,printing_internal_order_Form
from django.http import  JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages




@login_required
def production_m_order_update_page(request):
   user = User.objects.get(id=request.user.id)
   if user.position != "Production_manager":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
   orders=Productio_order.objects.filter(production_manager_agreement='لا')
   return render(request, 'Production_manager/new_order.html', {'orders':orders})

@login_required
def production_m_update(request, pk):
       user = User.objects.get(id=request.user.id)
       if user.position != "Production_manager":
           raise Http404('غير مسموج لك بالدخول لهذا الرابط')
       order = get_object_or_404(Productio_order_test2, pk=pk)
       print(request.POST.get('sdate'))
       if request.POST.get('sdate') !='2000-11-11':
           order.start_time = request.POST.get('sdate')
       if request.POST.get('ddate') != '2000-11-11':
           order.delivery_time = request.POST.get('ddate')
       if request.POST.get('dw') != "لا يوجد":
           order.delivery_way = request.POST.get('dw')

       order.production_manager_agreement = request.POST.get('ag')
       print(request.POST.get('ag') )
       order.save()
       messages.success(request, 'تم حفظ التعديلات')
       return redirect('production_m_order_update_page')



@login_required
def order_sch_view(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "Production_manager":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    form = order_sch_Form()
    if request.method=="POST":
        form2=order_sch_Form(request.POST)
        if form2.is_valid():
            if not order_sch.objects.filter(order_id__exact=form2.cleaned_data['order_id']).exists():
                form2.save()
                laste=order_sch.objects.all().last()
                if not agreements_for_order_sch.objects.filter(order_sch_id__exact=laste).exists():
                       agreements_for_order_sch.objects.create(order_sch_id=laste)
                messages.success(request,"تم اضافة خطة جديدة ")
                return redirect('all_order_sch')
            else:
                messages.success(request,"سبق وان قمت بوضع خطة للطلبية المحددة ")
                return redirect('order_sch_view')
    print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
    return render(request,'Production_manager/order_sch_template.html',{'form':form})






@login_required
def update_order_sch_view_manager(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "Production_manager":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    schs=order_sch.objects.filter(fixedd='لا')
    return render(request,'Production_manager/update_order_sch.html',{'schs':schs})

@csrf_exempt
@login_required
def update_order_sch_view_manager_two(request,pk):
    user = User.objects.get(id=request.user.id)
    if user.position != "Production_manager":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    print(request.POST)
    sch=get_object_or_404(order_sch,pk=pk)
    ag=agreements_for_order_sch.objects.get(order_sch_id=sch)
    if request.POST.get('cosi') != "2000-11-11" :
        sch.start_coating_date=request.POST.get('cosi')
    if request.POST.get('coei') != "2000-11-11" :
        sch.end_coating_date=request.POST.get('coei')
    if request.POST.get('csi') != "2000-11-11" :
        sch.start_cutting_date=request.POST.get('csi')
    if request.POST.get('cei') != "2000-11-11" :
        sch.end_cutting_date=request.POST.get('cei')
    if request.POST.get('psi') != "2000-11-11" :
        sch.star_printing_date=request.POST.get('psi')
    if request.POST.get('pei') != "2000-11-11" :
        sch.end_printing_date=request.POST.get('pei')

    if request.POST.get('lsi') != "2000-11-11" :
        sch.start_loom_date=request.POST.get('lsi')
    if request.POST.get('lei') !="2000-11-11" :
        sch.end_loom_date=request.POST.get('lei')

    if request.POST.get('l_fx') != "لا" :
        sch.loom_fixed=request.POST.get('l_fx')
    if request.POST.get('fixed') != 'لا':
        sch.fixedd="نعم"
    print(request.POST.get('fixed'))
    sch.save()
    messages.success(request, 'تم حفظ التعديلات')
    return redirect('update_order_sch_view_manager')


@login_required
def orders_in_p_manager_page(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "Production_manager":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    orders = Productio_order.objects.filter(~Q(order_status="انتهى") & Q(sales_manager_agreement="نعم"))
    return render(request,'Production_manager/orders.html',{'orders':orders})

@login_required
def all_order_sch(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "Production_manager":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    schds=order_sch.objects.filter(~Q(state='انتهى') & Q(fixedd='نعم'))
    return render(request,'Production_manager/all_order_sch.html',{'schds':schds})

@login_required
def update_order_state(request,pk):
    user = User.objects.get(id=request.user.id)
    if user.position != "Production_manager":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    updated_state=request.POST.get('selectionn')
    sch=get_object_or_404(order_sch,pk=pk)
    sch.state=updated_state
    sch.save()
    messages.success(request, 'تم تعديل خالة الخطة')
    return redirect('all_order_sch')

@login_required
def fiber_tables_manager(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "Production_manager":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    fibers=Fiber_Code.objects.all()
    return render(request,'Production_manager/fiber_code_template.html',{'fibers':fibers})

@login_required
def cutting_internal_order_view(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "Production_manager":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    form=cutting_internal_order_Form()
    if request.method == "POST":
        sid = int(request.POST.get('sch_id'))
        try :
            u=cutting_internal_order.objects.get(sch_id=order_sch.objects.get(sch_id=sid),order_id=order_sch.objects.get( sch_id=sid).order_id,item_id=request.POST.get('item_id'))
            messages.success(request,"عذرا يوجد طلب داخلي لهذا البند من الطلبية.. الرجاء قم بتغيير رقم البند او رقم الخطة")
            return render(request, 'Production_manager/cutting_internal_order_template.html', {'form': form})
        except cutting_internal_order.DoesNotExist:
            e = cutting_internal_order.objects.create(sch_id=order_sch.objects.get(sch_id=sid),
                                                      order_id=order_sch.objects.get( sch_id=sid).order_id,
                                                      item_id=request.POST.get('item_id'),
                                                      amount=request.POST.get('amount'),
                                                      notes=request.POST.get('notes'))
            order = Productio_order.objects.get(id=e.order_id.id)
            oo = cutting_internal_order.objects.filter(order_id=order)
            return render(request, 'Production_manager/cutting_internal_order_template.html', {'oo': oo,'form':form})
    return render(request, 'Production_manager/cutting_internal_order_template.html',{'form':form})


@login_required
def coating_internal_order_view(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "Production_manager":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    form=coating_internal_order_Form()
    if request.method == "POST":
        sid=int(request.POST.get('sch_id'))
        try:
            u = coating_internal_order.objects.get(sch_id=order_sch.objects.get(sch_id=sid),
                                                   order_id=order_sch.objects.get(sch_id=sid).order_id,
                                                   item_id=request.POST.get('item_id'))
            messages.success(request,
                             "عذرا يوجد طلب داخلي لهذا البند من الطلبية.. الرجاء قم بتغيير رقم البند او رقم الخطة")
            return render(request, 'Production_manager/caoting_iternal_order_template.html', {'form': form})
        except coating_internal_order.DoesNotExist:
            e=coating_internal_order.objects.create(sch_id=order_sch.objects.get(sch_id=sid),
                                                  order_id=order_sch.objects.get(sch_id=sid).order_id,
                                                  item_id=request.POST.get('item_id'),weight_after=request.POST.get('weight_after'),
                                                  weight_before=request.POST.get('weight_before'),amount=request.POST.get('amount'),
                                                  notes=request.POST.get('notes'),thickness=request.POST.get('thickness'))

            order = Productio_order.objects.get(id=e.order_id.id)
            oo = coating_internal_order.objects.filter(order_id=order)
            return render(request, 'Production_manager/caoting_iternal_order_template.html', { 'oo': oo,'form':form})
    return render(request,'Production_manager/caoting_iternal_order_template.html',{'form':form})

@login_required
def printing_internal_order_view(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "Production_manager":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    form = printing_internal_order_Form()
    if request.method == "POST":
        sid = int(request.POST.get('sch_id'))
        try:
            u = printing_internal_order.objects.get(sch_id=order_sch.objects.get(sch_id=sid),
                                                   order_id=order_sch.objects.get(sch_id=sid).order_id,
                                                   item_id=request.POST.get('item_id'))
            messages.success(request,
                             "عذرا يوجد طلب داخلي لهذا البند من الطلبية.. الرجاء قم بتغيير رقم البند او رقم الخطة")
            return render(request, 'Production_manager/printing_internal_order_template.html', {'form': form})
        except printing_internal_order.DoesNotExist:
            e = printing_internal_order.objects.create(sch_id=order_sch.objects.get(sch_id=sid),
                                                      order_id=order_sch.objects.get( sch_id=sid).order_id,
                                                      item_id=request.POST.get('item_id'),
                                                      amount=request.POST.get('amount'),
                                                      notes=request.POST.get('notes'))

            order = Productio_order.objects.get(id=e.order_id.id)
            oo = printing_internal_order.objects.filter(order_id=order)
            return render(request, 'Production_manager/printing_internal_order_template.html', {'oo': oo,'form':form})
    return render(request, 'Production_manager/printing_internal_order_template.html',{'form':form})

@login_required
def coating_reports(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "Production_manager":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    shift=coating_shift.objects.all().last()
    reports=coating_daily_report.objects.filter(shift_id=shift)
    try:
       rolls=Roll_Coating.objects.get(shift_id=shift)
    except Roll_Coating.DoesNotExist:
        rolls=None
    return render(request,'Production_manager/coating_reports.html',{'reports':reports,'rolls':rolls})
@login_required
def printing_reports(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "Production_manager":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    shift=printing_shift.objects.all().last()
    reports=printing_daily_report.objects.filter(shift_id=shift)
    try:
       rolls=Roll_printing.objects.get(shift_id=shift)
    except Roll_printing.DoesNotExist:
        rolls = None
    return render(request,'Production_manager/printing_reports.html',{'reports':reports,'rolls':rolls})

@login_required
def cutting_reports(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "Production_manager":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    shift=cutting_shift.objects.all().last()
    reports=cutting_daily_report.objects.filter(shift_id=shift)
    try:
       rolls=Roll_cutting.objects.get(shift_id=shift)
    except Roll_cutting.DoesNotExist:
       rolls = None
    return render(request,'Production_manager/cutting_reports.html',{'reports':reports,'rolls':rolls})

@login_required
def order_plan_state_production_m(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "Production_manager":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    plans=order_sch.objects.filter(state="جاري التصنيع")
    return render(request,'Production_manager/planinng_states.html',{'plans':plans})

def loom_waste_reports(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "Production_manager":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    count=waste_breach_looms.objects.all().count()
    if count<=10:
        reports = waste_breach_looms.objects.all()
    else:
        reports = waste_breach_looms.objects.all()[-10:]
    return render(request, 'Production_manager/loom_waste_reports.html', {'reports': reports})

def printing_waste_reports(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "Production_manager":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    count= waste_breach_printing.objects.all().count()
    if count<=10:
        reports= waste_breach_printing.objects.all()
    else:
        reports = waste_breach_printing.objects.all()[-10:]
    return render(request, 'Production_manager/printing_waste_reports.html', {'reports': reports})

def cutting_waste_reports(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "Production_manager":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    count=waste_breach_cutting.objects.all().count()
    if count<=10:
         reports = waste_breach_cutting.objects.all()
    else:
        reports=waste_breach_cutting.objects.all()[-10:]
    return render(request, 'Production_manager/cutting_waste_reports.html', {'reports': reports})


def all_printing_internal_orders(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "Production_manager":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    sch=order_sch.objects.filter(~Q(star_printing_date="2000-11-11") & Q(state="جاري التصنيع"))
    return render(request,'Production_manager/all_printing_internal_order.html',{'sch':sch})

def all_cutting_internal_orders(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "Production_manager":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    sch=order_sch.objects.filter(~Q(start_cutting_date="2000-11-11") & Q(state="جاري التصنيع"))
    return render(request,'Production_manager/all_cutting_internal_order.html',{'sch':sch})

def all_coating_internal_orders(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "Production_manager":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    sch=order_sch.objects.filter(~Q(start_coating_date="2000-11-11") & Q(state="جاري التصنيع"))
    return render(request,'Production_manager/all_cutting_internal_order.html',{'sch':sch})





def orders_p_manager(request,pk):
    order=Productio_order.objects.get(id=pk)
    return render(request,'Production_manager/show_total_order_two.html',{'order':order})















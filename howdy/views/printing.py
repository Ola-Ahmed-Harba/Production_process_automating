from django.shortcuts import get_object_or_404,render,redirect
from django.utils import timezone
from howdy.models import printing_prodution_follow_up_one,printing_daily_report,printing_daily_report_two,Manger,\
    agreements_for_order_sch,order_sch,Productio_order,Order_item,Customer,Productio_order_test2,\
    printing_shift,printing_internal_order,Central_Warehouse_Order_two,Central_Warehouse_Order_one,User
from howdy.forms import printing_daily_report_Form,printing_daily_report_two_Form,agreements_for_order_sch_form,order_sch_Form,OrderForm,ItemForm,customerForm,shift_identifier_printing_Form
from django.http import  JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.contrib import messages
from datetime import datetime


@login_required
def update_order_sch_printing_view(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="printing":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    schs=order_sch.objects.filter(Q(fixedd='لا') & ~Q(star_printing_date='2000-11-11') & Q(loom_fixed='نعم'))
    form =agreements_for_order_sch_form()
    return render(request,'printing/update_order_sch.html',{'schs':schs})

@login_required
def update_order_sch_view_printing_two(request,pk):
    user=User.objects.get(id=request.user.id)
    if user.position!="printing":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    sch=get_object_or_404(order_sch,pk=pk)
    ag=agreements_for_order_sch.objects.get(order_sch_id=sch)
    if request.POST.get('psi') is not "2000-11-11" :
        ag.cots=request.POST.get('psi')
    if request.POST.get('pei') is not "2000-11-11" :
        ag.cote=request.POST.get('pei')
    if request.POST.get('reason') is not "لا يموجد" :
        ag.cot_reason=request.POST.get('reason')
    ag.save()
    messages.success(request, 'تم ارسال التعديلات الى مدير الانتاج')
    return redirect('update_order_sch_printing_view')

@login_required
def daily_orders_printing_page(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="printing":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    orders = Productio_order.objects.filter(~Q(order_status="انتهى") & Q(sales_manager_agreement="نعم"))
    return render(request,'printing/orders.html',{'orders':orders})



@login_required
def internal_printing_order(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="printing":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    oo=printing_internal_order.objects.all()
    return render(request,'printing/internal_order.html',{'oo':oo})

@login_required
def shift_identifier_printing_view(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="printing":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    request.session['roll_id']="no"

    form =shift_identifier_printing_Form()
    shifts=printing_shift.objects.all()
    if request.method=="POST":
        form2=shift_identifier_printing_Form(request.POST)
        if form2.is_valid():
            form2.save()
            ss=printing_shift.objects.all().last()
            shifts=printing_shift.objects.all()
            printing_prodution_follow_up_one.objects.create(shift_id=ss)
            return render(request, 'printing/shift_identifier_template.html', {'form': form, 'shifts': shifts})
    return render(request,'printing/shift_identifier_template.html',{'form': form,'shifts':shifts})


@login_required
def first_printing_report(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="printing":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    form=printing_daily_report_Form()
    form2=printing_daily_report_two_Form()
    if request.method=="POST":
        if 'add_report' in request.POST :
            ff=printing_daily_report_Form(request.POST)
            if ff.is_valid():
                rep=ff.save(commit=False)
                rep.machine_id=1
                rep.shift_id=printing_shift.objects.all().last()
                rep.save()
                return render(request,'printing/first_machine_report.html',{'form2':form2,'rep':rep})
            return render(request, 'printing/first_machine_report.html', {'form': form})
        else:
            rr=printing_daily_report_two_Form(request.POST)
            print(request.POST)
            if rr.is_valid():
                re=rr.save(commit=False)
                re.report_id=printing_daily_report.objects.all().last()
                re.save()
                all_re=printing_daily_report_two.objects.filter(report_id=re.report_id)
                rep=printing_daily_report.objects.all().last()
                return render(request,'printing/first_machine_report.html',{'form2':form2,'rep':rep,'all_re':all_re})
            return render(request, 'printing/first_machine_report.html', {'form': form})

    else:
        return render(request,'printing/first_machine_report.html',{'form':form})


@login_required
def second_printing_report(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="printing":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    form=printing_daily_report_Form()
    form2=printing_daily_report_two_Form()
    if request.method=="POST":
        if 'add_report' in request.POST :
            ff=printing_daily_report_Form(request.POST)
            if ff.is_valid():
                rep=ff.save(commit=False)
                rep.machine_id=2
                rep.shift_id=printing_shift.objects.all().last()
                rep.save()
                return render(request,'printing/second_machine_report.html',{'form2':form2,'rep':rep})
            return render(request, 'printing/second_machine_report.html', {'form': form})
        else:
            rr=printing_daily_report_two_Form(request.POST)
            if rr.is_valid():
                re=rr.save(commit=False)
                re.report_id=printing_daily_report.objects.all().last()
                re.save()
                all_re=printing_daily_report_two.objects.filter(report_id=re.report_id)
                rep=printing_daily_report.objects.all().last()
                return render(request,'printing/second_machine_report.html',{'form2':form2,'rep':rep,'all_re':all_re})
            return render(request, 'printing/second_machine_report.html', {'form': form})

    else:
        return render(request,'printing/second_machine_report.html',{'form':form})

@login_required
def third_printing_report(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="printing":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    form=printing_daily_report_Form()
    form2=printing_daily_report_two_Form()
    if request.method=="POST":
        if 'add_report' in request.POST :
            ff=printing_daily_report_Form(request.POST)
            if ff.is_valid():
                rep=ff.save(commit=False)
                rep.machine_id=3
                rep.shift_id=printing_shift.objects.all().last()
                rep.save()
                return render(request,'printing/third_machine_report.html',{'form2':form2,'rep':rep})
            return render(request, 'printing/third_machine_report.html', {'form': form})
        else:
            rr=printing_daily_report_two_Form(request.POST)
            if rr.is_valid():
                re=rr.save(commit=False)
                re.report_id=printing_daily_report.objects.all().last()
                re.save()
                all_re=printing_daily_report_two.objects.filter(report_id=re.report_id)
                rep=printing_daily_report.objects.all().last()
                return render(request,'printing/third_machine_report.html',{'form2':form2,'rep':rep,'all_re':all_re})
            return render(request, 'printing/third_machine_report.html', {'form': form})

    else:
        return render(request,'printing/third_machine_report.html',{'form':form})

@login_required
def fourth_printing_report(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="printing":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    form=printing_daily_report_Form()
    form2=printing_daily_report_two_Form()
    if request.method=="POST":
        if 'add_report' in request.POST :
            ff=printing_daily_report_Form(request.POST)
            if ff.is_valid():
                rep=ff.save(commit=False)
                rep.machine_id=4
                rep.shift_id=printing_shift.objects.all().last()
                rep.save()
                return render(request,'printing/fourth_machine_report.html',{'form2':form2,'rep':rep})
            return render(request, 'printing/fourth_machine_report.html', {'form': form})
        else:
            rr=printing_daily_report_two_Form(request.POST)
            if rr.is_valid():
                re=rr.save(commit=False)
                re.report_id=printing_daily_report.objects.all().last()
                re.save()
                all_re=printing_daily_report_two.objects.filter(report_id=re.report_id)
                rep=printing_daily_report.objects.all().last()
                return render(request,'printing/fourth_machine_report.html',{'form2':form2,'rep':rep,'all_re':all_re})
            return render(request, 'printing/fourth_machine_report.html', {'form': form})

    else:
        return render(request,'printing/fourth_machine_report.html',{'form':form})
@login_required
def order_plan_state_printing(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="printing":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    plans=order_sch.objects.filter(~Q(start_coating_date="2000-11-11") & ~Q(state="انتهى"))
    return render(request,'printing/planinng_states.html',{'plans':plans})



def central_warehouse_order_printing(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="printing":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    if request.method=="GET":
        return render(request,'printing/central_warehouse_order.html')
    else:
        if 'add_report' in request.POST:
            suid=request.POST.get('suid')
            report=Central_Warehouse_Order_one.objects.create(order_date=datetime.now().date(),department="الطباعة",supervisor_id=suid)
            return render(request,'printing/central_warehouse_order.html',{'report':report})
        else:
            report_id=request.POST.get('report_id')
            matid=request.POST.get('matid')
            unit=request.POST.get('unit')
            amount=request.POST.get('amount')
            machine=request.POST.get('machine')
            material_describtion=request.POST.get('material_describtion')
            report=Central_Warehouse_Order_one.objects.get(report_id=report_id)
            Central_Warehouse_Order_two.objects.create(report_id=report,material_id=matid,unit=unit,machine_id=machine,amount=amount,
                                                  material_describtion=material_describtion)
            report_details=Central_Warehouse_Order_two.objects.filter(report_id=report)
            return render(request, 'printing/central_warehouse_order.html', {'report': report,'report_details':report_details})

def delete_item_from_central_warehouse_order_printing(request,pk):
    user=User.objects.get(id=request.user.id)
    if user.position!="printing":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    item=get_object_or_404(Central_Warehouse_Order_two,pk=pk)
    report=Central_Warehouse_Order_one.objects.get(report_id=item.report_id_id)
    item.delete()
    report_details=Central_Warehouse_Order_two.objects.filter(report_id=report)
    return render(request, 'printing/central_warehouse_order.html', {'report': report,'report_details':report_details})




def orders_printing(request,pk):
    order=Productio_order.objects.get(id=pk)
    return render(request,'printing/show_total_order_two.html',{'order':order})
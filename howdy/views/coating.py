from django.shortcuts import get_object_or_404,render,redirect
from django.http import  JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from datetime import datetime
from howdy.forms import coating_daily_report_Form,coating_daily_report_two_Form,loom_daily_order_production_report_Form,shift_identifier_Form,part_internal_order_between_loomers_Form,\
    loom_internal_order_Form,order_sch_Form,\
    Daily_Extroder_Report_For_Each_Extruder_Form,Daily_Report_For_Each_internal_Order_Form, ItemForm,AddFiberForm,\
    Daily_Fiber_Order_From_Looms_Form,loomers_related_daily_order_of_looms_to_extruder_Form,Lot_Identifier_Form,Roll_coating_Form,Roll_identifier_Form,\
    Roll_printing_Form,Roll_weaving_Form,shift_identifier_coating_Form,shift_identifier_printing_Form,agreements_for_order_sch_form

from howdy.models import coating_production_follow_up_two,coating_prodution_follow_up_one,coating_daily_report_two,coating_daily_report,Manger,loom_daily_order_production_report,shift_identifier,part_internal_order_between_loomers,cutting_internal_order,printing_internal_order,\
    coating_internal_order,loom_internal_order,order_sch,Daily_extruder_waste,Daily_Extroder_Report_For_Each_Extruder,Productio_order,Order_item,Fiber_Code,\
    Roll_Coating,Roll_weaving,Roll_Identifier,coating_shift,printing_shift,agreements_for_order_sch,Raw_Material_Order_one,Raw_Material_Order_two,\
    Central_Warehouse_Order_one,Central_Warehouse_Order_two,User
from .help_functions import getTime
from django.db.models import Q
from django.contrib import messages



@login_required
def update_order_sch_coating_view(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="coating":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    schs=order_sch.objects.filter(Q(fixedd='لا') & ~Q(start_coating_date='2000-11-11'))
    form =agreements_for_order_sch_form()
    return render(request,'coating/update_order_sch.html',{'schs':schs})

@login_required
def update_order_sch_view_coating_two(request,pk):
    user=User.objects.get(id=request.user.id)
    if user.position!="coating":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    sch=get_object_or_404(order_sch,pk=pk)
    ag=agreements_for_order_sch.objects.get(order_sch_id=sch)
    if request.POST.get('cosd') is not "2000-11-11" :
        ag.cots=request.POST.get('csi')
    if request.POST.get('coed') is not "2000-11-11" :
        ag.cote=request.POST.get('cei')
    if request.POST.get('reason') is not "لا يموجد" :
        ag.cot_reason=request.POST.get('reason')
    ag.save()
    messages.success(request, 'تم ارسال التعديلات الى مدير الانتاج')
    return redirect('update_order_sch_coating_view')


@login_required
def daily_orders_coating_page(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="coating":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    orders=Productio_order.objects.all()
    return render(request,'coating/orders.html',{'orders':orders})

@login_required
def daily_coating_reports(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="coating":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    orders = Productio_order.objects.filter(~Q(order_status="انتهى") & Q(sales_manager_agreement="نعم"))
    return render(request,'coating/orders.html',{'orders':orders})


@login_required
def internal_coating_order(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="coating":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    oo=coating_internal_order.objects.all()
    return render(request,'coating/internal_orders.html',{'oo':oo})


@login_required
def shift_identifier_coating_view(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="coating":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    request.session['roll_id']="no"

    form =shift_identifier_coating_Form()
    shifts=coating_shift.objects.all()
    if request.method=="POST":
        form2=shift_identifier_coating_Form(request.POST)
        if form2.is_valid():
            form2.save()
            coating_prodution_follow_up_one.objects.create(shift_id=coating_shift.objects.all().last())
            shifts=coating_shift.objects.all()
            return render(request, 'coating/shift_identifier_template.html', {'form': form, 'shifts': shifts})
    return render(request,'coating/shift_identifier_template.html',{'form': form,'shifts':shifts})



@login_required
def first_coating_report(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="coating":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    form=coating_daily_report_Form()
    form2=coating_daily_report_two_Form()
    if request.method=="POST":
        if 'add_report' in request.POST :
            ff=coating_daily_report_Form(request.POST)
            if ff.is_valid():
                rep=ff.save(commit=False)
                rep.machine_id=1
                rep.shift_id=coating_shift.objects.all().last()
                rep.save()
                return render(request,'coating/first_machine_report.html',{'form2':form2,'rep':rep})
            return render(request, 'coating/first_machine_report.html', {'form': form})
        else:
            rr=coating_daily_report_two_Form(request.POST)
            if rr.is_valid():
                re=rr.save(commit=False)
                re.report_id=coating_daily_report.objects.all().last()
                re.save()
                all_re=coating_daily_report_two.objects.filter(report_id=re.report_id)
                rep=coating_daily_report.objects.all().last()
                return render(request,'coating/first_machine_report.html',{'form2':form2,'rep':rep,'all_re':all_re})
            return render(request, 'coating/first_machine_report.html', {'form': form})

    else:
        return render(request,'coating/first_machine_report.html',{'form':form})

@login_required
def second_coating_report(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="coating":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    form=coating_daily_report_Form()
    form2=coating_daily_report_two_Form()
    if request.method=="POST":
        if 'add_report' in request.POST :
            ff=coating_daily_report_Form(request.POST)
            if ff.is_valid():
                rep=ff.save(commit=False)
                rep.machine_id=2
                rep.shift_id=coating_shift.objects.all().last()
                rep.save()
                return render(request,'coating/first_machine_report.html',{'form2':form2,'rep':rep})
            return render(request, 'coating/first_machine_report.html', {'form': form})
        else:
            rr=coating_daily_report_two_Form(request.POST)
            if rr.is_valid():
                re=rr.save(commit=False)
                re.report_id=coating_daily_report.objects.all().last()
                re.save()
                all_re=coating_daily_report_two.objects.filter(report_id=re.report_id)
                rep=coating_daily_report.objects.all().last()
                return render(request,'coating/first_machine_report.html',{'form2':form2,'rep':rep,'all_re':all_re})
            return render(request, 'coating/first_machine_report.html', {'form': form})

    else:
        return render(request,'coating/first_machine_report.html',{'form':form})


@login_required
def order_plan_state_coating(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="coating":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    plans=order_sch.objects.filter(~Q(start_coating_date="2000-11-11") & ~Q(state="انتهى"))
    return render(request,'coating/planinng_states.html',{'plans':plans})

######################################################################################################################################
def raw_material_order_coating(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="coating":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    if request.method=="GET":
        return render(request,'coating/raw_material_order.html')
    else:
        if 'add_report' in request.POST:
            suid=request.POST.get('suid')
            report=Raw_Material_Order_one.objects.create(order_date=datetime.now().date(),department="الطلي",supervisor_id=suid)
            return render(request,'coating/raw_material_order.html',{'report':report})
        else:
            report_id=request.POST.get('report_id')
            matid=request.POST.get('matid')
            unit=request.POST.get('unit')
            amount=request.POST.get('amount')
            machine=request.POST.get('machine')
            material_describtion=request.POST.get('material_describtion')
            report=Raw_Material_Order_one.objects.get(report_id=report_id)
            Raw_Material_Order_two.objects.create(report_id=report,material_id=matid,unit=unit,machine_id=machine,amount=amount,
                                                  material_describtion=material_describtion)
            report_details=Raw_Material_Order_two.objects.filter(report_id=report)
            return render(request, 'coating/raw_material_order.html', {'report': report,'report_details':report_details})

def delete_item_from_raw_order_coating(request,pk):
    user=User.objects.get(id=request.user.id)
    if user.position!="coating":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    item=get_object_or_404(Raw_Material_Order_two,pk=pk)
    report=Raw_Material_Order_one.objects.get(report_id=item.report_id_id)
    item.delete()
    report_details=Raw_Material_Order_two.objects.filter(report_id=report)
    return render(request, 'coating/raw_material_order.html', {'report': report,'report_details':report_details})



def central_warehouse_order_coating(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="coating":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    if request.method=="GET":
        return render(request,'coating/central_warehouse_order.html')
    else:
        if 'add_report' in request.POST:
            suid=request.POST.get('suid')
            report=Central_Warehouse_Order_one.objects.create(order_date=datetime.now().date(),department="الطلي",supervisor_id=suid)
            return render(request,'coating/central_warehouse_order.html',{'report':report})
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
            return render(request, 'coating/central_warehouse_order.html', {'report': report,'report_details':report_details})

def delete_item_from_central_warehouse_order_coating(request,pk):
    user=User.objects.get(id=request.user.id)
    if user.position!="coating":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    item=get_object_or_404(Central_Warehouse_Order_two,pk=pk)
    report=Central_Warehouse_Order_one.objects.get(report_id=item.report_id_id)
    item.delete()
    report_details=Central_Warehouse_Order_two.objects.filter(report_id=report)
    return render(request, 'coating/central_warehouse_order.html', {'report': report,'report_details':report_details})

def attendance_report_coating(request):
    return render(request,'coating/attendence_report.html')

def orders_coating(request,pk):
    order=Productio_order.objects.get(id=pk)
    return render(request,'coating/show_total_order_two.html',{'order':order})
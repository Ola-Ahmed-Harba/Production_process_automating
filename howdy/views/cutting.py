from django.shortcuts import get_object_or_404,render,redirect
from django.http import  JsonResponse
from howdy.forms import cutting_daily_report_Form,cutting_daily_report_two_Form,agreements_for_order_sch_form,shift_identifier_cutting_Form
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from datetime import datetime

from howdy.models import printing_internal_order,Manger,cutting_shift,cutting_internal_order,\
    cutting_daily_report,cutting_daily_report_two,loom_internal_order,order_sch,Daily_extruder_waste,Daily_Extroder_Report_For_Each_Extruder,\
    Productio_order,agreements_for_order_sch,Raw_Material_Order_two,Raw_Material_Order_one,Central_Warehouse_Order_two,Central_Warehouse_Order_one,User
from .help_functions import getTime
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import os.path
from django.contrib import messages


@login_required
def update_order_sch_cutting_view(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="cutting":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    schs=order_sch.objects.filter(Q(fixedd='لا') & ~Q(start_cutting_date='2000-11-11') & Q(loom_fixed='نعم'))
    form =agreements_for_order_sch_form()
    return render(request,'cutting/update_order_sch.html',{'schs':schs})

@login_required
def update_order_sch_view_cutting_two(request,pk):
    user=User.objects.get(id=request.user.id)
    if user.position!="cutting":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    sch=get_object_or_404(order_sch,pk=pk)
    ag=agreements_for_order_sch.objects.get(order_sch_id=sch)
    if request.POST.get('csi') is not "2000-11-11" :
        ag.cuts=request.POST.get('csi')
    if request.POST.get('cei') is not "2000-11-11" :
        ag.cute=request.POST.get('cei')
    if request.POST.get('reason') is not "لا يموجد" :
        ag.cut_reason=request.POST.get('reason')
    ag.save()
    messages.success(request, 'تم ارسال التعديلات الى مدير الانتاج')
    return redirect('update_order_sch_cutting_view')

@login_required
def daily_orders_cutting_page(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "cutting":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    orders = Productio_order.objects.filter(~Q(order_status="انتهى") & Q(sales_manager_agreement="نعم"))
    return render(request,'cutting/orders.html',{'orders':orders})


@login_required
def daily_cutting_reports(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="cutting":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    orders=Productio_order.objects.all()
    return render(request,'cutting/orders.html',{'orders':orders})


@login_required
def internal_cutting_order(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="cutting":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    oo=cutting_internal_order.objects.all()
    return render(request,'cutting/internal_orders.html',{'oo':oo})



@csrf_exempt
def save_image(request):
    SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
    if request.POST:
        f=open(SITE_ROOT+'/static/ola/ola.jpg','wb')
        f.write(request.raraw_post_data)
        f.close()
        return render(request,'extruder/extruder_home.html')
    else:
        return render(request,'barcode.html')


@login_required
def shift_identifier_cutting_view(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="cutting":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    form =shift_identifier_cutting_Form()
    shifts=cutting_shift.objects.all()
    if request.method=="POST":
        form2=shift_identifier_cutting_Form(request.POST)
        if form2.is_valid():
            form2.save()
            shifts=cutting_shift.objects.all()
            return render(request, 'cutting/shift_identifier_template.html', {'form': form, 'shifts': shifts})
    return render(request,'cutting/shift_identifier_template.html',{'form': form,'shifts':shifts})

@login_required
def first_cutting_report(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="cutting":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    form=cutting_daily_report_Form()
    form2=cutting_daily_report_two_Form()
    if request.method=="POST":
        if 'add_report' in request.POST :
            ff=cutting_daily_report_Form(request.POST)
            if ff.is_valid():
                rep=ff.save(commit=False)
                rep.machine_id=1
                rep.shift_id=cutting_shift.objects.all().last()
                rep.save()
                return render(request,'cutting/first_machine_report.html',{'form2':form2,'rep':rep})
            return render(request, 'cutting/first_machine_report.html', {'form': form})
        else:
            rr=cutting_daily_report_two_Form(request.POST)
            if rr.is_valid():
                re=rr.save(commit=False)
                re.report_id=cutting_daily_report.objects.all().last()
                re.save()
                all_re=cutting_daily_report_two.objects.filter(report_id=re.report_id)
                rep=cutting_daily_report.objects.all().last()
                return render(request,'cutting/first_machine_report.html',{'form2':form2,'rep':rep,'all_re':all_re})
            return render(request, 'cutting/first_machine_report.html', {'form': form})

    else:
        return render(request,'cutting/first_machine_report.html',{'form':form})

@login_required
def second_cutting_report(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="cutting":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    form=cutting_daily_report_Form()
    form2=cutting_daily_report_two_Form()
    if request.method=="POST":
        if 'add_report' in request.POST :
            ff=cutting_daily_report_Form(request.POST)
            if ff.is_valid():
                rep=ff.save(commit=False)
                rep.machine_id=2
                rep.shift_id=cutting_shift.objects.all().last()
                rep.save()
                return render(request,'cutting/second_machine_report.html',{'form2':form2,'rep':rep})
            return render(request, 'cutting/second_machine_report.html', {'form': form})
        else:
            rr=cutting_daily_report_two_Form(request.POST)
            if rr.is_valid():
                re=rr.save(commit=False)
                re.report_id=cutting_daily_report.objects.all().last()
                re.save()
                all_re=cutting_daily_report_two.objects.filter(report_id=re.report_id)
                rep=cutting_daily_report.objects.all().last()
                return render(request,'cutting/second_machine_report.html',{'form2':form2,'rep':rep,'all_re':all_re})
            return render(request, 'cutting/second_machine_report.html', {'form': form})

    else:
        return render(request,'cutting/second_machine_report.html',{'form':form})
@login_required
def third_cutting_report(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="cutting":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    form=cutting_daily_report_Form()
    form2=cutting_daily_report_two_Form()
    if request.method=="POST":
        if 'add_report' in request.POST :
            ff=cutting_daily_report_Form(request.POST)
            if ff.is_valid():
                rep=ff.save(commit=False)
                rep.machine_id=3
                rep.shift_id=cutting_shift.objects.all().last()
                rep.save()
                return render(request,'cutting/second_machine_report.html',{'form2':form2,'rep':rep})
            return render(request, 'cutting/second_machine_report.html', {'form': form})
        else:
            rr=cutting_daily_report_two_Form(request.POST)
            if rr.is_valid():
                re=rr.save(commit=False)
                re.report_id=cutting_daily_report.objects.all().last()
                re.save()
                all_re=cutting_daily_report_two.objects.filter(report_id=re.report_id)
                rep=cutting_daily_report.objects.all().last()
                return render(request,'cutting/second_machine_report.html',{'form2':form2,'rep':rep,'all_re':all_re})
            return render(request, 'cutting/second_machine_report.html', {'form': form})

    else:
        return render(request,'cutting/second_machine_report.html',{'form':form})

@login_required
def fourth_cutting_report(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="cutting":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    form=cutting_daily_report_Form()
    form2=cutting_daily_report_two_Form()
    if request.method=="POST":
        if 'add_report' in request.POST :
            ff=cutting_daily_report_Form(request.POST)
            if ff.is_valid():
                rep=ff.save(commit=False)
                rep.machine_id=4
                rep.shift_id=cutting_shift.objects.all().last()
                rep.save()
                return render(request,'cutting/fourth_machine_report.html',{'form2':form2,'rep':rep})
            return render(request, 'cutting/fourth_machine_report.html', {'form': form})
        else:
            rr=cutting_daily_report_two_Form(request.POST)
            if rr.is_valid():
                re=rr.save(commit=False)
                re.report_id=cutting_daily_report.objects.all().last()
                re.save()
                all_re=cutting_daily_report_two.objects.filter(report_id=re.report_id)
                rep=cutting_daily_report.objects.all().last()
                return render(request,'cutting/fourth_machine_report.html',{'form2':form2,'rep':rep,'all_re':all_re})
            return render(request, 'cutting/fourth_machine_report.html', {'form': form})

    else:
        return render(request,'cutting/fourth_machine_report.html',{'form':form})

@login_required
def fifth_cutting_report(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="cutting":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    form=cutting_daily_report_Form()
    form2=cutting_daily_report_two_Form()
    if request.method=="POST":
        if 'add_report' in request.POST :
            ff=cutting_daily_report_Form(request.POST)
            if ff.is_valid():
                rep=ff.save(commit=False)
                rep.machine_id=5
                rep.shift_id=cutting_shift.objects.all().last()
                rep.save()
                return render(request,'cutting/fifth_machine_report.html',{'form2':form2,'rep':rep})
            return render(request, 'cutting/fifth_machine_report.html', {'form': form})
        else:
            rr=cutting_daily_report_two_Form(request.POST)
            if rr.is_valid():
                re=rr.save(commit=False)
                re.report_id=cutting_daily_report.objects.all().last()
                re.save()
                all_re=cutting_daily_report_two.objects.filter(report_id=re.report_id)
                rep=cutting_daily_report.objects.all().last()
                return render(request,'cutting/fifth_machine_report.html',{'form2':form2,'rep':rep,'all_re':all_re})
            return render(request, 'cutting/fifth_machine_report.html', {'form': form})

    else:
        return render(request,'cutting/fifth_machine_report.html',{'form':form})

@login_required
def sixth_cutting_report(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="cutting":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    form=cutting_daily_report_Form()
    form2=cutting_daily_report_two_Form()
    if request.method=="POST":
        if 'add_report' in request.POST :
            ff=cutting_daily_report_Form(request.POST)
            if ff.is_valid():
                rep=ff.save(commit=False)
                rep.machine_id=6
                rep.shift_id=cutting_shift.objects.all().last()
                rep.save()
                return render(request,'cutting/sixth_machine_report.html',{'form2':form2,'rep':rep})
            return render(request, 'cutting/sixth_machine_report.html', {'form': form})
        else:
            rr=cutting_daily_report_two_Form(request.POST)
            if rr.is_valid():
                re=rr.save(commit=False)
                re.report_id=cutting_daily_report.objects.all().last()
                re.save()
                all_re=cutting_daily_report_two.objects.filter(report_id=re.report_id)
                rep=cutting_daily_report.objects.all().last()
                return render(request,'cutting/sixth_machine_report.html',{'form2':form2,'rep':rep,'all_re':all_re})
            return render(request, 'cutting/sixth_machine_report.html', {'form': form})

    else:
        return render(request,'cutting/sixth_machine_report.html',{'form':form})

@login_required
def seventh_cutting_report(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="cutting":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    form=cutting_daily_report_Form()
    form2=cutting_daily_report_two_Form()
    if request.method=="POST":
        if 'add_report' in request.POST :
            ff=cutting_daily_report_Form(request.POST)
            if ff.is_valid():
                rep=ff.save(commit=False)
                rep.machine_id=7
                rep.shift_id=cutting_shift.objects.all().last()
                rep.save()
                return render(request,'cutting/seventh_machine_report.html',{'form2':form2,'rep':rep})
            return render(request, 'cutting/seventh_machine_report.html', {'form': form})
        else:
            rr=cutting_daily_report_two_Form(request.POST)
            if rr.is_valid():
                re=rr.save(commit=False)
                re.report_id=cutting_daily_report.objects.all().last()
                re.save()
                all_re=cutting_daily_report_two.objects.filter(report_id=re.report_id)
                rep=cutting_daily_report.objects.all().last()
                return render(request,'cutting/seventh_machine_report.html',{'form2':form2,'rep':rep,'all_re':all_re})
            return render(request, 'cutting/seventh_machine_report.html', {'form': form})

    else:
        return render(request,'cutting/seventh_machine_report.html',{'form':form})

@login_required
def eighth_cutting_report(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="cutting":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    form=cutting_daily_report_Form()
    form2=cutting_daily_report_two_Form()
    if request.method=="POST":
        if 'add_report' in request.POST :
            ff=cutting_daily_report_Form(request.POST)
            if ff.is_valid():
                rep=ff.save(commit=False)
                rep.machine_id=8
                rep.shift_id=cutting_shift.objects.all().last()
                rep.save()
                return render(request,'cutting/eighth_machine_report.html',{'form2':form2,'rep':rep})
            return render(request, 'cutting/eighth_machine_report.html', {'form': form})
        else:
            rr=cutting_daily_report_two_Form(request.POST)
            if rr.is_valid():
                re=rr.save(commit=False)
                re.report_id=cutting_daily_report.objects.all().last()
                re.save()
                all_re=cutting_daily_report_two.objects.filter(report_id=re.report_id)
                rep=cutting_daily_report.objects.all().last()
                return render(request,'cutting/eighth_machine_report.html',{'form2':form2,'rep':rep,'all_re':all_re})
            return render(request, 'cutting/eighth_machine_report.html', {'form': form})

    else:
        return render(request,'cutting/eighth_machine_report.html',{'form':form})

@login_required
def order_plan_state_cutting(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="cutting":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    plans=order_sch.objects.filter(~Q(start_cutting_date="2000-11-11") & ~Q(state="انتهى"))
    return render(request,'cutting/planinng_states.html',{'plans':plans})

###############################################################
def raw_material_order_cutting(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="cutting":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    if request.method=="GET":
        return render(request,'cutting/raw_material_order.html')
    else:
        if 'add_report' in request.POST:
            suid=request.POST.get('suid')
            report=Raw_Material_Order_one.objects.create(order_date=datetime.now().date(),department="القص",supervisor_id=suid)
            return render(request,'cutting/raw_material_order.html',{'report':report})
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
            return render(request, 'cutting/raw_material_order.html', {'report': report,'report_details':report_details})

def delete_item_from_raw_order_cutting(request,pk):
    user=User.objects.get(id=request.user.id)
    if user.position!="cutting":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    item=get_object_or_404(Raw_Material_Order_two,pk=pk)
    report=Raw_Material_Order_one.objects.get(report_id=item.report_id_id)
    item.delete()
    report_details=Raw_Material_Order_two.objects.filter(report_id=report)
    return render(request, 'cutting/raw_material_order.html', {'report': report,'report_details':report_details})



def central_warehouse_order_cutting(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="cutting":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    if request.method=="GET":
        return render(request,'cutting/central_warehouse_order.html')
    else:
        if 'add_report' in request.POST:
            suid=request.POST.get('suid')
            report=Central_Warehouse_Order_one.objects.create(order_date=datetime.now().date(),department="القص",supervisor_id=suid)
            return render(request,'cutting/central_warehouse_order.html',{'report':report})
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
            return render(request, 'cutting/central_warehouse_order.html', {'report': report,'report_details':report_details})

def delete_item_from_central_warehouse_order_cutting(request,pk):
    user=User.objects.get(id=request.user.id)
    if user.position!="cutting":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    item=get_object_or_404(Central_Warehouse_Order_two,pk=pk)
    report=Central_Warehouse_Order_one.objects.get(report_id=item.report_id_id)
    item.delete()
    report_details=Central_Warehouse_Order_two.objects.filter(report_id=report)
    return render(request, 'cutting/central_warehouse_order.html', {'report': report,'report_details':report_details})


def orders_cutting(request,pk):
    order=Productio_order.objects.get(id=pk)
    return render(request,'cutting/show_total_order_two.html',{'order':order})

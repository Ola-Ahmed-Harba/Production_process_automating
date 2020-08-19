from datetime import datetime
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.contrib import messages
from django.db.models import Q



from howdy.forms import Daily_Extroder_Report_For_Each_Extruder_Form,Daily_Report_For_Each_internal_Order_Form, ItemForm,AddFiberForm,\
    Daily_Fiber_Order_From_Looms_Form,loomers_related_daily_order_of_looms_to_extruder_Form,Lot_Identifier_Form,Roll_coating_Form,Roll_identifier_Form,shift_identifier_extruder_Form

from howdy.models import Manger,Daily_extruder_waste,Daily_Extroder_Report_For_Each_Extruder,Productio_order,Order_item,Fiber_Code,\
    Daily_Fiber_Order_From_Looms,loomers_related_daily_order_of_looms_to_extruder,Lot_Identifiers,Daily_Report_for_each_internal_Order,Roll_printing,\
    extruder_shift,shift_identifier,Raw_Material_Order_one,Raw_Material_Order_two,Central_Warehouse_Order_two,Central_Warehouse_Order_one,User

from .help_functions import getTime,create_user


def extruderHome(request):
    return render(request,'extruder/extruder_home.html')



@login_required
def add_new_fiber(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="extruder":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    fibers=Fiber_Code.objects.all()
    if request.method=="GET":
        form=AddFiberForm()
        return render(request, 'extruder/add_new_fiber_code.html',{'form':form,'fibers':fibers})
    else:
        form2=AddFiberForm(request.POST)
        if form2.is_valid():
            new_fiber=form2.save()
            new_fiber.save()
            fibers = Fiber_Code.objects.all()
            form=AddFiberForm()
            return render(request, 'extruder/add_new_fiber_code.html',{'form':form,'fibers':fibers})
        else:
            print('invailed')

    return render(request,'extruder/add_new_fiber_code.html')


@login_required
def first_machine(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="extruder":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')

    orders=Daily_Fiber_Order_From_Looms.objects.filter(shift_id=shift_identifier.objects.all().last(),expected_extruder="1400")
    return render(request, 'extruder/machine1.html', {'orders': orders})



@login_required
def second_machine(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="extruder":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    orders=Daily_Fiber_Order_From_Looms.objects.filter(shift_id=shift_identifier.objects.all().last(),expected_extruder="1500/1")
    return render(request, 'extruder/machine2.html', {'orders': orders})



@login_required
def third_machine(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="extruder":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    orders=Daily_Fiber_Order_From_Looms.objects.filter(shift_id=shift_identifier.objects.all().last(),expected_extruder="1500/2")
    return render(request, 'extruder/machine3.html', {'orders': orders})


@login_required
def lots_machine1(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="extruder":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    year, month, day, hour ,sh= getTime()

    orders = Daily_Fiber_Order_From_Looms.objects.filter(order_date__year=year, order_date__month=month,
                                                         order_date__day=day, shift_id=shift_identifier.objects.all().last(), expected_extruder="1400")

    lots = Lot_Identifiers.objects.filter(lot_date__year=year, lot_date__month=month, lot_date__day=day,
                                          extruder_id="1400")
    form = Lot_Identifier_Form(initial={'extruder_id':"1400",'daily_order_id':orders.last() })
    if request.method=="GET":
        return render(request,'extruder/lot_machine1.html',{'form':form,'lots':lots,'orders':orders})
    else:
        form2=Lot_Identifier_Form(request.POST)
        if form2.is_valid():
            lot=form2.save(commit=False)
            lot.lot_date= datetime.now().date()
            form2.save()
            lots = Lot_Identifiers.objects.filter(lot_date__year=year, lot_date__month=month, lot_date__day=day,
                                                  extruder_id="1400")
            form = Lot_Identifier_Form(initial={'extruder_id': "1400", 'daily_order_id': orders[0].daily_order_id})
            messages.success(request,"تم اضافة تبديلة بنجاح")
            return render(request, 'extruder/lot_machine1.html', {'form': form, 'lots': lots,'orders':orders})
        else:
            messages.success(request, "المدخلات غير صحيحة")
            return render(request, 'extruder/lot_machine1.html', {'form': form, 'lots': lots,'orders':orders})


@login_required
def lots_machine2(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="extruder":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    year, month, day, hour ,sh= getTime()

    orders = Daily_Fiber_Order_From_Looms.objects.filter(order_date__year=year, order_date__month=month,
                                                         order_date__day=day, shift_id=shift_identifier.objects.all().last(), expected_extruder="1500/1")

    lots = Lot_Identifiers.objects.filter(lot_date__year=year, lot_date__month=month, lot_date__day=day,
                                          extruder_id="1500/1")
    form = Lot_Identifier_Form(initial={'extruder_id':"1500/1",'daily_order_id':orders.last() })
    if request.method=="GET":
        return render(request,'extruder/lot_machine2.html',{'form':form,'lots':lots,'orders':orders})
    else:
        form2=Lot_Identifier_Form(request.POST)
        if form2.is_valid():
            lot=form2.save(commit=False)
            lot.lot_date= datetime.now().date()
            form2.save()
            lots = Lot_Identifiers.objects.filter(lot_date__year=year, lot_date__month=month, lot_date__day=day,
                                                  extruder_id="1500/1")
            form = Lot_Identifier_Form(initial={'extruder_id': "1500/1", 'daily_order_id': orders[0].daily_order_id})
            return render(request, 'extruder/lot_machine2.html', {'form': form, 'lots': lots,'orders':orders})
        else:
            return render(request, 'extruder/lot_machine2.html', {'form': form, 'lots': lots,'orders':orders})



@login_required
def lots_machine3(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="extruder":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    year, month, day, hour ,sh= getTime()

    orders = Daily_Fiber_Order_From_Looms.objects.filter(order_date__year=year, order_date__month=month,
                                                         order_date__day=day, shift_id=shift_identifier.objects.all().last(), expected_extruder="1500/2")

    lots = Lot_Identifiers.objects.filter(lot_date__year=year, lot_date__month=month, lot_date__day=day,
                                          extruder_id="1500/2")
    form = Lot_Identifier_Form(initial={'extruder_id':"1500/2",'daily_order_id':orders.last() })
    if request.method=="GET":
        return render(request,'extruder/lot_machine3.html',{'form':form,'lots':lots,'orders':orders})
    else:
        form2=Lot_Identifier_Form(request.POST)
        if form2.is_valid():
            lot=form2.save(commit=False)
            lot.lot_date= datetime.now().date()
            form2.save()
            lots = Lot_Identifiers.objects.filter(lot_date__year=year, lot_date__month=month, lot_date__day=day,
                                                  extruder_id="1500/2")
            form = Lot_Identifier_Form(initial={'extruder_id': "1500/2", 'daily_order_id': orders[0].daily_order_id})
            return render(request, 'extruder/lot_machine3.html', {'form': form, 'lots': lots,'orders':orders})
        else:
            return render(request, 'extruder/lot_machine3.html', {'form': form, 'lots': lots,'orders':orders})


@login_required
def daily_reports(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="extruder":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    year, month, day, hour, shift = getTime()
    shift1=extruder_shift.objects.all().last()
    reports = Daily_Extroder_Report_For_Each_Extruder.objects.filter(report_date__year=year, report_date__month=month,
                                                            report_date__day=day,shift_id=shift1)
    form = Daily_Extroder_Report_For_Each_Extruder_Form()
    if request.method=="GET":
          return render(request, 'extruder/daily_reports.html', {'form': form, 'reports': reports})
    else:
        form3 = Daily_Extroder_Report_For_Each_Extruder_Form(request.POST)
        if form3.is_valid():
           ff=form3.save(commit=False)
           ff.shift_id=extruder_shift.objects.all().last()
           ff.total_production_amount=0
           ff.save()
           return render(request, 'extruder/daily_reports.html',
                         { 'reports': reports})
        else:
            print("invalid")
        reports = Daily_Extroder_Report_For_Each_Extruder.objects.filter(report_date__year=year,
                                                                         report_date__month=month,
                                                                         report_date__day=day, shift_id=shift1)
        return render(request, 'extruder/daily_reports.html', {'form': form, 'reports': reports})


@login_required
def shift_identifier_extruder_view(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="extruder":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    form =shift_identifier_extruder_Form()
    shifts=extruder_shift.objects.all()
    if request.method=="POST":
        form2=shift_identifier_extruder_Form(request.POST)
        if form2.is_valid():
            form2.save()
            shifts=extruder_shift.objects.all()
            return render(request, 'extruder/shift_identifier_template.html', {'form': form, 'shifts': shifts})
    return render(request,'extruder/shift_identifier_template.html',{'form': form,'shifts':shifts})


@login_required
def daily_orders(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="extruder":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    if request.method=="POST":
        extruder_id=request.POST.get('exname')
        daily_id=request.POST.get('doi')
        order=Daily_Fiber_Order_From_Looms.objects.get(daily_order_id=daily_id)
        order.expected_extruder=extruder_id
        order.save()
        year, month, day, hour, shift = getTime()
        orders=Daily_Fiber_Order_From_Looms.objects.filter(order_date__year=year,order_date__month=month,order_date__day=day).all()
        messages.success(request, 'تم تعديل رقم الالة')
        return render(request,'extruder/daily_orders_.html',{'orders':orders})
    else:
        year, month, day, hour, shift = getTime()
        orders=Daily_Fiber_Order_From_Looms.objects.filter(order_date__year=year,order_date__month=month,order_date__day=day).all()
        return render(request,'extruder/daily_orders_.html',{'orders':orders})

@login_required
def orders_extruder(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="extruder":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    orders = Productio_order.objects.filter(~Q(order_status="انتهى") & Q(sales_manager_agreement="نعم"))
    return render(request,'extruder/orders.html',{'orders':orders})



def raw_material_order(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="extruder":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    if request.method=="GET":
        return render(request,'extruder/raw_material_order.html')
    else:
        if 'add_report' in request.POST:
            suid=request.POST.get('suid')
            report=Raw_Material_Order_one.objects.create(order_date=datetime.now().date(),department="الخيوط",supervisor_id=suid)
            return render(request,'extruder/raw_material_order.html',{'report':report})
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
            return render(request, 'extruder/raw_material_order.html', {'report': report,'report_details':report_details})

def delete_item_from_raw_order(request,pk):
    user=User.objects.get(id=request.user.id)
    if user.position!="extruder":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    item=get_object_or_404(Raw_Material_Order_two,pk=pk)
    report=Raw_Material_Order_one.objects.get(report_id=item.report_id_id)
    item.delete()
    report_details=Raw_Material_Order_two.objects.filter(report_id=report)
    return render(request, 'extruder/raw_material_order.html', {'report': report,'report_details':report_details})



def central_warehouse_order_extruder(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="extruder":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    if request.method=="GET":
        return render(request,'extruder/central_warehouse_order.html')
    else:
        if 'add_report' in request.POST:
            suid=request.POST.get('suid')
            report=Central_Warehouse_Order_one.objects.create(order_date=datetime.now().date(),department="الخيوط",supervisor_id=suid)
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
            return render(request, 'extruder/central_warehouse_order.html', {'report': report,'report_details':report_details})

def delete_item_from_central_warehouse_order_extruder(request,pk):
    user=User.objects.get(id=request.user.id)
    if user.position!="extruder":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    item=get_object_or_404(Central_Warehouse_Order_two,pk=pk)
    report=Central_Warehouse_Order_one.objects.get(report_id=item.report_id_id)
    item.delete()
    report_details=Central_Warehouse_Order_two.objects.filter(report_id=report)
    return render(request, 'extruder/central_warehouse_order.html', {'report': report,'report_details':report_details})

def orders_extruder_show(request,pk):
    order=Productio_order.objects.get(id=pk)
    return render(request,'extruder/show_total_order_two.html',{'order':order})

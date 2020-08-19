from howdy.forms import waste_breach_looms_Form,waste_breach_cutting_Form,waste_breach_printing_Form
from howdy.models import Manger,waste_breach_looms,First_Group,shift_identifier,Second_Group,Third_Group,waste_breach_cutting,\
    cutting_shift,waste_breach_printing,printing_shift,order_sch,Productio_order,extruder_shift,Daily_extruder_waste,User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import get_object_or_404,render,redirect,reverse
from django.http import JsonResponse, Http404
from django.db.models import Q

@login_required
def loom_waste_view(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "quality":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    form = waste_breach_looms_Form()
    if request.method=="POST":
        form2=waste_breach_looms_Form(request.POST)
        print("222222222222222222222222222222222222222222")
        if form2.is_valid():
            print("1111111111111111111111111111111111111")
            temp=form2.save(commit=False)
            loom_id=form2.cleaned_data['loom_id']
            group_id = form2.cleaned_data['group_id']
            temp.loom_shift=shift_identifier.objects.all().last()
            temp.sending_time=timezone.localtime().time()

            temp.recived_time=None
            temp.quality_monitor=request.user.username
            if group_id=="أولى":
                loom=First_Group.objects.filter(loom_id=loom_id).last()
                temp.order_id=loom.order_id
                temp.item_id=loom.item_id
                temp.loomer_id =loom.worker_id
                temp.save()
            if group_id=="ثانية":
                loom=Second_Group.objects.filter(loom_id=loom_id).last()
                temp.order_id=loom.order_id
                temp.item_id=loom.item_id
                temp.loomer_id = loom.worker_id
                temp.save()
            if group_id=="ثالثة":
                loom=Third_Group.objects.filter(loom_id=loom_id).last()
                temp.order_id=loom.order_id
                temp.item_id=loom.item_id
                temp.loomer_id = loom.worker_id
                temp.save()
        reports=waste_breach_looms.objects.all()
        return render(request,'quality/loom_waste.html',{'form':form,'reports':reports})
    else:
        reports = waste_breach_looms.objects.all()
        return render(request,'quality/loom_waste.html',{'form':form,'reports':reports})

@login_required
def printing_waste_view(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "quality":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    form = waste_breach_printing_Form()
    if request.method=="POST":
        form2=waste_breach_printing_Form(request.POST)
        print("222222222222222222222222222222222222222222")
        if form2.is_valid():
            print("1111111111111111111111111111111111111")
            temp=form2.save(commit=False)
            temp.printing_shift=printing_shift.objects.all().last()
            temp.sending_time=timezone.localtime().time()
            temp.recived_time=None
            temp.quality_monitor=request.user.username
            temp.save()
        reports=waste_breach_printing.objects.all()
        return render(request,'quality/printing_waste.html',{'form':form,'reports':reports})
    else:
        reports = waste_breach_printing.objects.all()
        return render(request,'quality/printing_waste.html',{'form':form,'reports':reports})

@login_required
def cutting_waste_view(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "quality":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    form = waste_breach_cutting_Form()
    if request.method=="POST":
        form2=waste_breach_cutting_Form(request.POST)
        print("222222222222222222222222222222222222222222")
        if form2.is_valid():
            print("1111111111111111111111111111111111111")
            temp=form2.save(commit=False)
            temp.cutting_shift=cutting_shift.objects.all().last()
            temp.sending_time=timezone.localtime().time()
            temp.recived_time=None
            temp.quality_monitor=request.user.username
            temp.save()
        reports=waste_breach_cutting.objects.all()
        return render(request,'quality/cutting_waste.html',{'form':form,'reports':reports})
    else:
        reports = waste_breach_printing.objects.all()
        return render(request,'quality/cutting_waste.html',{'form':form,'reports':reports})

@login_required
def order_plan_state_quality(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "quality":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    plans=order_sch.objects.filter(state="جاري التصنيع")
    return render(request,'quality/planing_states.html',{'plans':plans})


@login_required
def orders_quality(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "quality":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    orders = Productio_order.objects.filter(~Q(order_status="انتهى") & Q(sales_manager_agreement="نعم"))
    return render(request,'quality/orders.html',{'orders':orders})

@login_required
def extruder_waste(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "quality":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    if request.method=="GET":
        return render(request,'quality/extruder_waste.html')
    else:
        extruder_id=request.POST.get('extruder_id')
        extruder_sh=request.POST.get('ext_sh')
        individual_waste = request.POST.get('individual_waste')
        stop_waste = request.POST.get('stop_waste')
        container_waste = request.POST.get('container_waste')
        pull_waste = request.POST.get('pull_waste')
        change_waste = request.POST.get('change_waste')
        electic_broken_waste = request.POST.get('electic_broken_waste')
        electic_broken_waste_reson = request.POST.get('electic_broken_waste_reson')
        ele_repair_order_id = request.POST.get('ele_repair_order_id')
        mecha_broken_waste = request.POST.get('mecha_broken_waste')
        mechabroken_waste_reson = request.POST.get('mechabroken_waste_reson')
        mecha_repair_order_id = request.POST.get('mecha_repair_order_id')
        ww = Daily_extruder_waste.objects.create(extruder_shift_id=extruder_sh, individual_waste=individual_waste,
                                                 stop_waste=stop_waste, container_waste=container_waste,
                                                 pull_waste=pull_waste, change_waste=change_waste,
                                                 electic_broken_waste=electic_broken_waste,
                                                 electic_broken_waste_reson=electic_broken_waste_reson,
                                                 ele_repair_order_id=ele_repair_order_id,
                                                 mecha_broken_waste=mecha_broken_waste,
                                                 mechabroken_waste_reson=mechabroken_waste_reson,
                                                 mecha_repair_order_id=mecha_repair_order_id,
                                                 extruder_id=extruder_id)

        reports=Daily_extruder_waste.objects.filter(extruder_shift_id=extruder_sh)

        return render(request,'quality/extruder_waste.html',{'reports':reports})

def orders_quality_show(request,pk):
    order=Productio_order.objects.get(id=pk)
    return render(request,'quality/show_total_order_two.html',{'order':order})

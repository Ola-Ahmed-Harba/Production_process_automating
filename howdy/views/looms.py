from datetime import datetime
from django.shortcuts import get_object_or_404,render,redirect
from django.http import  JsonResponse
from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404

from howdy.forms import loom_internal_order_Form,loom_daily_order_production_report_Form,shift_identifier_Form,part_internal_order_between_loomers_Form,\
    Daily_Fiber_Order_From_Looms_Form,loomers_related_daily_order_of_looms_to_extruder_Form,Lot_Identifier_Form,Roll_coating_Form,Roll_identifier_Form,\
    Roll_printing_Form,Roll_weaving_Form,shift_identifier_coating_Form,shift_identifier_printing_Form,agreements_for_order_sch_form

from howdy.models import Manger,Third_Group,Second_Group,First_Group,extruder_shift,loom_daily_order_production_report,shift_identifier,part_internal_order_between_loomers,cutting_internal_order,printing_internal_order,\
    coating_internal_order,loom_internal_order,order_sch,Daily_extruder_waste,Daily_Extroder_Report_For_Each_Extruder,Productio_order,Order_item,Fiber_Code,\
    Daily_Fiber_Order_From_Looms,loomers_related_daily_order_of_looms_to_extruder,Lot_Identifiers,Daily_Report_for_each_internal_Order,Roll_printing,\
    agreements_for_order_sch,order_follow_up,weaving_prodution_follow_up,weaving_prodution_follow_up_one,Raw_Material_Order_one,Raw_Material_Order_two,\
    Central_Warehouse_Order_one,Central_Warehouse_Order_two,User
from .help_functions import getTime
from django.db.models import Q
from django.contrib import messages



@login_required
def update_order_sch_view(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="looms":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    schs=order_sch.objects.filter(fixedd='لا' )
    form =agreements_for_order_sch_form()
    return render(request,'looms/update_order_sch.html',{'schs':schs})

@login_required
def update_order_sch_view_two(request,pk):
    user=User.objects.get(id=request.user.id)
    if user.position!="looms":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    sch=get_object_or_404(order_sch,pk=pk)
    ag=agreements_for_order_sch.objects.get(order_sch_id=sch)
    if request.POST.get('lsi') != "2000-11-11" :
        ag.ls=request.POST.get('lsi')
    if request.POST.get('lei') != "2000-11-11" :
        ag.le=request.POST.get('lei')
    if request.POST.get('reason') is not "لا يموجد" :
        ag.l_reason=request.POST.get('reason')
    ag.save()
    messages.success(request,'تم ارسال التعديلات الى مدير الانتاج')
    return redirect('update_order_sch_view')



@login_required
def add_daily_order_from_looms_to_extruder(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="looms":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    reports=Daily_Fiber_Order_From_Looms.objects.all()

    form=Daily_Fiber_Order_From_Looms_Form()
    form.order_date=datetime.now().date()

    if request.method=="GET":
        return render(request, 'looms/daily_order_for_extruders.html', {'form': form,'reports':reports})
    else:
        oo=Daily_Fiber_Order_From_Looms.objects.create(expected_extruder=request.POST.get('expected_extruder'),makok_fiber_code=request.POST.get('makok_fiber_code'),num_kanar_lots=0,num_makok_lots=0,
                                                       num_sdh_lots=0,sdh_fiber_code=request.POST.get('sdh_fiber_code'),
                                                       kanar_fiber_code=request.POST.get('kanar_fiber_code'),order_id=Productio_order.objects.get(id=request.POST.get('order_id')),item_id=request.POST.get('item_id'),
                                                       shift_id=shift_identifier.objects.all().last(),order_date=datetime.now())


        repo=Daily_Report_for_each_internal_Order.objects.create(makok_production_amount=0, sebah_production_amount=0,
                                             kanar_production_amount=0, total_production_amount=0,shift_id=extruder_shift.objects.all().last(),
                                             daily_order_id=oo)

        reports = Daily_Fiber_Order_From_Looms.objects.all()
        form = Daily_Fiber_Order_From_Looms_Form()
        return render(request, 'looms/daily_order_for_extruders.html', {'form': form,'reports': reports})


#       return render(request,'looms/daily_order_for_extruders.html',{'form' :form})


@login_required
def add_names(request,pk):
    user=User.objects.get(id=request.user.id)
    if user.position!="looms":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    order=Daily_Fiber_Order_From_Looms.objects.get(pk=pk)
    form=loomers_related_daily_order_of_looms_to_extruder_Form()
    if request.method=="GET":
        names = loomers_related_daily_order_of_looms_to_extruder.objects.filter(order_id=order)
        return  render(request,'looms/add_names.html',{'order':order,'form':form,'names':names})
    else:
        form2=loomers_related_daily_order_of_looms_to_extruder_Form(request.POST)
        name=form2.save(commit=False)
        name.order_id=order
        name.save()
        order.num_kanar_lots=order.num_kanar_lots+form2.cleaned_data['kanar_lots_num']
        order.num_sdh_lots=order.num_sdh_lots+form2.cleaned_data['sebh_lots_num']
        order.num_makok_lots=order.num_makok_lots+form2.cleaned_data['mkok_lots_num']
        order.save()
        names=loomers_related_daily_order_of_looms_to_extruder.objects.filter(order_id=order)
        form=loomers_related_daily_order_of_looms_to_extruder_Form()
        return render(request,'looms/add_names.html',{'order':order,'form':form,'names':names})



##############################################################################################################


@login_required
def part_internal_order_between_loomers_view(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="looms":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    form =part_internal_order_between_loomers_Form()
    if request.method=="POST":
        form2=part_internal_order_between_loomers_Form(request.POST)
        if form2.is_valid():
            form2.save()
            inite_id2 = form2.cleaned_data['inte_id']
            parts = part_internal_order_between_loomers.objects.filter(inte_id=inite_id2.inte_id)
            return render(request, 'looms/part_internal_order_between_loomers_template.html',
                          {'form': form, 'parts': parts})
        return render(request, 'looms/part_internal_order_between_loomers_template.html', {'form': form})
"""
            if ii.group_id=='أولى':
                First_Group.objects.create(loom_id=ii.loom_id,parting_id=ii,current_produced_amount=0.0,reast_amount=0.0,
                                           shift_id=shift_identifier.objects.all().last(),state='يعمل')
            if ii.group_id == 'ثانية':
                Second_Group.objects.create(loom_id=ii.loom_id,parting_id=ii,current_produced_amount=0.0,reast_amount=0.0,
                                           shift_id=shift_identifier.objects.all().last(),state='يعمل')
            if ii.group_id == 'ثالثة':
                Third_Group.objects.create(loom_id=ii.loom_id,parting_id=ii,current_produced_amount=0.0,reast_amount=0.0,
                                           shift_id=shift_identifier.objects.all().last(),state='يعمل')

"""




@login_required
def loom_internal_order_view(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="looms":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    form=loom_internal_order_Form()
    oo=loom_internal_order.objects.all()
    print(oo)
    if request.method=="POST":
        form2=loom_internal_order_Form(request.POST)
        if form2.is_valid():
            e=form2.save(commit=False)
            e.order_id=order_sch.objects.get(sch_id=form2.cleaned_data['sch_id'].sch_id).order_id
            e.save()
            order=Productio_order.objects.get(id=e.order_id.id)
            oo=loom_internal_order.objects.filter(order_id=order)
            return render(request, 'looms/loom_internal_order_template.html',{'form':form,'oo':oo})
    print("ppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp")
    return render(request,'looms/loom_internal_order_template.html',{'form':form,'oo':oo})




@login_required
def shift_identifier_view(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="looms":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    request.session['roll_id']="no"
    form =shift_identifier_Form()
    shifts=shift_identifier.objects.all()
    if request.method=="POST":
        form2=shift_identifier_Form(request.POST)
        if form2.is_valid():
            form2.save()
            shifts=shift_identifier.objects.all()
            ss=shift_identifier.objects.all().last()
            rr=weaving_prodution_follow_up.objects.create(shift_id=ss)
            weaving_prodution_follow_up_one.objects.create(report_idd=rr,group_id="أولى")
            weaving_prodution_follow_up_one.objects.create(report_idd=rr, group_id="ثانية")
            weaving_prodution_follow_up_one.objects.create(report_idd=rr, group_id="ثالثة")
            return render(request, 'looms/shift_identifier_template.html', {'form': form, 'shifts': shifts})
    return render(request,'looms/shift_identifier_template.html',{'form': form,'shifts':shifts})



@login_required
def orders_in_loom_page_view(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="looms":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    orders = Productio_order.objects.filter(~Q(order_status="انتهى") & Q(sales_manager_agreement="نعم"))
    return render(request,'looms/orders.html',{'orders':orders})

@login_required
def parting_reports_view(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="looms":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    parts=part_internal_order_between_loomers.objects.all()
    return  render(request,'looms/parting_reports_template.html',{'parts':parts})

@login_required
def fiber_tables_looms(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="looms":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    fibers=Fiber_Code.objects.all()
    return render(request,'looms/fiber_code_template.html',{'fibers':fibers})

@login_required
def all_order_sch_in_looms(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="looms":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    schds=order_sch.objects.filter(Q(fixedd="نعم") & ~Q(state="انتهى"))
    return render(request,'looms/all_order_sch.html',{'schds':schds})


def show_first_group(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="looms":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    info=First_Group.objects.all()[:5]
    return render(request,'looms/show_first_group.html',{'info':info})


@login_required
def follow_up_first_group(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="looms":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    if request.method == "POST":
        loom_num = request.POST.get('loom')
        amount = request.POST.get('amot')
        order = Productio_order.objects.get(id=int(request.POST.get('order')))
        item = request.POST.get('item')
        worker = request.POST.get('worker')
        state = request.POST.get('stat')
        thick = request.POST.get('thick')
        loom = First_Group.objects.filter(loom_id=loom_num).last()
        if state==  "لا يعمل":
            First_Group.objects.create(loom_id=loom_num,order_id=None,item_id=0,current_produced_amount=0,reast_amount=0,
                                       worker_id=None,shift_id=shift_identifier.objects.all().last(),state=state,thickness=0)
        else:
            First_Group.objects.create(loom_id=loom_num,order_id=order,item_id=item,worker_id=worker,current_produced_amount=amount,reast_amount=0,
                                       shift_id=shift_identifier.objects.all().last(),state=state,thickness=thick)

    one = First_Group.objects.filter(loom_id=1).last()
    one2 = First_Group.objects.filter(loom_id=2).last()
    one3 = First_Group.objects.filter(loom_id=3).last()
    one4 = First_Group.objects.filter(loom_id=4).last()
    one5 = First_Group.objects.filter(loom_id=5).last()
    one6 = First_Group.objects.filter(loom_id=6).last()
    one7 = First_Group.objects.filter(loom_id=7).last()
    one8 = First_Group.objects.filter(loom_id=8).last()
    one9 = First_Group.objects.filter(loom_id=9).last()
    one10 = First_Group.objects.filter(loom_id=10).last()
    one11 = First_Group.objects.filter(loom_id=11).last()
    one12 = First_Group.objects.filter(loom_id=12).last()
    one13 = First_Group.objects.filter(loom_id=13).last()
    one14 = First_Group.objects.filter(loom_id=14).last()
    one15 = First_Group.objects.filter(loom_id=15).last()
    one16 = First_Group.objects.filter(loom_id=16).last()
    one17 = First_Group.objects.filter(loom_id=17).last()
    one18 = First_Group.objects.filter(loom_id=18).last()
    one19 = First_Group.objects.filter(loom_id=19).last()
    one20 = First_Group.objects.filter(loom_id=20).last()
    one21 = First_Group.objects.filter(loom_id=21).last()
    one22 = First_Group.objects.filter(loom_id=22).last()
    one23 = First_Group.objects.filter(loom_id=23).last()
    one24 = First_Group.objects.filter(loom_id=24).last()
    one25 = First_Group.objects.filter(loom_id=25).last()
    one26 = First_Group.objects.filter(loom_id=26).last()
    one27 = First_Group.objects.filter(loom_id=27).last()
    one28 = First_Group.objects.filter(loom_id=28).last()
    one29 = First_Group.objects.filter(loom_id=29).last()
    one30 = First_Group.objects.filter(loom_id=30).last()
    one31 = First_Group.objects.filter(loom_id=31).last()
    one32 = First_Group.objects.filter(loom_id=32).last()
    one33 = First_Group.objects.filter(loom_id=33).last()
    one34 = First_Group.objects.filter(loom_id=34).last()
    one35 = First_Group.objects.filter(loom_id=35).last()
    one36 = First_Group.objects.filter(loom_id=36).last()
    one37 = First_Group.objects.filter(loom_id=37).last()
    one38 = First_Group.objects.filter(loom_id=38).last()
    one39 = First_Group.objects.filter(loom_id=39).last()
    one40 = First_Group.objects.filter(loom_id=40).last()
    one41 = First_Group.objects.filter(loom_id=41).last()
    one42 = First_Group.objects.filter(loom_id=42).last()
    one43 = First_Group.objects.filter(loom_id=43).last()

    return render(request, 'looms/first_group.html',
                  {'one': one, 'one2': one2, 'one3': one3, 'one4': one4, 'one5': one5,
                   'one6': one6, 'one7': one7, 'one8': one8, 'one9': one9, 'one10': one10,
                   'one11': one11, 'one12': one12, 'one13': one13, 'one14': one14, 'one15': one15,
                   'one16': one16, 'one17': one17, 'one18': one18, 'one19': one19, 'one20': one20,
                   'one21': one21, 'one22': one22, 'one23': one23, 'one24': one24, 'one25': one25,
                   'one26': one26, 'one27': one27, 'one28': one28, 'one29': one29, 'one30': one30,
                   'one31': one31, 'one32': one32, 'one33': one33, 'one34': one34, 'one35': one35,
                   'one36': one36, 'one37': one37, 'one38': one38, 'one39': one39, 'one40': one40,
                   'one41': one41, 'one42': one42, 'one43': one43,})


@login_required
def follow_up_second_group(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="looms":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    if request.method == "POST":
        loom_num = request.POST.get('loom')
        amount = request.POST.get('amot')
        order = Productio_order.objects.get(id=int(request.POST.get('order')))
        item = request.POST.get('item')
        worker = request.POST.get('worker')
        state = request.POST.get('stat')
        thick = request.POST.get('thick')
        loom = Second_Group.objects.filter(loom_id=loom_num).last()
        if state==  "لا يعمل":
            Second_Group.objects.create(loom_id=loom_num,order_id=None,item_id=0,current_produced_amount=0,reast_amount=0,
                                       worker_id=None,shift_id=shift_identifier.objects.all().last(),state=state,thickness=0)
        else:
            Second_Group.objects.create(loom_id=loom_num,order_id=order,item_id=item,worker_id=worker,current_produced_amount=amount,reast_amount=0,
                                       shift_id=shift_identifier.objects.all().last(),state=state,thickness=thick)

    one = Second_Group.objects.filter(loom_id=1).last()
    one2 = Second_Group.objects.filter(loom_id=2).last()
    one3 = Second_Group.objects.filter(loom_id=3).last()
    one4 = Second_Group.objects.filter(loom_id=4).last()
    one5 = Second_Group.objects.filter(loom_id=5).last()
    one6 = Second_Group.objects.filter(loom_id=6).last()
    one7 = Second_Group.objects.filter(loom_id=7).last()
    one8 = Second_Group.objects.filter(loom_id=8).last()
    one9 = Second_Group.objects.filter(loom_id=9).last()
    one10 = Second_Group.objects.filter(loom_id=10).last()
    one11 = Second_Group.objects.filter(loom_id=11).last()
    one12 = Second_Group.objects.filter(loom_id=12).last()
    one13 = Second_Group.objects.filter(loom_id=13).last()
    one14 = Second_Group.objects.filter(loom_id=14).last()
    one15 = Second_Group.objects.filter(loom_id=15).last()
    one16 = Second_Group.objects.filter(loom_id=16).last()
    one17 = Second_Group.objects.filter(loom_id=17).last()
    one18 = Second_Group.objects.filter(loom_id=18).last()
    one19 = Second_Group.objects.filter(loom_id=19).last()
    one20 = Second_Group.objects.filter(loom_id=20).last()
    one21 = Second_Group.objects.filter(loom_id=21).last()
    one22 = Second_Group.objects.filter(loom_id=22).last()
    one23 = Second_Group.objects.filter(loom_id=23).last()
    one24 = Second_Group.objects.filter(loom_id=24).last()
    one25 = Second_Group.objects.filter(loom_id=25).last()
    one26 = Second_Group.objects.filter(loom_id=26).last()
    one27 = Second_Group.objects.filter(loom_id=27).last()
    one28 = Second_Group.objects.filter(loom_id=28).last()
    one29 = Second_Group.objects.filter(loom_id=29).last()
    one30 = Second_Group.objects.filter(loom_id=30).last()
    one31 = Second_Group.objects.filter(loom_id=31).last()
    one32 = Second_Group.objects.filter(loom_id=32).last()
    one33 = Second_Group.objects.filter(loom_id=33).last()
    one34 = Second_Group.objects.filter(loom_id=34).last()
    one35 = Second_Group.objects.filter(loom_id=35).last()
    one36 = Second_Group.objects.filter(loom_id=36).last()
    one37 = Second_Group.objects.filter(loom_id=37).last()
    one38 = Second_Group.objects.filter(loom_id=38).last()
    one39 = Second_Group.objects.filter(loom_id=39).last()
    one40 = Second_Group.objects.filter(loom_id=40).last()
    one41 = Second_Group.objects.filter(loom_id=41).last()
    one42 = Second_Group.objects.filter(loom_id=42).last()
    one43 = Second_Group.objects.filter(loom_id=43).last()

    return render(request, 'looms/second_group.html',
                  {'one': one, 'one2': one2, 'one3': one3, 'one4': one4, 'one5': one5,
                   'one6': one6, 'one7': one7, 'one8': one8, 'one9': one9, 'one10': one10,
                   'one11': one11, 'one12': one12, 'one13': one13, 'one14': one14, 'one15': one15,
                   'one16': one16, 'one17': one17, 'one18': one18, 'one19': one19, 'one20': one20,
                   'one21': one21, 'one22': one22, 'one23': one23, 'one24': one24, 'one25': one25,
                   'one26': one26, 'one27': one27, 'one28': one28, 'one29': one29, 'one30': one30,
                   'one31': one31, 'one32': one32, 'one33': one33, 'one34': one34, 'one35': one35,
                   'one36': one36, 'one37': one37, 'one38': one38, 'one39': one39, 'one40': one40,
                   'one41': one41, 'one42': one42, 'one43': one43,})




@login_required
def follow_up_third_group(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="looms":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    if request.method == "POST":
        loom_num = request.POST.get('loom')
        amount = request.POST.get('amot')
        order = Productio_order.objects.get(id=int(request.POST.get('order')))
        item = request.POST.get('item')
        worker = request.POST.get('worker')
        state = request.POST.get('stat')
        loom = Third_Group.objects.filter(loom_id=loom_num).last()
        thick = request.POST.get('thick')
        if state==  "لا يعمل":
            Third_Group.objects.create(loom_id=loom_num,order_id=None,item_id=0,current_produced_amount=0,reast_amount=0,
                                       worker_id=None,shift_id=shift_identifier.objects.all().last(),state=state,thickness=0)
        else:
            Third_Group.objects.create(loom_id=loom_num,order_id=order,item_id=item,worker_id=worker,current_produced_amount=amount,reast_amount=0,
                                       shift_id=shift_identifier.objects.all().last(),state=state,thickness=thick)

    one = Third_Group.objects.filter(loom_id=1).last()
    one2 = Third_Group.objects.filter(loom_id=2).last()
    one3 = Third_Group.objects.filter(loom_id=3).last()
    one4 = Third_Group.objects.filter(loom_id=4).last()
    one5 = Third_Group.objects.filter(loom_id=5).last()
    one6 = Third_Group.objects.filter(loom_id=6).last()
    one7 = Third_Group.objects.filter(loom_id=7).last()
    one8 = Third_Group.objects.filter(loom_id=8).last()
    one9 = Third_Group.objects.filter(loom_id=9).last()
    one10 = Third_Group.objects.filter(loom_id=10).last()
    one11 = Third_Group.objects.filter(loom_id=11).last()
    one12 = Third_Group.objects.filter(loom_id=12).last()
    one13 = Third_Group.objects.filter(loom_id=13).last()
    one14 = Third_Group.objects.filter(loom_id=14).last()
    one15 = Third_Group.objects.filter(loom_id=15).last()
    one16 = Third_Group.objects.filter(loom_id=16).last()
    one17 = Third_Group.objects.filter(loom_id=17).last()
    one18 = Third_Group.objects.filter(loom_id=18).last()
    one19 = Third_Group.objects.filter(loom_id=19).last()
    one20 = Third_Group.objects.filter(loom_id=20).last()
    one21 = Third_Group.objects.filter(loom_id=21).last()
    one22 = Third_Group.objects.filter(loom_id=22).last()
    one23 = Third_Group.objects.filter(loom_id=23).last()
    one24 = Third_Group.objects.filter(loom_id=24).last()
    one25 = Third_Group.objects.filter(loom_id=25).last()
    one26 = Third_Group.objects.filter(loom_id=26).last()
    one27 = Third_Group.objects.filter(loom_id=27).last()
    one28 = Third_Group.objects.filter(loom_id=28).last()
    one29 = Third_Group.objects.filter(loom_id=29).last()
    one30 = Third_Group.objects.filter(loom_id=30).last()
    one31 = Third_Group.objects.filter(loom_id=31).last()
    one32 = Third_Group.objects.filter(loom_id=32).last()
    one33 = Third_Group.objects.filter(loom_id=33).last()
    one34 = Third_Group.objects.filter(loom_id=34).last()
    one35 = Third_Group.objects.filter(loom_id=35).last()
    one36 = Third_Group.objects.filter(loom_id=36).last()
    one37 = Third_Group.objects.filter(loom_id=37).last()
    one38 = Third_Group.objects.filter(loom_id=38).last()
    one39 = Third_Group.objects.filter(loom_id=39).last()
    one40 = Third_Group.objects.filter(loom_id=40).last()
    one41 = Third_Group.objects.filter(loom_id=41).last()
    one42 = Third_Group.objects.filter(loom_id=42).last()
    one43 = Third_Group.objects.filter(loom_id=43).last()

    return render(request, 'looms/third_group.html',
                  {'one': one, 'one2': one2, 'one3': one3, 'one4': one4, 'one5': one5,
                   'one6': one6, 'one7': one7, 'one8': one8, 'one9': one9, 'one10': one10,
                   'one11': one11, 'one12': one12, 'one13': one13, 'one14': one14, 'one15': one15,
                   'one16': one16, 'one17': one17, 'one18': one18, 'one19': one19, 'one20': one20,
                   'one21': one21, 'one22': one22, 'one23': one23, 'one24': one24, 'one25': one25,
                   'one26': one26, 'one27': one27, 'one28': one28, 'one29': one29, 'one30': one30,
                   'one31': one31, 'one32': one32, 'one33': one33, 'one34': one34, 'one35': one35,
                   'one36': one36, 'one37': one37, 'one38': one38, 'one39': one39, 'one40': one40,
                   'one41': one41, 'one42': one42, 'one43': one43,})












"""
@login_required
def OrdersFollowUp(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="looms":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    orders=order_sch.objects.filter(state='جاري التصنيع')
    if orders:
        for order_sc in orders:
           order=Productio_order.objects.get(id=order_sc.order_id.id)
           for i in Order_item.objects.filter(order_id=order):
                vals=First_Group.objects.filter(order_id=order,item_id=i.item_id).values('loom_id').distinct()
                amount_produced = 0
                if vals:
                    for v in vals:
                        ll=First_Group.objects.filter(loom_id=v['loom_id']).last()
                        amount_produced+=ll.current_produced_amount
                    try:
                       test=order_follow_up.objects.get(order_id=order,item_id=i.item_id)
                       test.produced_amount+=amount_produced
                       test.save()
                    except order_follow_up.DoesNotExist:
                        order_follow_up.objects.create(order_id=order,item_id=i.item_id,produced_amount=amount_produced,state=order_sc.state)


                vals2=Second_Group.objects.filter(order_id=order,item_id=i.item_id).values('loom_id').distinct()
                amount_produced2 = 0
                if vals2:
                    for v in vals2:
                        ll = Second_Group.objects.filter(loom_id=v['loom_id']).last()
                        amount_produced2 += ll.current_produced_amount
                    try:
                        test2 = order_follow_up.objects.get(order_id=order, item_id=i.item_id)
                        test2.produced_amount += amount_produced2
                        test2.save()
                    except order_follow_up.DoesNotExist:
                        order_follow_up.objects.create(order_id=order, item_id=i.item_id,
                                                       produced_amount=amount_produced,state=order_sc.state)

                vals3 = Third_Group.objects.filter(order_id=order, item_id=i.item_id).values('loom_id').distinct()
                amount_produced3 = 0
                if vals3:
                    for v in vals3:
                        ll = Third_Group.objects.filter(loom_id=v['loom_id']).last()
                        amount_produced3 += ll.current_produced_amount
                    try:
                        test3 = order_follow_up.objects.get(order_id=order, item_id=i.item_id)
                        test3.produced_amount += amount_produced3
                        test3.save()
                    except order_follow_up.DoesNotExist:
                        order_follow_up.objects.create(order_id=order, item_id=i.item_id,
                                                       produced_amount=amount_produced, state=order_sc.state)

    orders_follows=order_follow_up.objects.filter(~Q(state='انتهى'))
    return render(request,'looms/order_follow_up_template.html',{'orders_follows':orders_follows})
"""




@login_required
def OrdersFollowUp(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="looms":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    orders=order_sch.objects.filter(state='جاري التصنيع')
    if orders:
        for order_sc in orders:
           order=Productio_order.objects.get(id=order_sc.order_id.id)
           for i in Order_item.objects.filter(order_id=order):
                sum_temp1 = 0
                vals=First_Group.objects.filter(order_id=order,item_id=i.item_id).values('loom_id').distinct()#looms num which works for this item
                print(vals)
                if vals:
                    for v in vals:
                        print(v)
                        ll=First_Group.objects.filter(loom_id=v['loom_id'])
                        temp1=0
                        for l in ll:
                            if l.current_produced_amount>=temp1:
                                temp1=l.current_produced_amount
                            else:
                                temp1+=l.current_produced_amount
                        sum_temp1+=temp1
                sum_temp2 = 0
                vals2=Second_Group.objects.filter(order_id=order,item_id=i.item_id).values('loom_id').distinct()
                if vals2:
                    for v in vals2:
                        ll2 = Second_Group.objects.filter(loom_id=v['loom_id'])
                        temp2=0
                        for l in ll2:
                            if l.current_produced_amount>=temp2:
                                temp2=l.current_produced_amount
                            else:
                                temp2+=l.current_produced_amount
                        sum_temp2+=temp2
                sum_temp3 = 0
                vals3 = Third_Group.objects.filter(order_id=order, item_id=i.item_id).values('loom_id').distinct()
                if vals3:
                    for v in vals3:
                        ll3 = Third_Group.objects.filter(loom_id=v['loom_id'])
                        temp3=0
                        for l in ll3:
                            if l.current_produced_amount >= temp3:
                                temp3 = l.current_produced_amount
                            else:
                                temp3 += l.current_produced_amount
                        sum_temp3+=temp3
                try:
                    test = order_follow_up.objects.get(order_id=order, item_id=i.item_id)
                    test.produced_amount = sum_temp1+sum_temp2+sum_temp3
                    test.save()
                except order_follow_up.DoesNotExist:
                    order_follow_up.objects.create(order_id=order, item_id=i.item_id,
                                                   produced_amount=sum_temp1+sum_temp2+sum_temp3, state=order_sc.state)



    orders_follows=order_follow_up.objects.filter(~Q(state='انتهى'))
    return render(request,'looms/order_follow_up_template.html',{'orders_follows':orders_follows})







@login_required
def all_internal_order_description(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="looms":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    oo=Productio_order.objects.filter(~Q(order_status='انتهى'))
    return render(request,'looms/all_internal_orders.html',{'oo' : oo})

@login_required
def all_internal_order_to_extruder(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="looms":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    return render(request,'looms/all_internal_order_to_extruder.html')

@login_required
def order_plan_state_looms(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="looms":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    plans=order_sch.objects.filter(state="جاري التصنيع")
    return render(request,'looms/planing_states.html',{'plans':plans})



################################################################################################################################
def central_warehouse_order_looms(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="looms":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    if request.method=="GET":
        return render(request,'looms/central_warehouse_order.html')
    else:
        if 'add_report' in request.POST:
            suid=request.POST.get('suid')
            report=Central_Warehouse_Order_one.objects.create(order_date=datetime.now().date(),department="الانوال",supervisor_id=suid)
            return render(request,'looms/central_warehouse_order.html',{'report':report})
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
            return render(request, 'looms/central_warehouse_order.html', {'report': report,'report_details':report_details})

def delete_item_from_central_warehouse_order_looms(request,pk):
    user=User.objects.get(id=request.user.id)
    if user.position!="looms":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    item=get_object_or_404(Central_Warehouse_Order_two,pk=pk)
    report=Central_Warehouse_Order_one.objects.get(report_id=item.report_id_id)
    item.delete()
    report_details=Central_Warehouse_Order_two.objects.filter(report_id=report)
    return render(request, 'looms/central_warehouse_order.html', {'report': report,'report_details':report_details})



def orders_looms(request,pk):
    order=Productio_order.objects.get(id=pk)
    return render(request,'looms/show_total_order_two.html',{'order':order})



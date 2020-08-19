from django.shortcuts import get_object_or_404,render,redirect
from django.utils import timezone
from howdy.models import coating_shift,cutting_shift,printing_prodution_follow_up_one,printing_prodution_follow_up_two,printing_daily_report,printing_daily_report_two,\
    Manger,agreements_for_order_sch,order_sch,Productio_order,Order_item,Customer,Productio_order_test2,\
    printing_shift,printing_internal_order,cutting_production_follow_up_two,cutting_prodution_follow_up_one,\
    coating_prodution_follow_up_one,coating_production_follow_up_two,weaving_prodution_follow_up_one,weaving_prodution_follow_up,weaving_production_follow_up_two,\
    shift_identifier,User
from howdy.forms import printing_daily_report_Form,printing_daily_report_two_Form,agreements_for_order_sch_form,order_sch_Form,\
    OrderForm,ItemForm,customerForm,shift_identifier_printing_Form
from django.http import  JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.contrib import messages

def printing1(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="follower":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    count=printing_prodution_follow_up_one.objects.all().count()
    if request.method=="POST":
        wid = request.POST.get('worker_id')
        print(wid)
        mtrs = request.POST.get('meters')
        print(mtrs)
        mach_state = request.POST.get('machine_state')
        print(mach_state)
        if 'first_shift' in request.POST:
            if printing_shift.objects.all().last().shift_date!=timezone.localdate():
                messages.success(request,'عذرا لم يتم اضافة وردية اليوم ..يمكنك اضافة تقريرك بعد اضافة وردية اليوم')
                return redirect('printing1')
            rep1=printing_prodution_follow_up_one.objects.get(report_id=count-2)
            try:
                ss=printing_prodution_follow_up_two.objects.get(report_id=rep1,machine_id=1)
                messages.success(request, 'عذرا تم اضافة تقرير انتاج لهذه الالة في الوردية المحددة')
                return redirect('printing1')
            except printing_prodution_follow_up_two.DoesNotExist:
                if mach_state == "متوقف":
                    first = printing_prodution_follow_up_two.objects.create(machine_id=1, worker_id="لا احد",
                                                                             machine_state=mach_state, report_id=rep1,
                                                                             meters=0)
                else:
                    first = printing_prodution_follow_up_two.objects.create(machine_id=1, worker_id=wid,
                                                                             machine_state=mach_state,
                                                                             report_id=rep1, meters=mtrs)
                return render(request,'production_follow_up/printing1.html' ,{'first':first})
        else:
            if printing_shift.objects.all().last().shift_date!=timezone.localdate():
                messages.success(request,'عذرا لم يتم اضافة وردية اليوم ..يمكنك اضافة تقريرك بعد اضافة وردية اليوم')
                return redirect('printing1')
            rep2=printing_prodution_follow_up_one.objects.get(report_id=count-1)
            try:
                ss=printing_prodution_follow_up_two.objects.get(report_id=rep2,machine_id=1)
                messages.success(request, 'عذرا تم اضافة تقرير انتاج لهذه الالة في الوردية المحددة')
                return redirect('printing1')
            except printing_prodution_follow_up_two.DoesNotExist:
                if mach_state=="متوقف":
                    second = printing_prodution_follow_up_two.objects.create(machine_id=1, worker_id="لا احد",
                                                                             machine_state=mach_state, report_id=rep2,
                                                                             meters=0)
                else:
                    second=printing_prodution_follow_up_two.objects.create(machine_id=1,worker_id=wid,machine_state=mach_state,
                                                                           report_id=rep2,meters=mtrs)
                return render(request,'production_follow_up/printing1.html' ,{'second':second})
    else:
     return render(request,'production_follow_up/printing1.html')

def printing2(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="follower":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    count=printing_prodution_follow_up_one.objects.all().count()
    if request.method=="POST":
        wid = request.POST.get('worker_id')
        mtrs = request.POST.get('meters')
        mach_state = request.POST.get('machine_state')
        if 'first_shift' in request.POST:
            if printing_shift.objects.all().last().shift_date!=timezone.localdate():
                messages.success(request,'عذرا لم يتم اضافة وردية اليوم ..يمكنك اضافة تقريرك بعد اضافة وردية اليوم')
                return redirect('printing2')
            rep1=printing_prodution_follow_up_one.objects.get(report_id=count-2)
            try:
                ss=printing_prodution_follow_up_two.objects.get(report_id=rep1,machine_id=2)
                messages.success(request, 'عذرا تم اضافة تقرير انتاج لهذه الالة في الوردية المحددة')
                return redirect('printing2')
            except printing_prodution_follow_up_two.DoesNotExist:
                if mach_state == "متوقف":
                    first = printing_prodution_follow_up_two.objects.create(machine_id=2, worker_id="لا احد",
                                                                             machine_state=mach_state, report_id=rep1,
                                                                             meters=0)
                else:
                    first = printing_prodution_follow_up_two.objects.create(machine_id=2, worker_id=wid,
                                                                             machine_state=mach_state,
                                                                             report_id=rep1, meters=mtrs)
                return render(request,'production_follow_up/printing2.html' ,{'first':first})
        else:
            if printing_shift.objects.all().last().shift_date!=timezone.localdate():
                messages.success(request,'عذرا لم يتم اضافة وردية اليوم ..يمكنك اضافة تقريرك بعد اضافة وردية اليوم')
                return redirect('printing2')
            rep2=printing_prodution_follow_up_one.objects.get(report_id=count-1)
            try:
                ss=printing_prodution_follow_up_two.objects.get(report_id=rep2,machine_id=2)
                messages.success(request, 'عذرا تم اضافة تقرير انتاج لهذه الالة في الوردية المحددة')
                return redirect('printing2')
            except printing_prodution_follow_up_two.DoesNotExist:
                if mach_state=="متوقف":
                    second = printing_prodution_follow_up_two.objects.create(machine_id=2, worker_id="لا احد",
                                                                             machine_state=mach_state, report_id=rep2,
                                                                             meters=0)
                else:
                    second=printing_prodution_follow_up_two.objects.create(machine_id=2,worker_id=wid,machine_state=mach_state,
                                                                           report_id=rep2,meters=mtrs)
                return render(request,'production_follow_up/printing2.html' ,{'second':second})
    else:
     return render(request,'production_follow_up/printing2.html')


def printing3(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="follower":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    count = printing_prodution_follow_up_one.objects.all().count()
    if request.method == "POST":
        wid = request.POST.get('worker_id')
        mtrs = request.POST.get('meters')
        mach_state = request.POST.get('machine_state')
        if 'first_shift' in request.POST:
            if printing_shift.objects.all().last().shift_date != timezone.localdate():
                messages.success(request, 'عذرا لم يتم اضافة وردية اليوم ..يمكنك اضافة تقريرك بعد اضافة وردية اليوم')
                return redirect('printing3')
            rep1 = printing_prodution_follow_up_one.objects.get(report_id=count - 2)
            try:
                ss = printing_prodution_follow_up_two.objects.get(report_id=rep1, machine_id=3)
                messages.success(request, 'عذرا تم اضافة تقرير انتاج لهذه الالة في الوردية المحددة')
                return redirect('printing3')
            except printing_prodution_follow_up_two.DoesNotExist:
                if mach_state == "متوقف":
                    first = printing_prodution_follow_up_two.objects.create(machine_id=3, worker_id="لا احد",
                                                                            machine_state=mach_state, report_id=rep1,
                                                                            meters=0)
                else:
                    first = printing_prodution_follow_up_two.objects.create(machine_id=3, worker_id=wid,
                                                                            machine_state=mach_state,
                                                                            report_id=rep1, meters=mtrs)
                return render(request, 'production_follow_up/printing3.html', {'first': first})
        else:
            if printing_shift.objects.all().last().shift_date != timezone.localdate():
                messages.success(request, 'عذرا لم يتم اضافة وردية اليوم ..يمكنك اضافة تقريرك بعد اضافة وردية اليوم')
                return redirect('printing3')
            rep2 = printing_prodution_follow_up_one.objects.get(report_id=count - 1)
            try:
                ss = printing_prodution_follow_up_two.objects.get(report_id=rep2, machine_id=3)
                messages.success(request, 'عذرا تم اضافة تقرير انتاج لهذه الالة في الوردية المحددة')
                return redirect('printing3')
            except printing_prodution_follow_up_two.DoesNotExist:
                if mach_state == "متوقف":
                    second = printing_prodution_follow_up_two.objects.create(machine_id=3, worker_id="لا احد",
                                                                             machine_state=mach_state, report_id=rep2,
                                                                             meters=0)
                else:
                    second = printing_prodution_follow_up_two.objects.create(machine_id=3, worker_id=wid,
                                                                             machine_state=mach_state,
                                                                             report_id=rep2, meters=mtrs)
                return render(request, 'production_follow_up/printing3.html', {'second': second})
    else:
        return render(request, 'production_follow_up/printing3.html')


def printing4(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="follower":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    count = printing_prodution_follow_up_one.objects.all().count()
    if request.method == "POST":
        wid = request.POST.get('worker_id')
        mtrs = request.POST.get('meters')
        mach_state = request.POST.get('machine_state')
        if 'first_shift' in request.POST:
            if printing_shift.objects.all().last().shift_date != timezone.localdate():
                messages.success(request, 'عذرا لم يتم اضافة وردية اليوم ..يمكنك اضافة تقريرك بعد اضافة وردية اليوم')
                return redirect('printing4')
            rep1 = printing_prodution_follow_up_one.objects.get(report_id=count - 2)
            try:
                ss = printing_prodution_follow_up_two.objects.get(report_id=rep1, machine_id=4)
                messages.success(request, 'عذرا تم اضافة تقرير انتاج لهذه الالة في الوردية المحددة')
                return redirect('printing4')
            except printing_prodution_follow_up_two.DoesNotExist:
                if mach_state == "متوقف":
                    first = printing_prodution_follow_up_two.objects.create(machine_id=4, worker_id="لا احد",
                                                                            machine_state=mach_state, report_id=rep1,
                                                                            meters=0)
                else:
                    first = printing_prodution_follow_up_two.objects.create(machine_id=4, worker_id=wid,
                                                                            machine_state=mach_state,
                                                                            report_id=rep1, meters=mtrs)
                return render(request, 'production_follow_up/printing4.html', {'first': first})
        else:
            if printing_shift.objects.all().last().date != timezone.localdate():
                messages.success(request, 'عذرا لم يتم اضافة وردية اليوم ..يمكنك اضافة تقريرك بعد اضافة وردية اليوم')
                return redirect('printing4')
            rep2 = printing_prodution_follow_up_one.objects.get(report_id=count - 1)
            try:
                ss = printing_prodution_follow_up_two.objects.get(report_id=rep2, machine_id=4)
                messages.success(request, 'عذرا تم اضافة تقرير انتاج لهذه الالة في الوردية المحددة')
                return redirect('printing4')
            except printing_prodution_follow_up_two.DoesNotExist:
                if mach_state == "متوقف":
                    second = printing_prodution_follow_up_two.objects.create(machine_id=4, worker_id="لا احد",
                                                                             machine_state=mach_state, report_id=rep2,
                                                                             meters=0)
                else:
                    second = printing_prodution_follow_up_two.objects.create(machine_id=4, worker_id=wid,
                                                                             machine_state=mach_state,
                                                                             report_id=rep2, meters=mtrs)
                return render(request, 'production_follow_up/printing4.html', {'second': second})
    else:
        return render(request, 'production_follow_up/printing4.html')



def cutting1(request,pk):
    user=User.objects.get(id=request.user.id)
    if user.position!="follower":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    count = cutting_prodution_follow_up_one.objects.all().count()
    if request.method == "POST":
        mid=request.POST.get('machine_id')
        wid = request.POST.get('worker_id')
        assid = request.POST.get('assicent_id')
        pks = request.POST.get('pockets')
        mach_state = request.POST.get('machine_state')
        if 'first_shift' in request.POST:
            if cutting_shift.objects.all().last().shift_date != timezone.localdate():
                messages.success(request, 'عذرا لم يتم اضافة وردية اليوم ..يمكنك اضافة تقريرك بعد اضافة وردية اليوم')
                return redirect('cutting{}'.format(mid),mid)
            rep1 = cutting_prodution_follow_up_one.objects.get(report_id=count - 2)
            try:
                ss = cutting_production_follow_up_two.objects.get(report_id=rep1, machine_id=mid)
                messages.success(request, 'عذرا تم اضافة تقرير انتاج لهذه الالة في الوردية المحددة')
                return redirect('cutting{}'.format(mid),mid)
            except cutting_production_follow_up_two.DoesNotExist:
                if mach_state == "متوقف":
                    first = cutting_production_follow_up_two.objects.create(machine_id=mid, worker_id="لا احد",
                                                                            machine_state=mach_state, report_id=rep1,
                                                                            pockets=0,assicent_id="لا احد")
                else:
                    first = cutting_production_follow_up_two.objects.create(machine_id=mid, worker_id=wid,
                                                                            machine_state=mach_state,
                                                                            report_id=rep1, pockets=pks,assicent_id=assid)
                return render(request, 'production_follow_up/cutting{}.html'.format(mid), {'first': first})
        else:
            if cutting_shift.objects.all().last().shift_date != timezone.localdate():
                messages.success(request, 'عذرا لم يتم اضافة وردية اليوم ..يمكنك اضافة تقريرك بعد اضافة وردية اليوم')
                return redirect('cutting{}'.format(mid),mid)
            rep2 = cutting_prodution_follow_up_one.objects.get(report_id=count - 1)
            try:
                ss = cutting_production_follow_up_two.objects.get(report_id=rep2, machine_id=mid)
                messages.success(request, 'عذرا تم اضافة تقرير انتاج لهذه الالة في الوردية المحددة')
                return redirect('cutting{}'.format(mid),mid)
            except cutting_production_follow_up_two.DoesNotExist:
                if mach_state == "متوقف":
                    second = cutting_production_follow_up_two.objects.create(machine_id=mid, worker_id="لا احد",
                                                                            machine_state=mach_state, report_id=rep2,
                                                                            pockets=0,assicent_id="لا احد")
                else:
                    second = cutting_production_follow_up_two.objects.create(machine_id=mid, worker_id=wid,
                                                                            machine_state=mach_state,
                                                                            report_id=rep2, pockets=pks,assicent_id=assid)
                return render(request,'production_follow_up/cutting{}.html'.format(mid), {'second': second})
    else:
        print(timezone.localdate())
        print(type(pk))
        if pk== "1":
           return render(request, 'production_follow_up/cutting1.html')
        if pk == "2":
            return render(request, 'production_follow_up/cutting2.html')
        if pk== "3":
           return render(request, 'production_follow_up/cutting3.html')
        if pk== "4":
           return render(request, 'production_follow_up/cutting4.html')
        if pk== "5":
           return render(request, 'production_follow_up/cutting5.html')
        if pk== "6":
           return render(request, 'production_follow_up/cutting6.html')
        if pk== "7":
           return render(request, 'production_follow_up/cutting7.html')
        else:
           return render(request, 'production_follow_up/cutting8.html')


def coating1(request,pk):
    user=User.objects.get(id=request.user.id)
    if user.position!="follower":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    count = coating_prodution_follow_up_one.objects.all().count()
    if request.method == "POST":
        mid=request.POST.get('machine_id')
        wid = request.POST.get('worker_id')
        pks = request.POST.get('pockets')
        mach_state = request.POST.get('machine_state')
        if 'first_shift' in request.POST:
            if coating_shift.objects.all().last().shift_date != timezone.localdate():
                messages.success(request, 'عذرا لم يتم اضافة وردية اليوم ..يمكنك اضافة تقريرك بعد اضافة وردية اليوم')
                return redirect('coating{}'.format(mid),mid)
            rep1 = coating_prodution_follow_up_one.objects.get(report_id=count - 2)
            try:
                ss = coating_production_follow_up_two.objects.get(report_id=rep1, machine_id=mid)
                messages.success(request, 'عذرا تم اضافة تقرير انتاج لهذه الالة في الوردية المحددة')
                return redirect('coating{}'.format(mid),mid)
            except coating_production_follow_up_two.DoesNotExist:
                if mach_state == "متوقف":
                    first = coating_production_follow_up_two.objects.create(machine_id=mid, worker_id="لا احد",
                                                                            machine_state=mach_state, report_id=rep1,
                                                                            pockets=0)
                else:
                    first = coating_production_follow_up_two.objects.create(machine_id=mid, worker_id=wid,
                                                                            machine_state=mach_state,
                                                                            report_id=rep1, pockets=pks)
                return render(request, 'production_follow_up/coating{}.html'.format(mid), {'first': first})
        else:
            if coating_shift.objects.all().last().shift_date != timezone.localdate():
                messages.success(request, 'عذرا لم يتم اضافة وردية اليوم ..يمكنك اضافة تقريرك بعد اضافة وردية اليوم')
                return redirect('coating{}'.format(mid),mid)
            rep2 = coating_prodution_follow_up_one.objects.get(report_id=count - 1)
            try:
                ss = coating_production_follow_up_two.objects.get(report_id=rep2, machine_id=mid)
                messages.success(request, 'عذرا تم اضافة تقرير انتاج لهذه الالة في الوردية المحددة')
                return redirect('coating{}'.format(mid),mid)
            except coating_production_follow_up_two.DoesNotExist:
                if mach_state == "متوقف":
                    second = coating_production_follow_up_two.objects.create(machine_id=mid, worker_id="لا احد",
                                                                            machine_state=mach_state, report_id=rep2,
                                                                            pockets=0)
                else:
                    second = coating_production_follow_up_two.objects.create(machine_id=mid, worker_id=wid,
                                                                            machine_state=mach_state,
                                                                            report_id=rep2, pockets=pks)
                return render(request,'production_follow_up/coating{}.html'.format(mid), {'second': second})
    else:
        print(timezone.localdate())
        print(type(pk))
        if pk == "1":
           return render(request, 'production_follow_up/coating1.html')
        else:
            return render(request, 'production_follow_up/coating2.html')


def weaving1(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="follower":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    count = weaving_prodution_follow_up.objects.all().count()
    print(count)
    if request.method == "POST":
        loom=request.POST.get('loom')
        wid = request.POST.get('worker_id')
        pks = request.POST.get('current_produced_amount')
        mach_state = request.POST.get('state')
        if 'one' in request.POST:
            if shift_identifier.objects.all().last().shift_date != timezone.localdate():
                messages.success(request, 'عذرا لم يتم اضافة وردية اليوم ..يمكنك اضافة تقريرك بعد اضافة وردية اليوم')
                return redirect('weaving1')
            rep1 = weaving_prodution_follow_up.objects.get(report_id=count - 2)
            rpp1=weaving_prodution_follow_up_one.objects.get(report_idd=rep1,group_id="أولى")
            try:
                ss = weaving_production_follow_up_two.objects.get(report_id=rpp1, loom_id=loom)
                messages.success(request, 'عذرا تم اضافة تقرير انتاج لهذه الالة في الوردية المحددة')
                return redirect('weaving1')
            except weaving_production_follow_up_two.DoesNotExist:
                if mach_state == "متوقف":
                    first = weaving_production_follow_up_two.objects.create(loom_id=loom, worker_id="لا احد",
                                                                            tate=mach_state, report_id=rpp1,
                                                                            current_produced_amount=0)
                else:
                    first = weaving_production_follow_up_two.objects.create(loom_id=loom, worker_id=wid,
                                                                            tate=mach_state, report_id=rpp1,
                                                                            current_produced_amount=pks)
                print(first)
                return render(request, 'production_follow_up/loom_first_group.html')
        else:
            if shift_identifier.objects.all().last().shift_date != timezone.localdate():
                messages.success(request, 'عذرا لم يتم اضافة وردية اليوم ..يمكنك اضافة تقريرك بعد اضافة وردية اليوم')
                return redirect('weaving1')
            rep2 = weaving_prodution_follow_up.objects.get(report_id=count - 1)
            rpp2=weaving_prodution_follow_up_one.objects.get(report_idd=rep2,group_id="أولى")
            try:
                ss = weaving_production_follow_up_two.objects.get(report_id=rpp2, loom_id=loom)
                messages.success(request, 'عذرا تم اضافة تقرير انتاج لهذه الالة في الوردية المحددة')
                return redirect('weaving1')
            except weaving_production_follow_up_two.DoesNotExist:
                if mach_state == "متوقف":
                    first = weaving_production_follow_up_two.objects.create(loom_id=loom, worker_id="لا احد",
                                                                            tate=mach_state, report_id=rpp2,
                                                                            current_produced_amount=0)
                else:
                    first = weaving_production_follow_up_two.objects.create(loom_id=loom, worker_id=wid,
                                                                            tate=mach_state, report_id=rpp2,
                                                                            current_produced_amount=pks)
                print(first)
                return render(request, 'production_follow_up/loom_first_group.html')
    else:
      return render(request,'production_follow_up/loom_first_group.html')


def show_weaving1(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="follower":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    count = weaving_prodution_follow_up.objects.all().count()
    rep1=weaving_prodution_follow_up.objects.get(report_id=count-2)# morning
    rep2=weaving_prodution_follow_up.objects.get(report_id=count-1)#evening
    r1=weaving_prodution_follow_up_one.objects.get(report_idd=rep1,group_id="أولى")#moring
    r2=weaving_prodution_follow_up_one.objects.get(report_idd=rep2,group_id="أولى")#evening
    looms1=weaving_production_follow_up_two.objects.filter(report_id=r1)#moring
    looms2=weaving_production_follow_up_two.objects.filter(report_id=r2)#evening
    return render(request,'production_follow_up/loom_first_group1.html',{'looms1':looms1,'looms2':looms2})



def weaving2(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="follower":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    count = weaving_prodution_follow_up.objects.all().count()
    print(count)
    if request.method == "POST":
        loom=request.POST.get('loom')
        wid = request.POST.get('worker_id')
        pks = request.POST.get('current_produced_amount')
        mach_state = request.POST.get('state')
        if 'one' in request.POST:
            if shift_identifier.objects.all().last().shift_date != timezone.localdate():
                messages.success(request, 'عذرا لم يتم اضافة وردية اليوم ..يمكنك اضافة تقريرك بعد اضافة وردية اليوم')
                return redirect('weaving2')
            rep1 = weaving_prodution_follow_up.objects.get(report_id=count - 2)
            rpp1=weaving_prodution_follow_up_one.objects.get(report_idd=rep1,group_id="ثانية")
            try:
                ss = weaving_production_follow_up_two.objects.get(report_id=rpp1, loom_id=loom)
                messages.success(request, 'عذرا تم اضافة تقرير انتاج لهذه الالة في الوردية المحددة')
                return redirect('weaving2')
            except weaving_production_follow_up_two.DoesNotExist:
                if mach_state == "متوقف":
                    first = weaving_production_follow_up_two.objects.create(loom_id=loom, worker_id="لا احد",
                                                                            tate=mach_state, report_id=rpp1,
                                                                            current_produced_amount=0)
                else:
                    first = weaving_production_follow_up_two.objects.create(loom_id=loom, worker_id=wid,
                                                                            tate=mach_state, report_id=rpp1,
                                                                            current_produced_amount=pks)
                print(first)
                return render(request, 'production_follow_up/loom_second_group.html')
        else:
            if shift_identifier.objects.all().last().shift_date != timezone.localdate():
                messages.success(request, 'عذرا لم يتم اضافة وردية اليوم ..يمكنك اضافة تقريرك بعد اضافة وردية اليوم')
                return redirect('weaving2')
            rep2 = weaving_prodution_follow_up.objects.get(report_id=count - 1)
            rpp2=weaving_prodution_follow_up_one.objects.get(report_idd=rep2,group_id="ثانية")
            try:
                ss = weaving_production_follow_up_two.objects.get(report_id=rpp2, loom_id=loom)
                messages.success(request, 'عذرا تم اضافة تقرير انتاج لهذه الالة في الوردية المحددة')
                return redirect('weaving2')
            except weaving_production_follow_up_two.DoesNotExist:
                if mach_state == "متوقف":
                    first = weaving_production_follow_up_two.objects.create(loom_id=loom, worker_id="لا احد",
                                                                            tate=mach_state, report_id=rpp2,
                                                                            current_produced_amount=0)
                else:
                    first = weaving_production_follow_up_two.objects.create(loom_id=loom, worker_id=wid,
                                                                            tate=mach_state, report_id=rpp2,
                                                                            current_produced_amount=pks)
                print(first)
                return render(request, 'production_follow_up/loom_second_group.html')
    else:
      return render(request,'production_follow_up/loom_second_group.html')


def show_weaving2(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="follower":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    count = weaving_prodution_follow_up.objects.all().count()
    rep1=weaving_prodution_follow_up.objects.get(report_id=count-2)# morning
    rep2=weaving_prodution_follow_up.objects.get(report_id=count-1)#evening
    r1=weaving_prodution_follow_up_one.objects.get(report_idd=rep1,group_id="ثانية")#moring
    r2=weaving_prodution_follow_up_one.objects.get(report_idd=rep2,group_id="ثانية")#evening
    looms1=weaving_production_follow_up_two.objects.filter(report_id=r1)#moring
    looms2=weaving_production_follow_up_two.objects.filter(report_id=r2)#evening
    return render(request,'production_follow_up/loom_second_group1.html',{'looms1':looms1,'looms2':looms2})


def weaving3(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="follower":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    count = weaving_prodution_follow_up.objects.all().count()
    print(count)
    if request.method == "POST":
        loom=request.POST.get('loom')
        wid = request.POST.get('worker_id')
        pks = request.POST.get('current_produced_amount')
        mach_state = request.POST.get('state')
        if 'one' in request.POST:
            if shift_identifier.objects.all().last().shift_date != timezone.localdate():
                messages.success(request, 'عذرا لم يتم اضافة وردية اليوم ..يمكنك اضافة تقريرك بعد اضافة وردية اليوم')
                return redirect('weaving3')
            rep1 = weaving_prodution_follow_up.objects.get(report_id=count - 2)
            rpp1=weaving_prodution_follow_up_one.objects.get(report_idd=rep1,group_id="ثالثة")
            try:
                ss = weaving_production_follow_up_two.objects.get(report_id=rpp1, loom_id=loom)
                messages.success(request, 'عذرا تم اضافة تقرير انتاج لهذه الالة في الوردية المحددة')
                return redirect('weaving3')
            except weaving_production_follow_up_two.DoesNotExist:
                if mach_state == "متوقف":
                    first = weaving_production_follow_up_two.objects.create(loom_id=loom, worker_id="لا احد",
                                                                            tate=mach_state, report_id=rpp1,
                                                                            current_produced_amount=0)
                else:
                    first = weaving_production_follow_up_two.objects.create(loom_id=loom, worker_id=wid,
                                                                            tate=mach_state, report_id=rpp1,
                                                                            current_produced_amount=pks)
                print(first)
                return render(request, 'production_follow_up/loom_third_group.html')
        else:
            if shift_identifier.objects.all().last().shift_date != timezone.localdate():
                messages.success(request, 'عذرا لم يتم اضافة وردية اليوم ..يمكنك اضافة تقريرك بعد اضافة وردية اليوم')
                return redirect('weaving3')
            rep2 = weaving_prodution_follow_up.objects.get(report_id=count - 1)
            rpp2=weaving_prodution_follow_up_one.objects.get(report_idd=rep2,group_id="ثالثة")
            try:
                ss = weaving_production_follow_up_two.objects.get(report_id=rpp2, loom_id=loom)
                messages.success(request, 'عذرا تم اضافة تقرير انتاج لهذه الالة في الوردية المحددة')
                return redirect('weaving3')
            except weaving_production_follow_up_two.DoesNotExist:
                if mach_state == "متوقف":
                    first = weaving_production_follow_up_two.objects.create(loom_id=loom, worker_id="لا احد",
                                                                            tate=mach_state, report_id=rpp2,
                                                                            current_produced_amount=0)
                else:
                    first = weaving_production_follow_up_two.objects.create(loom_id=loom, worker_id=wid,
                                                                            tate=mach_state, report_id=rpp2,
                                                                            current_produced_amount=pks)
                print(first)
                return render(request, 'production_follow_up/loom_third_group.html')
    else:
      return render(request,'production_follow_up/loom_third_group.html')


def show_weaving3(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="follower":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    count = weaving_prodution_follow_up.objects.all().count()
    rep1=weaving_prodution_follow_up.objects.get(report_id=count-2)# morning
    rep2=weaving_prodution_follow_up.objects.get(report_id=count-1)#evening
    r1=weaving_prodution_follow_up_one.objects.get(report_idd=rep1,group_id="ثالثة")#moring
    r2=weaving_prodution_follow_up_one.objects.get(report_idd=rep2,group_id="ثالثة")#evening
    looms1=weaving_production_follow_up_two.objects.filter(report_id=r1)#moring
    looms2=weaving_production_follow_up_two.objects.filter(report_id=r2)#evening
    return render(request,'production_follow_up/loom_third_group1.html',{'looms1':looms1,'looms2':looms2})














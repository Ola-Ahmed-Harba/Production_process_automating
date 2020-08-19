from django.shortcuts import render
from django.views.generic import TemplateView

from django.shortcuts import get_object_or_404,render,redirect
from os import access, path, R_OK

from django.http import  JsonResponse
from numpy import roll
import zxing
from .qrr import fun_insanity



from howdy.forms import Roll_coating_Form,Roll_identifier_Form,\
    Roll_printing_Form,Roll_weaving_Form,Roll_cutting_Form
from howdy.models import Manger,Roll_cutting,cutting_shift,coating_shift,printing_shift,Roll_printing,Roll_Coating,\
    Roll_weaving,Roll_Identifier,shift_identifier,User,Order_item,roll_final_waste
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,HttpResponseRedirect
from .help_functions import stringToRGB
from pyzbar import pyzbar
import argparse
import cv2
import imutils
from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required



from django.contrib import messages
# Create your views here.


class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)

from django.views.decorators.csrf import csrf_exempt
class AboutPageView(TemplateView):
    template_name = "about.html"




@csrf_exempt
def take_image_looms(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "looms":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    print(request.GET)
    return render(request, 'VC/index_looms.html', {})





@csrf_exempt
@login_required
def vc_handel(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "looms":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    print("oooooooooooooooooooooooooo")
    print(request.POST)
    barValue = "o"
    img=stringToRGB(request.POST.get('imgsrc'))
    cv2.imwrite('olllaloom.jpg',img)
    ba = fun_insanity('olllaloom.jpg')
    print(ba)
    barValue=ba.parsed
    if barValue=="o" :
        print("welcome")

        return HttpResponse('لم يتم التعرف على الباركود')
    else:
        try:
            roll=Roll_Identifier.objects.get(roll_id=barValue)
            request.session['roll_id'] = barValue
        except Roll_Identifier.DoesNotExist:
            roll=Roll_Identifier.objects.create(roll_id=barValue,order_id=None,item_id=None)
            request.session['roll_id']=barValue
        return HttpResponse("تم اكتشاف هذا الباركود {}".format(barValue))


@login_required
def barcode_by_number_loom(request):
    return render(request,'looms/barcode_by_number.html')



@login_required
def add_roll_by_number(request):
    barValue=request.POST.get("roll_id")
    try:
       roll=Roll_Identifier.objects.get(roll_id=barValue)
       request.session['roll_id'] = 'no'
       messages.success(request, "هذا الرول موجود مسبقا لا يمكن اضافته")
       return redirect('barcode_by_number_loom')
    except Roll_Identifier.DoesNotExist :
        roll=Roll_Identifier.objects.create(roll_id=barValue,order_id=None,item_id=None)
        request.session['roll_id'] = barValue
        messages.success(request, "تم اضافة رول جديد")
        return redirect('roll_weaving_view')




















@login_required
@csrf_exempt
def take_image_looms(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "looms":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    print(request.GET)
    request.session['roll_id'] = "no"
    return render(request, 'VC/index_looms.html', {})


@login_required
def roll_weaving_view(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "looms":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    if request.session['roll_id'] == "no":
        messages.success(request,'لم نتعرف على الباركود بعد... رجاء قم بتصوير باركود اولا')
        return redirect('take_image_looms')
    else:
        form =Roll_identifier_Form()
        form2=Roll_weaving_Form()
        rolls=Roll_Identifier.objects.all().last()
        print("111111111")
        if request.method=="POST":
            if 'add_roll' in request.POST:
                print("2222222222")
                f=Roll_identifier_Form(request.POST)
                if f.is_valid():
                    print("3333333333")
                    roll=Roll_Identifier.objects.get(roll_id=request.session['roll_id'])
                    idd=roll.roll_id
                    roll.delete()
                    try:
                        tt=Order_item.objects.get(order_id=f.cleaned_data['order_id'],item_id=f.cleaned_data['item_id'])
                        new_roll=Roll_Identifier.objects.create(roll_id=idd,order_id=f.cleaned_data['order_id'],item_id=f.cleaned_data['item_id'])
                        new_roll.setPropereties()
                        new_roll.save()
                        rolls=Roll_Identifier.objects.filter(order_id=f.cleaned_data['order_id']).last()
                        form2 = Roll_weaving_Form()
                        return render(request,'rolls/roll_weaving.html',{'form2':form2,'rolls':rolls})
                    except Order_item.DoesNotExist:
                        messages.success(request,"الطلبية لا تحوي العنصر المذكور يرجى اضافة رقم عنصر صحيح")
                        return render(request, 'rolls/roll_weaving.html',
                                      {'form': form, 'form2': form2, 'rolls': rolls})
            else:
                request.session['roll_id'] = "no"
                fw=Roll_weaving_Form(request.POST)
                if fw.is_valid():
                    ww=fw.save(commit=False)
                    ww.roll_id=Roll_Identifier.objects.all().last()
                    ww.current_shift_id=shift_identifier.objects.all().last()
                    ww.save()
                    rolls=Roll_Identifier.objects.all().last()
                    rolls_wev=Roll_weaving.objects.all().last()
                    return render(request, 'rolls/roll_weaving.html',
                                  {'form': form, 'form2': form2, 'rolls': rolls, 'rolls_wev': rolls_wev})
        return render(request,'rolls/roll_weaving.html',{'form':form,'form2':form2})


"""

def roll_printing_view(request):
    print(request.POST)
    if request.is_ajax():
        print(request.POST)
        form = Roll_printing_Form(request.POST)
        if form.is_valid():
            roid = form.cleaned_data['roll_id']
            test = Roll_printing.objects.filter(roll_id=roid)
            if not test:
                print("1111111111111111111111111111111111111111111111111")
                pp=form.save(commit=False)
                pp.shift_id=printing_shift.objects.all().last()
                pp.save()
            return JsonResponse({'Success':'Data Successfully saved'})
        else:
            print("222222222222222222222222222222222222222222222222222222222222")
            print(request.POST)
            return JsonResponse({'Error':'Some Thing Wrong'})
    form =  Roll_printing_Form()
    if request.method == "POST":
        if 'ridbutn' in request.POST:
            rollid = request.POST.get('ridbutn')  # get rool_id
            if rollid:
                roll = Roll_Identifier.objects.get(roll_id=int(rollid))  # get roll info from first table
                roll_w = Roll_weaving.objects.get(roll_id=roll.roll_id)  # get roll first state
                if roll.need_printing!='نعم':
                    return render(request, 'rolls/roll_printing.html')
                roll_c = Roll_Coating.objects.get(roll_id=roll.roll_id)  # get roll first state
                form = Roll_printing_Form(instance=roll)
                return render(request, 'rolls/roll_printing.html', {'roll': roll, 'roll_w': roll_w,'roll_c': roll_c, 'form': form})
            return render(request, 'rolls/roll_printing.html')

    else:
        return render(request, 'rolls/roll_printing.html')

"""

"""
def roll_cutting_view(request):
    print(request.POST)
    if request.is_ajax():
        print(request.POST)
        form = Roll_cutting_Form(request.POST)
        if form.is_valid():
            roid = form.cleaned_data['roll_id']
            test = Roll_cutting.objects.filter(roll_id=roid)
            print("23222222222222222222222222222222222222222222222222222222")
            if not test:
                print("11111111111111111111111111111111111111111111111111111111111")
                pp=form.save(commit=False)
                pp.shift_id=cutting_shift.objects.all().last()
                pp.save()
            return JsonResponse({'Success':'Some Thing Wrong'})
        else:
            print(request.POST)
            return JsonResponse({'Error':'Some Thing Wrong'})
    if request.method == "POST":
        if 'ridbutn' in request.POST:
            rollid = request.POST.get('ridbutn')  # get rool_id
            if rollid:
                roll = Roll_Identifier.objects.get(roll_id=int(rollid))  # get roll info from first table
                roll_w = Roll_weaving.objects.get(roll_id=roll.roll_id)  # get roll first state
                if roll.need_coating!='لا':
                    roll_co = Roll_Coating.objects.get(roll_id=roll.roll_id)  # get roll first state
                else:
                    roll_co=None
                if roll.need_printing!='لا':
                    roll_pr=Roll_printing.objects.get(roll_id=roll.roll_id)
                else:
                    roll_pr=None

                form = Roll_cutting_Form(instance=roll)
                return render(request, 'rolls/roll_cutting.html', {'roll': roll, 'roll_w': roll_w,'roll_co': roll_co,'roll_pr':roll_pr, 'form': form})
            return render(request, 'rolls/roll_cutting.html')

    else:
        return render(request, 'rolls/roll_cutting.html')
"""

















#----------------------------------------------------------------------------------------------------quality updates
@login_required
def quality_roll_weaving_view(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "quality":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    rolls=Roll_weaving.objects.filter(quality_agreement=None)
    return render(request,'quality/roll_weaving.html',{'rolls':rolls})

@login_required
def update_weving_roll(request,pk):
    user = User.objects.get(id=request.user.id)
    if user.position != "quality":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    if request.method =="POST":
        notess=request.POST.get('qn')
        agree=request.POST.get('qa')
        print(notess)
        print(agree)
        item=Roll_weaving.objects.get(roll_id=pk)
        item.quality_agreement=agree
        item.quality_notes=notess
        item.save()
    rolls=Roll_weaving.objects.filter(quality_agreement=None)
    return render(request, 'quality/roll_weaving.html', {'rolls': rolls})

@login_required
def quality_roll_coating_view(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "quality":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    rolls=Roll_Coating.objects.filter(quality_agreement=None)
    return render(request,'quality/roll_coating.html',{'rolls':rolls})

@login_required
def update_coating_roll(request,pk):
    user = User.objects.get(id=request.user.id)
    if user.position != "quality":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    if request.method =="POST":
        notess=request.POST.get('qn')
        agree=request.POST.get('qa')
        print(notess)
        print(agree)
        item=Roll_Coating.objects.get(roll_id=pk)
        item.quality_agreement=agree
        item.quality_notes=notess
        item.save()
    rolls=Roll_Coating.objects.filter(quality_agreement=None)
    return render(request, 'quality/roll_coating.html', {'rolls': rolls})


@login_required
def quality_roll_printing_view(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "quality":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    rolls=Roll_printing.objects.filter(quality_agreement=None)
    return render(request,'quality/roll_printing.html',{'rolls':rolls})

@login_required
def update_printing_roll(request,pk):
    user = User.objects.get(id=request.user.id)
    if user.position != "quality":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    if request.method =="POST":
        notess=request.POST.get('qn')
        agree=request.POST.get('qa')
        print(notess)
        print(agree)
        item=Roll_printing.objects.get(roll_id=pk)
        item.quality_agreement=agree
        item.quality_notes=notess
        item.save()
    rolls=Roll_printing.objects.filter(quality_agreement=None)
    return render(request, 'quality/roll_printing.html', {'rolls': rolls})


@login_required
def quality_roll_cutting_view(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "quality":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    rolls=Roll_cutting.objects.filter(quality_agreement=None)
    return render(request,'quality/roll_cutting.html',{'rolls':rolls})

@login_required
def update_cutting_roll(request,pk):
    user = User.objects.get(id=request.user.id)
    if user.position != "quality":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    if request.method =="POST":
        notess=request.POST.get('qn')
        agree=request.POST.get('qa')
        item=Roll_cutting.objects.get(roll_id=pk)
        item.quality_agreement=agree
        item.quality_notes=notess
        item.save()
    rolls=Roll_cutting.objects.filter(quality_agreement=None)
    return render(request, 'quality/roll_cutting.html', {'rolls': rolls})












@login_required
def delet_false_roll_in_looms(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "looms":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    roll=Roll_Identifier.objects.all().last()
    if not roll.order_id:
        roll.delete()
    return render(request,'VC/index_looms.html')

##################################3----------------------------------------------coating image

@login_required
@csrf_exempt
def take_image_in_coating(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "coating":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    request.session['roll_id'] = "no"
    return render(request,'VC/index_coating.html')

@login_required
@csrf_exempt
def vc_handel_coating(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "coating":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    print("oooooooooooooooooooooooooo")
    print(request.POST)
    barValue = "o"
    img=stringToRGB(request.POST.get('imgsrc'))
    cv2.imwrite('olllacoating.jpg',img)
    ba = fun_insanity('olllacoating.jpg')
    print(ba)
    barValue=ba.parsed
    if barValue=="o" :
        print("welcome")
        request.session['roll_id'] = "no"
        print(request.session['roll_id'])
        return HttpResponse('لم يتم التعرف على الباركود')
    else:
        try:
           rr=Roll_Identifier.objects.get(roll_id=barValue)
           request.session['roll_id'] = barValue
           print(request.session['roll_id'])
           return HttpResponse("تم اكتشاف هذا الباركود {}".format(barValue))
        except Roll_Identifier.DoesNotExist:
           print(request.session['roll_id'])
           return HttpResponse("تم اكتشاف هذا الباركود {} لكن لا يوجد رول بهذا الرقم".format(barValue))

@login_required
def roll_coating_view(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "coating":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    print(request.session['roll_id'])
    if request.session['roll_id']=="no" or None:
        messages.success(request,'لم نتعرف على الباركود بعد... رجاء قم بتصوير باركود اولا')
        return redirect('take_image_in_coating')
    else:
        print("0000000000000000")
        roll = Roll_Identifier.objects.get(roll_id=request.session['roll_id'])
        print(roll.roll_id)
        try:
           roll_w = Roll_weaving.objects.get(roll_id=roll)
        except Roll_weaving.DoesNotExist:
            messages.success(request,"هذا الرول مدخل لكنه غير منسوج بعد")
            return redirect('barcode_by_num_coating')
        if roll.need_coating != 'نعم':
            messages.success(request,'هذا الرول لا يحتاج طلي')
            return redirect('barcode_by_num_coating')
        else:
            print("pppppppppppppppppp")
            if request.method=="POST":
               roid=request.POST.get('roll_id')
               thk=request.POST.get('thikness')
               wl=request.POST.get('waste_long')
               wid=request.POST.get('worker_id')
               test = Roll_Coating.objects.filter(roll_id=roid)
               print(test)
               print("11111111111111111111111111111111111111111111111")
               if not test:
                   print("2222222222222222222222222222222222222222222222222222222222")
                   roll_c = Roll_Coating.objects.create(roll_id=roll,thikness=thk,waste_long=wl,worker_id=wid,shift_id=coating_shift.objects.all().last())
                   roll_c.save()
                   request.session['roll_id'] = "no"
                   messages.success(request,"تم اضافة معلومات الطلي الى معلومات الرول")

                   return render(request,'rolls/roll_coating.html',{'roll': roll, 'roll_w': roll_w, 'roll_c':roll_c})
               else:
                   request.session['roll_id']="no"
                   messages.success(request,"هناك رول بنفس الرقم موجود مسبقا ")
                   return redirect('roll_coating_view')
            else:
                print("Dddddddddddddddddddd")
                form = Roll_coating_Form()
                return render(request, 'rolls/roll_coating.html', {'roll': roll, 'roll_w': roll_w, 'form': form})


@login_required
def barcode_by_num_coating(request):
    return render(request, 'coating/barcode_by_number.html')


@login_required
def vc_handel_coating_by_number(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "coating":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    print("oooooooooooooooooooooooooo")
    print(request.POST)
    barValue = request.POST.get('bar_id')
    try:
        rr = Roll_Identifier.objects.get(roll_id=barValue)
        if rr.need_coating== "لا":
            request.session['roll_id'] = 'no'
            messages.success(request, "تم اكتشاف هذا الباركود {} لكن هذا الرول لا يحتاج طلي".format(barValue))
            return redirect('barcode_by_num_coating')
        request.session['roll_id'] = barValue
        print(request.session['roll_id'])
        messages.success(request, "تم اكتشاف هذا الباركود {}".format(barValue))
        return redirect('roll_coating_view')
    except Roll_Identifier.DoesNotExist:
        messages.success(request, "تم اكتشاف هذا الباركود {} لكن لا يوجد رول بهذا الرقم".format(barValue))
        return redirect('barcode_by_num_coating')


    ###############################-------------------------------------------------------------------------------------------printing
@login_required
@csrf_exempt
def take_image_in_printing(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "printing":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    request.session['roll_id'] = "no"
    return render(request,'VC/index_printing.html')
@login_required
@csrf_exempt
def vc_handel_printing(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "printing":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    print("oooooooooooooooooooooooooo")
    print(request.POST)
    barValue = "o"
    img=stringToRGB(request.POST.get('imgsrc'))
    cv2.imwrite('olllaprinting.jpg',img)
    ba = fun_insanity('olllaprinting.jpg')
    print(ba)
    barValue=ba.parsed
    if barValue=="o" :
        print("welcome")
        request.session['roll_id'] = "no"
        print(request.session['roll_id'])
        return HttpResponse('لم يتم التعرف على الباركود')
    else:
        try:
           rr=Roll_Identifier.objects.get(roll_id=barValue)
           print(request.session['roll_id'])
           if rr.need_printing=="لا":
               return HttpResponse("تم اكتشاف هذا الباركود {} لكن هذا الرول لا يحتاج الى طباعة".format(barValue))
           if rr.need_coating=="نعم":
               try:
                   cc=Roll_Coating.objects.get(roll_id=barValue)
                   request.session['roll_id'] = barValue
                   return HttpResponse("تم اكتشاف هذا الباركود {}".format(barValue))
               except Roll_Coating.DoesNotExist:
                   return HttpResponse("تم اكتشاف هذا الباركود {} لكن هذا الرول يحتاج لطلي وهو غير مطلي بعد".format(barValue))
        except Roll_Identifier.DoesNotExist:
           print(request.session['roll_id'])
           return HttpResponse("تم اكتشاف هذا الباركود {} لكن لا يوجد رول بهذا الرقم".format(barValue))


@login_required
def roll_printing_view(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "printing":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    print(request.session['roll_id'])
    if request.session['roll_id']=="no" or None:
        messages.success(request,'لم نتعرف على الباركود بعد... رجاء قم بتصوير باركود اولا')
        return redirect('take_image_in_printing')
    else:
        print("0000000000000000")
        roll = Roll_Identifier.objects.get(roll_id=request.session['roll_id'])
        try:
            roll_w = Roll_weaving.objects.get(roll_id=roll)
        except Roll_weaving.DoesNotExist:
            messages.success(request, "هذا الرول مدخل لكنه غير منسوج بعد")
            return redirect('barcode_by_num_printing')
        if roll.need_coating=="نعم":
            roll_c=Roll_Coating.objects.get(roll_id=roll)
        roll_c = Roll_Coating.objects.get(roll_id=roll)
        print("pppppppppppppppppp")
        if request.method=="POST":
           roid=request.POST.get('roll_id')
           st=request.POST.get('stain_type')
           si=request.POST.get('stain_info')
           wid=request.POST.get('worker_id')
           test = Roll_printing.objects.filter(roll_id=roid)
           print(test)
           print("11111111111111111111111111111111111111111111111")
           if not test:
               print("2222222222222222222222222222222222222222222222222222222222")
               roll_p = Roll_printing.objects.create(roll_id=roll,stain_info=si,stain_type=st,worker_id=wid,shift_id=printing_shift.objects.all().last())
               roll_p.save()
               request.session['roll_id'] = "no"
               messages.success(request,"تم اضافة معلومات الطباعة الى معلومات الرول")

               if roll.need_coating=="نعم":
                   return render(request,'rolls/roll_printing.html',{'roll': roll, 'roll_w': roll_w, 'roll_c':roll_c,'roll_p':roll_p})
               else:
                   return render(request,'rolls/roll_printing.html',{'roll': roll, 'roll_w': roll_w, 'roll_p':roll_p})
           else:
               request.session['roll_id']="no"
               messages.success(request,"هناك رول بنفس الرقم موجود مسبقا ")
               return redirect('roll_printing_view')
        else:
            print("Dddddddddddddddddddd")
            form = Roll_printing_Form()
            return render(request, 'rolls/roll_printing.html', {'roll': roll, 'roll_w': roll_w, 'form': form,'roll_c':roll_c})


@login_required
def barcode_by_num_printing(request):
    return render(request,'printing/barcode_by_number.html')

@login_required
def vc_handel_printing_by_number(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "printing":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    print("oooooooooooooooooooooooooo")
    print(request.POST)
    barValue = request.POST.get('bar_id')
    try:
       rr = Roll_Identifier.objects.get(roll_id=barValue)
       if rr.need_printing=="لا":
           messages.success(request, "تم اكتشاف هذا الباركود {} لكن هذا الرول لا يحتاج الى طباعة".format(barValue))
           return redirect('barcode_by_num_printing')
       if rr.need_coating=="نعم":
           try:
               cc=Roll_Coating.objects.get(roll_id=barValue)
               request.session['roll_id'] = barValue
               messages.success(request, "تم اكتشاف هذا الباركود {}".format(barValue))
               return redirect('roll_printing_view')
           except Roll_Coating.DoesNotExist:
               request.session['roll_id'] = 'no'
               messages.success(request, "تم اكتشاف هذا الباركود {} لكن هذا الرول يحتاج لطلي وهو غير مطلي بع".format(barValue))
               return redirect('barcode_by_num_printing')
       else:
           messages.success(request, "تم اكتشاف هذا الباركود {}".format(barValue))
           return redirect('roll_printing_view')

    except Roll_Identifier.DoesNotExist:
        request.session['roll_id'] = 'no'
        messages.success(request, "تم اكتشاف هذا الباركود {} لكن لا يوجد رول بهذا الرقم".format(barValue))
        return redirect('barcode_by_num_printing')



















#--------------------------------------------------------------------------------------------------cutting
@login_required
@csrf_exempt
def take_image_in_cutting(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "cutting":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    request.session['roll_id']="no"
    return render(request,'VC/index_cutting.html')

@login_required
@csrf_exempt
def vc_handel_cutting(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "cutting":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    print("oooooooooooooooooooooooooo")
    print(request.POST)
    img=stringToRGB(request.POST.get('imgsrc'))

    #img = imutils.resize(img, width=600)
    cv2.imwrite('olllacutting.jpg',img)
    ba = fun_insanity('olllacutting.jpg')
    print(ba)
    barValue=ba.parsed

    if barValue=="o" :
        print("welcome")
        request.session['roll_id'] = "no"
        print(request.session['roll_id'])
        return HttpResponse('لم يتم التعرف على الباركود')
    else:
        try:
           rr=Roll_Identifier.objects.get(roll_id=barValue)
           print(request.session['roll_id'])
           if rr.need_cutting=="لا":
               return HttpResponse("تم اكتشاف هذا الباركود {} لكن هذا الرول لا يحتاج الى قص".format(barValue))
           if rr.need_coating=="نعم":
               try:
                   cc=Roll_Coating.objects.get(roll_id=barValue)
                   request.session['roll_id'] = barValue
                   return HttpResponse("تم اكتشاف هذا الباركود {}".format(barValue))
               except Roll_Coating.DoesNotExist:
                   return HttpResponse("تم اكتشاف هذا الباركود {} لكن هذا الرول يحتاج لطلي وهو غير مطلي بعد".format(barValue))
        except Roll_Identifier.DoesNotExist:
           print(request.session['roll_id'])
           return HttpResponse("تم اكتشاف هذا الباركود {} لكن لا يوجد رول بهذا الرقم".format(barValue))

@login_required
def roll_cutting_view(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "cutting":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    print(request.session['roll_id'])
    if request.session['roll_id']=="no" or None:
        messages.success(request,'لم نتعرف على الباركود بعد... رجاء قم بتصوير باركود اولا')
        return redirect('take_image_in_cutting')
    else:
        print("0000000000000000")
        roll = Roll_Identifier.objects.get(roll_id=request.session['roll_id'])
        roll_w = Roll_weaving.objects.get(roll_id=roll)
        print("pppppppppppppppppp")
        if request.method=="POST":
           roid=request.POST.get('roll_id')
           mid=request.POST.get('machine_id')
           prp=request.POST.get('produced_packages')
           wid=request.POST.get('worker_id')
           test = Roll_cutting.objects.filter(roll_id=roid)
           print(test)
           print("11111111111111111111111111111111111111111111111")
           if not test:
               print("2222222222222222222222222222222222222222222222222222222222")
               roll_cu = Roll_cutting.objects.create(roll_id=roll,machine_id=mid,produced_packages=prp,worker_id=wid,shift_id=cutting_shift.objects.all().last())
               roll_cu.save()
               request.session['roll_id'] = "no"
               messages.success(request,"تم اضافة معلومات الطباعة الى معلومات الرول")
               if roll.need_coating == "نعم":
                   if roll.need_printing == "نعم":
                       print(1)
                       return render(request, 'rolls/roll_cutting.html',
                                     {'roll': roll, 'roll_w': roll_w, 'roll_cu':roll_cu,
                                      'roll_c': Roll_Coating.objects.get(roll_id=roll),
                                      'roll_p': Roll_printing.objects.get(roll_id=roll)})
                   else:
                       print(2)
                       return render(request, 'rolls/roll_cutting.html',
                                     {'roll': roll, 'roll_w': roll_w, 'roll_cu':roll_cu,
                                      'roll_c': Roll_Coating.objects.get(roll_id=roll)})
               else:
                   if roll.need_printing == "نعم":
                       print(3)
                       return render(request, 'rolls/roll_cutting.html',
                                     {'roll': roll, 'roll_w': roll_w, 'roll_cu':roll_cu,
                                      'roll_p': Roll_printing.objects.get(roll_id=roll)})
                   else:
                       print(4)
                       return render(request, 'rolls/roll_cutting.html',
                                         {'roll': roll, 'roll_w': roll_w, 'roll_cu':roll_cu, })
           else:
               request.session['roll_id'] = "no"
               messages.success(request, "هناك رول بنفس الرقم موجود مسبقا ")
               return redirect('roll_cutting_view')
        else:
            print("Dddddddddddddddddddd")
            form = Roll_cutting_Form()
            if roll.need_coating=="نعم":
                if roll.need_printing=="نعم":
                    print(5)
                    return render(request, 'rolls/roll_cutting.html',
                                  {'roll': roll, 'roll_w': roll_w, 'form': form, 'roll_c': Roll_Coating.objects.get(roll_id=roll),
                                   'roll_p':Roll_printing.objects.get(roll_id=roll)})
                else:
                    print(6)
                    return render(request, 'rolls/roll_cutting.html',
                                  {'roll': roll, 'roll_w': roll_w, 'form': form, 'roll_c': Roll_Coating.objects.get(roll_id=roll)})
            else:
                if roll.need_printing == "نعم":
                    print(7)
                    return render(request, 'rolls/roll_cutting.html',
                                  {'roll': roll, 'roll_w': roll_w, 'form': form,
                                   'roll_p': Roll_printing.objects.get(roll_id=roll)})
                else:
                    print(8)
                    return render(request, 'rolls/roll_cutting.html',
                                      {'roll': roll, 'roll_w': roll_w, 'form': form,})

@login_required
def barcode_by_num(request):
    return render(request,'cutting/barcode_by_number.html')

@login_required
def vc_handel_cutting_by_number(request):
    user = User.objects.get(id=request.user.id)
    if user.position != "cutting":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    print("oooooooooooooooooooooooooo")
    print(request.POST)
    barValue = request.POST.get('bar_id')
    try:
        rr = Roll_Identifier.objects.get(roll_id=barValue)

        if rr.need_cutting == "لا":
            request.session['roll_id'] = 'no'
            messages.success(request, "تم اكتشاف هذا الباركود {} لكن هذا الرول لا يحتاج الى قص".format(barValue))
            return redirect('barcode_by_num')
        if rr.need_coating == "نعم":
            try:
                cc = Roll_Coating.objects.get(roll_id=barValue)
                request.session['roll_id'] = barValue
                return redirect('roll_cutting_view')
            except Roll_Coating.DoesNotExist:
                request.session['roll_id'] = 'no'
                messages.success(request,  "تم اكتشاف هذا الباركود {} لكن هذا الرول يحتاج لطلي وهو غير مطلي بعد".format(barValue))
                return redirect('barcode_by_num')
        else:
            request.session['roll_id'] = barValue
            return redirect('roll_cutting_view')

    except Roll_Identifier.DoesNotExist:
        request.session['roll_id']='no'
        print(request.session['roll_id'])
        messages.success(request,"تم اكتشاف هذا الباركود {} لكن لا يوجد رول بهذا الرقم".format(barValue))
        return redirect('barcode_by_num')




################################################################################################################### normal_user

@csrf_exempt
def vc_handel_normal_user(request):
     user = User.objects.get(id=request.user.id)
     if user.position != "normal":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
     if request.method=="GET":
         return render(request,'VC/index_normal.html')
     else:
            print("oooooooooooooooooooooooooo")
            print(request.POST)
            img=stringToRGB(request.POST.get('imgsrc'))
            img = imutils.resize(img, width=600)
            barcodes = pyzbar.decode(img)
            print(len(barcodes))
            print()
            barValue="o"
            print("hi")
            for barcode in barcodes:
                print("hi2")
                (x, y, w, h) = barcode.rect
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                barcodeData = barcode.data.decode("utf-8")
                barcodeType = barcode.type
                if len(barcodeData)> len(barValue):
                    barValue=barcodeData
                print("mmmmm")
                print(barcodeType)
                print(barcodeData)
                print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
            if barValue=="o" :
                print("welcome")
                request.session['roll_id'] = "no"
                print(request.session['roll_id'])
                return HttpResponse('لم يتم التعرف على الباركود')
            else:
                 request.session['roll_id'] = barValue
                 return HttpResponse("تم اكتشاف هذا الباركود {}".format(barValue))

def view_roll_info(request):
        user = User.objects.get(id=request.user.id)
        if user.position != "normal":
             raise Http404('غير مسموج لك بالدخول لهذا الرابط')
        barValue=request.session['roll_id']
        try:
            roll = Roll_Identifier.objects.get(roll_id=barValue)

            print(roll)
            print("kkkkkkkkkk")

            print(request.session['roll_id'])
            roll_w = Roll_weaving.objects.get(roll_id=roll)
            print(roll_w)
            if roll.need_coating == "نعم":
                try:
                    roll_c = Roll_cutting.objects.get(roll_id=roll)
                except Roll_cutting.DoesNotExist:
                    roll_c = None
            else:
                roll_c = None
            if roll.need_printing == "نعم":
                try:
                    roll_p = Roll_printing.objects.get(roll_id=roll)
                except Roll_printing.DoesNotExist:
                    roll_p = None

            else:
                roll_p = None

            if roll.need_cutting == "نعم":
                try:
                    roll_cu = Roll_cutting.objects.get(roll_id=roll)
                except Roll_cutting.DoesNotExist:
                    roll_cu = None
            else:
                roll_cu = None

            print("i got here")
            request.session['roll_id']="no"
            return render(request, 'rolls/normal_user.html', {'roll': roll, 'roll_w': roll_w, 'roll_c': roll_c, 'roll_p': roll_p, 'roll_cu': roll_cu})

        except Roll_Identifier.DoesNotExist:
          print(request.session['roll_id'])
          messages.success(request," لم يتم انتاج رول بهذا الرقم")
          return redirect('vc_handel_normal_user')
    
####

def roll_waste(request,pk):
    if request.method=="POST":
        roll_id=request.POST.get['roll_id']
        ww=request.POST.get['ww']
        pw=request.POST.get['pw']
        cow=request.POST.get['cow']
        cuw=request.POST.get['cuw']
        roll=roll_final_waste.objects.create(roll_id=roll_id,weaving_waste=ww,cutting_waste=cuw,coating_waste=cow,
                                             printing_waste=pw,shift_id=cutting_shift.objects.all().last())
        return render(request,'rolls/roll_waste.html',{'roll':roll})
    else:
        test=Roll_Identifier.objects.get(pk=pk)
        return render(request, 'rolls/roll_waste.html', {'test': test})

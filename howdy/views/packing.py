from howdy.models import packing_rolls,packs_barcode,Roll_Identifier,User
from django.shortcuts import get_object_or_404,render,redirect
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse, Http404

def add_roll_packing(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="packing":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    rolls = packing_rolls.objects.all()
    rre = Roll_Identifier.objects.all()
    rr = []
    nn =[x.roll_id for x in rolls]
    print(nn)
    for r in rre:
        if r.roll_id in nn:
            print("yes")
        else:
            print("no")
            rr.append(r.roll_id)


    print("11111111111111111111111111111")
    if request.method=="GET":
        return render(request,'packing/add_roll.html',{'rolls':rolls,'rr':rr})
    else:
        rr = []
        for r in rre:
            try:
                t = packs_barcode.objects.get(roll_id=r.roll_id)
                print(t)
            except packs_barcode.DoesNotExist:
                rr.append(r.roll_id)

        roid=request.POST.get('roll_id')
        packer_id = request.POST.get('packer_id')
        worker_id = request.POST.get('worker_id')
        try:
            roll=packing_rolls.objects.get(roll_id=roid)
            messages.success(request,"عذرا هذا الرول تمت اضافته مسبقا ")
            return redirect('add_roll_packing')
        except packing_rolls.DoesNotExist:
            try:
              r=Roll_Identifier.objects.get(roll_id=roid)
              packing_rolls.objects.create(roll_id=roid,packer_id=packer_id,worker_id=worker_id,
                                           packing_date=timezone.localdate(),recorder_id=request.user.username)
              rolls = packing_rolls.objects.all()
              return render(request,'packing/add_roll.html',{'rolls':rolls,'rr':rr})

            except Roll_Identifier.DoesNotExist:
                messages.success(request, "عذرا لم يتم تصنيع رول بهذا الرقم ")
                return redirect('add_roll_packing')



def first_add_pack(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="packing":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    roll=packing_rolls.objects.filter(packer_id="أول").last()
    packs=packs_barcode.objects.filter(roll_id=roll)
    if request.method=="GET":
        return render(request,'packing/first_packer.html',{'packs':packs,'roll':roll})
    else:
        pockets_num=request.POST.get('pockets_num')
        pac_id=request.POST.get('pac_id')
        try:
            p=packs_barcode.objects.get(pac_id=pac_id)
            messages.success(request, "عذرا هذه الحزمة تمت اضافتها مسبقا ")
            return redirect('first_add_pack')
        except packs_barcode.DoesNotExist:
            o=packs_barcode.objects.create(roll_id=roll,pac_id=pac_id,pockets_num=pockets_num)
            packs = packs_barcode.objects.filter(roll_id=roll)
            return render(request, 'packing/first_packer.html', {'packs': packs,'roll':roll})

def second_add_pack(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="packing":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    roll=packing_rolls.objects.filter(packer_id="ثاني").last()
    packs=packs_barcode.objects.filter(roll_id=roll)
    if request.method=="GET":
        return render(request,'packing/second_packer.html',{'packs':packs,'roll':roll})
    else:
        pockets_num=request.POST.get('pockets_num')
        pac_id=request.POST.get('pac_id')
        try:
            p=packs_barcode.objects.get(pac_id=pac_id)
            messages.success(request, "عذرا هذه الحزمة تمت اضافتها مسبقا ")
            return redirect('second_add_pack')
        except packs_barcode.DoesNotExist:
            o=packs_barcode.objects.create(roll_id=roll,pac_id=pac_id,pockets_num=pockets_num)
            packs = packs_barcode.objects.filter(roll_id=roll)
            return render(request, 'packing/second_packer.html', {'packs': packs,'roll':roll})

def third_add_pack(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="packing":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    roll=packing_rolls.objects.filter(packer_id="ثالث").last()
    packs=packs_barcode.objects.filter(roll_id=roll)
    if request.method=="GET":
        return render(request,'packing/third_packer.html',{'packs':packs,'roll':roll})
    else:
        pockets_num=request.POST.get('pockets_num')
        pac_id=request.POST.get('pac_id')
        try:
            p=packs_barcode.objects.get(pac_id=pac_id)
            messages.success(request, "عذرا هذه الحزمة تمت اضافتها مسبقا ")
            return redirect('third_add_pack')
        except packs_barcode.DoesNotExist:
            o=packs_barcode.objects.create(roll_id=roll,pac_id=pac_id,pockets_num=pockets_num)
            packs = packs_barcode.objects.filter(roll_id=roll)
            return render(request, 'packing/third_packer.html', {'packs': packs,'roll':roll})



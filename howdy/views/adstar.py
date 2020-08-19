from django.shortcuts import get_object_or_404,render,redirect
from django.http import  JsonResponse
from howdy.forms import adstar_shift_Form,adstar_daily_report_Form,adstar_daily_report_two_Form
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from datetime import datetime

from howdy.models import User,AD_daily_report_two,AD_daily_report_one,adstar_shift
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import os.path
from django.contrib import messages

@login_required
def shift_identifier_adstar_view(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="adstar":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    form =adstar_shift_Form()
    shifts=adstar_shift.objects.all()
    if request.method=="POST":
        form2=adstar_shift_Form(request.POST)
        if form2.is_valid():
            form2.save()
            shifts=adstar_shift.objects.all()
            return render(request, 'ADStar/ad_shift.html', {'form': form, 'shifts': shifts})
    return render(request,'ADStar/ad_shift.html',{'form': form,'shifts':shifts})

@login_required
def first_adstar_report(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="adstar":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    form=adstar_daily_report_Form()
    form2=adstar_daily_report_two_Form()
    if request.method=="POST":
        if 'add_report' in request.POST :
            ff=adstar_daily_report_Form(request.POST)
            if ff.is_valid():
                rep=ff.save(commit=False)
                rep.machine_id=1
                rep.shift_id=adstar_shift.objects.all().last()
                rep.save()
                return render(request,'ADStar/first_machine_report.html',{'form2':form2,'rep':rep})
            return render(request, 'ADStar/first_machine_report.html', {'form': form})
        else:
            rr=adstar_daily_report_two_Form(request.POST)
            if rr.is_valid():
                re=rr.save(commit=False)
                re.report_id=AD_daily_report_one.objects.all().last()
                re.save()
                all_re=AD_daily_report_two.objects.filter(report_id=re.report_id)
                rep=AD_daily_report_one.objects.all().last()
                return render(request,'ADStar/first_machine_report.html',{'form2':form2,'rep':rep,'all_re':all_re})
            return render(request, 'ADStar/first_machine_report.html', {'form': form})

    else:
        return render(request,'ADStar/first_machine_report.html',{'form':form})


@login_required
def second_adstar_report(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="adstar":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    form=adstar_daily_report_Form()
    form2=adstar_daily_report_two_Form()
    if request.method=="POST":
        if 'add_report' in request.POST :
            ff=adstar_daily_report_Form(request.POST)
            if ff.is_valid():
                rep=ff.save(commit=False)
                rep.machine_id=2
                rep.shift_id=adstar_shift.objects.all().last()
                rep.save()
                return render(request,'ADStar/second_machine_report.html',{'form2':form2,'rep':rep})
            return render(request, 'ADStar/second_machine_report.html', {'form': form})
        else:
            rr=adstar_daily_report_two_Form(request.POST)
            if rr.is_valid():
                re=rr.save(commit=False)
                re.report_id=AD_daily_report_one.objects.all().last()
                re.save()
                all_re=AD_daily_report_two.objects.filter(report_id=re.report_id)
                rep=AD_daily_report_one.objects.all().last()
                return render(request,'ADStar/second_machine_report.html',{'form2':form2,'rep':rep,'all_re':all_re})
            return render(request, 'ADStar/second_machine_report.html', {'form': form})

    else:
        return render(request,'ADStar/second_machine_report.html',{'form':form})


@login_required
def third_adstar_report(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="adstar":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    form=adstar_daily_report_Form()
    form2=adstar_daily_report_two_Form()
    if request.method=="POST":
        if 'add_report' in request.POST :
            ff=adstar_daily_report_Form(request.POST)
            if ff.is_valid():
                rep=ff.save(commit=False)
                rep.machine_id=3
                rep.shift_id=adstar_shift.objects.all().last()
                rep.save()
                return render(request,'ADStar/third_machine_report.html',{'form2':form2,'rep':rep})
            return render(request, 'ADStar/third_machine_report.html', {'form': form})
        else:
            rr=adstar_daily_report_two_Form(request.POST)
            if rr.is_valid():
                re=rr.save(commit=False)
                re.report_id=AD_daily_report_one.objects.all().last()
                re.save()
                all_re=AD_daily_report_two.objects.filter(report_id=re.report_id)
                rep=AD_daily_report_one.objects.all().last()
                return render(request,'ADStar/third_machine_report.html',{'form2':form2,'rep':rep,'all_re':all_re})
            return render(request, 'ADStar/third_machine_report.html', {'form': form})

    else:
        return render(request,'ADStar/third_machine_report.html',{'form':form})



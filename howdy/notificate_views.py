""""
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import *

def make_readed(request, pk):
	n = notificate.objects.filter(recipient=request.user, id=pk)
	if len(n) > 0:
		n[0].is_readed = True
		n[0].save()

	return redirect(n[0].url)

def get_count(request):
	user_no = notificate.objects.filter(recipient=request.user, is_readed=False)
	return JsonResponse({'count':len(user_no)})



@login_required
def notifihome(request):
	notifications = notificate.objects.filter(recipient=request.user, is_readed=False)
	return render(request, 'notifications_home.html', {'notifications':notifications})
"""
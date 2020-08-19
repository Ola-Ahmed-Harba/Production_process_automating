from howdy.forms import UserLoginForm
from django.shortcuts import get_object_or_404,render,redirect,reverse
from django.http import HttpResponse
from howdy.models import User

from django.contrib.auth import (
      authenticate,
      get_user_model,
      login,
      logout,
 )

def test_home(request):
    print(request.META.get('REMOTE_ADDR'))
    return HttpResponse('ok!')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/ola/')

    title = "Login"
    form = UserLoginForm(request.POST or None)
    print(request.POST)
    print(form.is_valid())
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get('password')
        # request.session['username'] = username
        print(form.cleaned_data)
        print('valid')
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            man = User.objects.get(id=request.user.id)
            if man.position == 'sales':
                return redirect('add_order_view')
            if man.position == 'Production_manager':
                return redirect('orders_in_p_manager_page')
            if man.position == 'extruder':
                return redirect('shift_identifier_extruder_view')
            if man.position == 'cutting':
                return redirect('shift_identifier_cutting_view')
            if man.position == 'coating':
                return redirect('shift_identifier_coating_view')
            if man.position == 'looms':
                return redirect('shift_identifier_view')
            if man.position == 'printing':
                return redirect('shift_identifier_printing_view')
            if man.position == "quality":
                return redirect('printing_waste_view')
            if man.position == "follower":
                return redirect('printing1')
            if man.position == "packing":
                return redirect('add_roll_packing')

        else:
            context = {"title": title}
            context['error'] = 'username or password isn\'t valid'
            return render(request, "authentication/login.html", context)
    return render(request, "authentication/login.html", {"form":form, "title": title})

def redirectLogin(request,username):
    return render(request, 'orders/{}.html'.format(username), {'username': username})

def logoutt(request):
    logout(request)
    return redirect(reverse('login'))


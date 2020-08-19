from builtins import id

from django.shortcuts import get_object_or_404,render,redirect
from django.utils import timezone
from howdy.models import Manger,Productio_order,Order_item,Customer,Productio_order_test2,order_sch,User
from howdy.forms import agreements_for_order_sch_form,order_sch_Form,OrderForm,ItemForm,customerForm
from django.http import  JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.contrib import messages

def index(request):
    return render(request, 'index.html')


@login_required
def add_order_view(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="sales":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                o=Productio_order.objects.get(id=form.cleaned_data['id'])
                messages.success(request,"عذرا يوجد طلبية بنفس الاسم الرجاء ادخال رقم اخر")
                return render(request, 'sales/add_order.html', {'form': form})
            except Productio_order.DoesNotExist:
                order = form.save(commit=False)
                order.order_date = timezone.now()

                order.save()

                r = Productio_order.objects.get(id=form.cleaned_data['id'])
                print(r)
                Productio_order_test2.objects.create(order_id=r.id, customer_name=r.customer_name,
                                                    order_date=r.order_date, start_time=r.start_time,
                                                    delivery_time=r.delivery_time,
                                                    delivery_way=r.delivery_way,
                                                    order_status=r.order_status, notes=r.notes,
                                                    production_manager_agreement=r.production_manager_agreement)
                if order.pk is None :
                    return render(request, 'sales/add_order.html', {'form': form})
                else :
                    return redirect('add_item', order.id)
        else:
            messages.success(request, "عذرا بعض المدخلات غير صحيحة")
            return render(request, 'sales/add_order.html', {'form': form})

    else:
        form = OrderForm()
        return render(request, 'sales/add_order.html', {'form': form})

@login_required
def add_item(request,pk):
    user=User.objects.get(id=request.user.id)
    if user.position!="sales":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')

    order = get_object_or_404(Productio_order, pk=pk)
    items = Order_item.objects.filter(order_id=pk)
    if request.method=="POST":
        if 'add_item_btn' in request.POST:
            form2=ItemForm(request.POST)
            print(form2)
            if form2.is_valid():
                item=form2.save(commit=False)
                item.order_id=order
                print(item)
                item.save()
                return redirect('add_item',pk)
            else:
                form = ItemForm()
                return render(request, 'sales/add_item.html', {'order': order, 'items': items, 'form': form})
        else:
            return redirect('show_total_order',pk)
    else:
        form=ItemForm()
        return render(request, 'sales/add_item.html', {'order': order, 'items' :items, 'form' :form})

@login_required
def show_total_order(request,pk):
    user=User.objects.get(id=request.user.id)
    if user.position!="sales":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    order = get_object_or_404(Productio_order, pk=pk)
    items=Order_item.objects.filter(order_id=pk)
    return render(request, 'sales/show_total_order.html', {'order': order, 'items' :items})

@login_required
def add_new_customer(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="sales":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    customers=Customer.objects.all()
    form = customerForm()
    if request.method=="GET":
        return render(request, 'sales/add_customer.html', {'form':form, 'customers':customers})
    else:
        form2=customerForm(request.POST)
        if form2.is_valid():
            form2.save()
            return render(request, 'sales/add_customer.html', {'form':form, 'customers':customers})
        else:
            print('invailed')

    return render(request, 'sales/add_customer.html')


@login_required
def update_F_M_BY_sales_one(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="sales":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    orders=Productio_order.objects.filter(sales_manager_agreement='لا')
    return render(request, 'sales/factory_m_update.html',  { 'orders':orders })

@login_required
def update_F_M_BY_sales_two(request,pk):
    user=User.objects.get(id=request.user.id)
    if user.position!="sales":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    order = get_object_or_404(Productio_order, pk=pk)
    order2 = get_object_or_404(Productio_order_test2, pk=pk)

    if request.POST.get('sdate') != '2000-11-11':
        order.start_time = request.POST.get('sdate')
    if request.POST.get('ddate') != '2000-11-11':
        order.delivery_time = request.POST.get('ddate')
    if request.POST.get('dw') != "لا يوجد":
        order.delivery_way = request.POST.get('dw')
    if int(request.POST.get('pri')) != 0:
        order.total_price = request.POST.get('pri')
    if request.POST.get('pcy') != 'SP':
        order.payment_currency = request.POST.get('pcy')
    if request.POST.get('pw') != "لا يوجد":
         order.payment_way = request.POST.get('pw')
    if request.POST.get('ag') != "لا":
         order.sales_manager_agreement = request.POST.get('ag')
    order.production_manager_agreement=order2.production_manager_agreement
    order.save()
    messages.success(request,'تم تعديل الطلبية وتثبيتها بنجاح!')
    return redirect('update_F_M_BY_sales_one')

@login_required
def orders_in_sales_page(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="sales":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    orders=Productio_order.objects.filter(~Q(order_status="انتهى") & Q(sales_manager_agreement="نعم") )
    return render(request,'sales/orders.html',{'orders':orders})

def orders_in_sales_page_two(request,pk):
    order=Productio_order.objects.get(id=pk)
    return render(request,'sales/show_total_order_two.html',{'order':order})

@login_required
def search_by_order_id(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="sales":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    if request.method=="POST":
        order_id=request.POST.get('order_id')
        try:
            order=Productio_order.objects.get(id=order_id)
        except Productio_order.DoesNotExist:
            messages.success(request," لا يوجد طلبية بهذا الرقم الرجاء التحقق من الرقم")
            return render(request, 'sales/search_by_order_id.html')
        return render(request,'sales/search_by_order_id.html',{'order':order})
    else:
        return render(request, 'sales/search_by_order_id.html')

@login_required
def search_by_customer_name(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="sales":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    if request.method=="POST":
        customer_name=request.POST.get('customer_name')
        try:
            cn=Customer.objects.get(customer_name=customer_name)
            orders=Productio_order.objects.filter(customer_name=cn)
            return render(request, 'sales/search_by_customer_name.html', {'orders': orders})

        except Customer.DoesNotExist:
            messages.success(request,"لا يوجد زبون بهذا الاسم الرجاء التحقق من الاسم")
            return render(request, 'sales/search_by_customer_name.html')
    else:
        return render(request, 'sales/search_by_customer_name.html')

@login_required
def order_plan_state_sales(request):
    user=User.objects.get(id=request.user.id)
    if user.position!="sales":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    plans=order_sch.objects.filter(state="جاري التصنيع")
    return render(request,'sales/planning_states.html',{'plans':plans})



@login_required
def update_order_as_new_order(request,pk):
    user=User.objects.get(id=request.user.id)
    if user.position!="sales":
        raise Http404('غير مسموج لك بالدخول لهذا الرابط')
    order=get_object_or_404(Productio_order,pk=pk)
    return render(request,'sales/update_order_as_new_order.html')





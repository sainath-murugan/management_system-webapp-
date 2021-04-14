from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from .form import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from django.contrib import messages
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group
# sai
#sainath@3

@unauthenticated_user
def login_user(request):
    
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.info(request, "user name or password is incorrect")
        return render(request, "accounts/login_form.html")

@login_required(login_url="login")
def logout_user(request):
    logout(request)
    return redirect("login")

@unauthenticated_user
def register(request):

        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get("username")
                
                messages.success(request, "account created for"+ username)
                return redirect("login")
        return render(request, "accounts/register_form.html",{"form": form})

def user(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status="delivered").count()
    pending = orders.filter(status="pending").count()
    return render(request, "accounts/user.html",{"total_order": total_orders, "orders":orders,  "delivered": delivered, "pending": pending})
@login_required(login_url="login")
@admin_only
def home(request):
    
    order = Order.objects.all()
    customer = Customer.objects.all()
    total_orders = order.count()
    delivered = order.filter(status="delivered").count()
    pending = order.filter(status="pending").count()
    return render(request, "accounts/dashboard.html", {"orders": order, "customer": customer, "total_order": total_orders, "delivered": delivered, "pending": pending})
@login_required(login_url="login")
@allowed_users(allowed=["admin"])
def products(request):
    product = Products.objects.all()
    return render(request, "accounts/products.html",{"product": product})

@login_required(login_url="login")
@allowed_users(allowed=["customer"])
def account_setting(request):
    customer = request.user.customer 
    form = CustomerForm(instance=customer)
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    return render(request, "accounts/account_setting.html",{"form":form})

@login_required(login_url="login")
@allowed_users(allowed=["admin"])
def customers(request, id):
    customer = Customer.objects.get(id=id)
    order = customer.order_set.all()
    order_count = order.count()
    orderfilter = OrderFilter(request.GET, queryset=order)
    order = orderfilter.qs
    return render(request, "accounts/customer.html",{"customer": customer, "orders": order, "order_count": order_count, "order_filter": orderfilter})

@login_required(login_url="login")
@allowed_users(allowed=["admin"])
def create_order(request, id):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=("products", "status")) #parent, child
    customer = Customer.objects.get(id = id)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    #form = OrderForm(initial={'customer':customer})
    if request.method == "POST":
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect("/")
    return render(request, "accounts/order_form.html",{"formset": formset})

@login_required(login_url="login")
@allowed_users(allowed=["admin"])
def update_order(request, id):
    order = Order.objects.get(id=id)
    form = OrderForm(instance=order) #full instance of the data in the primary id
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("/")
    return render(request, "accounts/update_form.html",{"form": form})
    
@login_required(login_url="login")
@allowed_users(allowed=["admin"])
def delete_order(request, id):
    order = Order.objects.get(id=id)
    if request.method == "POST":
            order.delete()
            return redirect("/")

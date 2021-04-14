# management_system

This project is developed by python library "django". It is a management app to place the customer's order.I have used many classes and methods in django to make the website more dynamic.
Read below to view the specification of the website 👇

# features in the website

* registeration
* Good login/out feature
* Password reset feature
* User profile page with image
* Backend works
* AWS RDS database and s3 bucket
* Deployment in Heroku
* Specification of website

# REGISTERATION
   I have created a form class in `form.py` file and implemented the form in registeration page to create User with django class `from django.contrib.auth.models import User`. It is used to create a customer id.
 
 ``` python
 
 class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
```

# Login/Logout
   I have created a good login/out feature in this project so the customer can logout and login any time. If the user is already logged in they can't visit the login page again.

``` python

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
```

# Password reset
  Django provides a good password reset capability by email. I have implemented the feature in this project so the user can reset their password when they want.
  
  ``` python
    from django.contrib.auth import views as auth_views
    
    
    path("reset_password", auth_views.PasswordResetView.as_view(template_name="accounts/reset_password.html"), name="reset_password"),
    path("reset_password_sent", auth_views.PasswordResetDoneView.as_view(template_name="accounts/reset_password_sent.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="accounts/reset_password_email.html"), name="password_reset_confirm"),
    path("reset_password_complete", auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"), name="password_reset_complete")
 ```
# User profile page
  
  I have created a sepreate template for user profile page. so the customer can update their detail anytime the can with profile picture. The customer can update their detail by ` CustomerForm` class in form.py file.
  
  ``` python
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
 ```

# Backend Works
   I have used many classes and method to make the website more dynamic such as, i have used `django-filter==2.4.0` to make the search very easier to the admin.
 I have created a sepreate `decarators.py` file and created `unauthenticated_user`, `allowed_users`, `admin_only` classes to make the login and regiteration feature more efficeint.
 
 I have also used signals to make the communication better
 
  ``` python
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Customer
from django.contrib.auth.models import Group

def customer_profile(sender, instance, created, **kwargs):
     if created:
        group = Group.objects.get(name = "customer")
        instance.groups.add(group)
        Customer.objects.create(user=instance, name=instance.username)

post_save.connect(customer_profile, sender=User)
 ```
# AWS RDS database and s3 bucket
   I have created a Postgresql database in AWS and connected it with my django app. so, the user's data can be stoed in live rds.
   And i have created a s3 bucket to store the static and image file in aws and it is controlled by `boto3==1.17.49`, `django-storages==1.11.1`.
   
   ``` python
#aws

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN = "%s.s3.amazonaws.com" % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400"
}
AWS_DEFAULT_ACL = None
AWS_S3_FILE_OVERWRITE = False

#s3 static setting
AWS_LOCATION = 'static'
STATIC_URL = "https://%s/%s/" %(AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
DEFAULT_FILE_STORAGE = "webapp.storage_backends.StaticStorage"



#s3 public media setting
PUBLIC_MEDIA_LOCATION = "images"
MEDIA_URL = "https://%s/%s/" %(AWS_S3_CUSTOM_DOMAIN, PUBLIC_MEDIA_LOCATION)
DEFAULT_FILE_STORAGE = "webapp.storage_backends.PublicMediaStorage"
```
# Deployment in Heroku   
 I have deployed the app in heroku and the app is in live so anyone can view it.
 You can also register your id [here](https://sainathmanagement.herokuapp.com/register)
 
 # Specification of website
  In this website the admin can manage the orders of the customer. The admin page has many specification such as update, delete the customer's order.
  And i have used `model` method `count()` to show number of orders- delivered, pending, total in the home page from the database. And in the customer id's page, the customer can view the number of order placed by him.  I have also used Bootstrap to style the page.

  ``` python
@login_required(login_url="login")
@admin_only
def home(request):
    
    order = Order.objects.all()
    customer = Customer.objects.all()
    total_orders = order.count()
    delivered = order.filter(status="delivered").count()
    pending = order.filter(status="pending").count()
    return render(request, "accounts/dashboard.html", {"orders": order, "customer": customer, "total_order": total_orders, "delivered": delivered, "pending": pending})
   ```
  
      

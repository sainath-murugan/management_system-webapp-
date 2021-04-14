# management_system

This project is developed by python library "django". It is a management app to place the customer's order.I have used many classes and methods in django to make the website more dynamic.
Read below to view the specification of the website 👇

# features in the website

* registeration
* Good login/out feature
* Password reset feature
* User profile page with image
* Backend works
* AWS RDS database
* Deployment in Heroku

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

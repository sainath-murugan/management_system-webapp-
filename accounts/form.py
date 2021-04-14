from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User  #used to add fields
from django.contrib.auth.forms import UserCreationForm #used to create a user account

class OrderForm(ModelForm): #ModelForm is used to convert model into form in web
    class Meta:
        model = Order
        fields = "__all__"

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
       
class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        exclude = ["user"]

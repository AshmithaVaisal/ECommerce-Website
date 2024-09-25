from django.contrib.auth.forms import UserCreationForm
from .models import User,Customer,Order
from django import forms


class CustomUserForm(UserCreationForm):
  
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':"Enter your name"}))
    email=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':"Enter your email address"}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':"Enter your password"}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':"Re-Enter your password"}))

    class Meta:
        model=User
        fields = ['username','email','password1','password2']

#for pp ashmitha made changes
# class CheckoutForm(forms.Form):
#     customer_name = forms.CharField(max_length=100)
#     customer_email = forms.EmailField()
#     shipping_address = forms.CharField(widget=forms.Textarea)


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'location', 'shipping_address']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'quantity']
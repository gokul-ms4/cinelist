from django import forms

from myapp.models import *

class UserRegistrationForm(forms.ModelForm):

    class Meta:

        model = CustomUserModel

        fields = ["username","email","phone_number","password"]

        widgets = {
            "username":forms.TextInput(attrs={"class":"form-control w-100 mx-auto","placeholder":"Enter your name"}),
            "email":forms.TextInput(attrs={"class":"form-control w-100 mx-auto","placeholder":"Enter your email"}),
            "phone_number":forms.TextInput(attrs={"class":"form-control w-100 mx-auto","placeholder":"Enter your phonr number"}),
            "password":forms.PasswordInput(attrs={"class":"form-control w-100 mx-auto","placeholder":"Enter your password"})
        }

class OtpVerifyForm(forms.Form):

    otp = forms.CharField(max_length=100,label="", widget=forms.TextInput(attrs={"class":"form-control w-100 mx-auto","placeholder":"Enter OTP"}))

class LoginForm(forms.Form):

    username = forms.CharField(max_length=100,widget = forms.TextInput(attrs={"class":"form-control w-100 mx-auto","placeholder":"Enter username"}))

    password = forms.CharField(max_length=100,widget = forms.PasswordInput(attrs={"class":"form-control w-100 mx-auto","placeholder":"Enter password"}))

class ForgotPasswordForm(forms.Form):

    email = forms.CharField(max_length=100,label="", widget=forms.TextInput(attrs={"class":"form-control w-100 mx-auto","placeholder":"Enter Email"}))

class NewPasswordForm(forms.Form):

        new_password = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class":"form-control w-100 mx-auto","placeholder":"Enter password"}))

        confirm_password = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class":"form-control w-100 mx-auto","placeholder":"Enter password"}))

class UserUpdateForm(forms.ModelForm):
     
     class Meta:
          
          model = CustomUserModel

          fields = ["username","email","phone_number"]

          widgets = {
            "username":forms.TextInput(attrs={"class":"form-control w-100 mx-auto","placeholder":"Enter your name"}),
            "email":forms.TextInput(attrs={"class":"form-control w-100 mx-auto","placeholder":"Enter your email"}),
            "phone_number":forms.TextInput(attrs={"class":"form-control w-100 mx-auto","placeholder":"Enter your phonr number"})
          }
    
class CurrentPassword(forms.Form):
     
     current_password = forms.CharField(max_length=100,label="",widget = forms.PasswordInput(attrs={"class":"form-control w-100 mx-auto"}))

class NewPasswordForm1(forms.Form):

        new_password = forms.CharField(max_length=100,label="", widget=forms.TextInput(attrs={"class":"form-control w-100 mx-auto","placeholder":"Enter New Password"}))

        confirm_password = forms.CharField(max_length=100,label="", widget=forms.TextInput(attrs={"class":"form-control w-100 mx-auto mt-4","placeholder":"Confirm New Password"}))


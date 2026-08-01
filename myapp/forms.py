from django import forms

from myapp.models import *

class UserRegistrationForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control w-100 mx-auto", "placeholder": "Enter your password"})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control w-100 mx-auto", "placeholder": "Confirm your password"})
    )

    class Meta:
        model = CustomUserModel
        fields = ["username", "email", "phone_number"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control w-100 mx-auto", "placeholder": "Enter your username"}),
            "email": forms.EmailInput(attrs={"class": "form-control w-100 mx-auto", "placeholder": "Enter your email"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control w-100 mx-auto", "placeholder": "Enter your phone number"}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username', '').lower()
        if CustomUserModel.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("A user with that username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower()
        if not email:
            raise forms.ValidationError("Email is required.")
        if CustomUserModel.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.username = user.username.lower()
        if commit:
            user.save()
        return user
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

    new_password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={
            "class": "form-control w-100 mx-auto",
            "placeholder": "Enter password"
        })
    )

    confirm_password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={
            "class": "form-control w-100 mx-auto",
            "placeholder": "Enter password"
        })
    )
class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = CustomUserModel
        fields = ["profile_picture"]
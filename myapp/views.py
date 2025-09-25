from django.shortcuts import render,redirect

from django.contrib.auth import login,logout,authenticate

from myapp.models import *

from movies.models import *

from myapp.forms import *

from django.views.generic import View

import random

from django.core.mail import send_mail

from django.utils.decorators import method_decorator

from django.contrib.auth.decorators import login_required

class UserRegisterView(View):

    def get(self,request):

        form = UserRegistrationForm

        return render(request,"signup.html",{"form":form})
    
    def post(self,request):

        form = UserRegistrationForm(request.POST)

        if form.is_valid():
          
          otp = random.randint(1000,9999)

          request.session["otp"] = otp

          print(otp)

          email = form.cleaned_data.get("email")

          request.session["username"] =  form.cleaned_data.get("username")

          request.session["email"] =  email

          request.session["phone_number"] =  form.cleaned_data.get("phone_number")

          request.session["password"] =  form.cleaned_data.get("password")

        send_mail(subject="OTP FOR SIGNUP",message=str(otp),from_email="gokulms538@gmail.com",recipient_list=[email])

        return redirect("otpverify")
    
class CinelistHomeView(View):

    def get(self,request):

        return render(request,"cinelist_home.html")
    
class IntroView(View):

    def get(self,request):

        return render(request,"home.html")
        
class OtpVerifyView(View):

    def get(self,request):

        form = OtpVerifyForm

        return render(request,"otpverify.html",{"form":form})
    
    def post(self,request):

        form = OtpVerifyForm(request.POST)

        if form.is_valid():

            entered_otp = form.cleaned_data.get("otp")

            generated_otp = request.session.get("otp")

            if entered_otp == str(generated_otp):

                username = request.session.get("username")

                password = request.session.get("password")

                email = request.session.get("email")

                phone_number = request.session.get("phone_number")

                user = CustomUserModel.objects.create_user(username=username,password=password,email=email,phone_number=phone_number)

                WishlistModel.objects.create(user_id = user)

                WatchlistModel.objects.create(user_id = user)

                ReviewModel.objects.create(user_id = user)

                login(request,user)

                return render(request,"cinelist_home.html")
            
            else:

                return redirect("otpverify")

class LoginView(View):

    def get(self,request):

        form = LoginForm

        return render(request,"login.html",{"form":form})
    
    def post(self,request):

        form = LoginForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data.get("username")

            password = form.cleaned_data.get("password")

            user_obj = authenticate(request,username=username,password=password)

            if user_obj:

                login(request,user_obj)

                return redirect("cinelist_home")
            
            else:

                return redirect("login")

class ForgetPasswordView(View):

    def get(self,request):

        form = ForgotPasswordForm

        return render(request,"forgotpswd.html",{"form":form})
    
    def post(self,request):

        form = ForgotPasswordForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data.get("email")

            otp = random.randint(1000,9999)

            request.session["otp"] = str(otp)

            request.session["email"] = email

            send_mail(subject="OTP for Reset Password",
                      message=str(otp),
                      from_email="gokulms538@gmail.com",
                      recipient_list=[email])
            
            return redirect("pswdotp")
        
        else:

            return render(request,"forgotpswd.html")
        
class ForgotOtpVerifyView(View):

    def get(self,request):

      form = OtpVerifyForm

      return render(request,"pswdotp.html",{"form":form})
    
    def post(self,request):

        form = OtpVerifyForm(request.POST)

        if form.is_valid():

            entered_otp = form.cleaned_data.get("otp")

            generated_otp = request.session.get("otp")

            if entered_otp == generated_otp:

                return redirect("newpswd")
            
            else:

                return render(request,"pswdotp.html")
            
class NewPasswordView(View):

    def get(self,request):

        form = NewPasswordForm

        return render(request,"new_password.html",{"form":form})
    
    def post(self,request):

        form = NewPasswordForm(request.POST)

        if form.is_valid():

            new_password = form.cleaned_data.get("new_password")

            confirm_password = form.cleaned_data.get("confirm_password")

            if new_password == confirm_password:

                email = request.session.get("email")

                user_obj = CustomUserModel.objects.get(email=email)

                user_obj.set_password(new_password)

                user_obj.save()

                return redirect("login")
            
        else:

                return render(request,"new_password.html")

@method_decorator(login_required,name="dispatch")
class UserProfileView(View):

    def get(self,request,**kwargs):

        user = request.user

        details = CustomUserModel.objects.get(username=user)

        following = FollowingModel.objects.filter(user_obj = user)

        follower = FollowingModel.objects.filter(following_id = user.id )

        if following:

         total = following.count()

        else:

            total = 0

        if follower:

            count = follower.count()

        else:

            count = 0

        watchlist_id = WatchlistModel.objects.get(user_id = request.user)

        watchlist = WatchlistItems.objects.filter(watchlist_id = watchlist_id)

        review_id = ReviewModel.objects.get(user_id = request.user)

        reviews = ReviewItems.objects.filter(review_id = review_id)

        return render(request,"user_profile.html",{"details":details,"total":total,"count":count,
                                                   "watchlist" : watchlist, "reviews" : reviews})
    
@method_decorator(login_required,name="dispatch")
class LogoutView(View):

    def get(self,request):

        logout(request)

        return redirect("login")

class UserUpdateView(View):

    def get(self,request):

        user = CustomUserModel.objects.get(username=request.user)

        form = UserUpdateForm(instance=user)

        return render(request,"edit_profile.html",{"form":form})
    
    def post(self,request):

        user = CustomUserModel.objects.get(username=request.user)

        form = UserUpdateForm(request.POST,instance=user)

        if form.is_valid():

            form.save()

            return redirect("user_profile")

class ResetPasswordView(View):

    def get(self,request):

        form = CurrentPassword

        return render(request,"current_password.html",{"form":form})
    
    def post(self,request):

        form = CurrentPassword(request.POST)

        if form.is_valid():

            password = form.cleaned_data.get("current_password")

            username = request.user

            user_obj = authenticate(request,username=username,password=password)

            if user_obj:

                return redirect("change_password")
            
            else:

                return redirect("current_password")
            
class ChangePasswordView(View):

    def get(self,request):

        form = NewPasswordForm1

        return render(request,"change_password.html",{"form":form})
    
    def post(self,request):

        form = NewPasswordForm1(request.POST)

        if form.is_valid():

            new_password = form.cleaned_data.get("new_password")

            confirm_password = form.cleaned_data.get("confirm_password")

            if new_password == confirm_password:

                user_obj = CustomUserModel.objects.get(username = request.user)

                user_obj.set_password(new_password)

                user_obj.save()

                return redirect("login")
            
            else:

                return redirect("change_password")

@method_decorator(login_required,name="dispatch")       
class UsersListView(View):

    def get(self,request):

        users = CustomUserModel.objects.all()

        admin = CustomUserModel.objects.get(username = "admin")

        profiles = [request.user,admin]

        return render(request,"users_list.html",{"users":users,"profiles":profiles})

@method_decorator(login_required,name="dispatch")   
class UserInfoView(View):

    def get(self,request,**kwargs):

        id = kwargs.get("id")

        following = FollowingModel.objects.filter(user_obj = id)

        follower = FollowingModel.objects.filter(following_id = id )

        if following:

         total = following.count()

        else:

            total = 0

        if follower:

            count = follower.count()

        else:

            count = 0

        details = CustomUserModel.objects.get(id = id)

        is_following = FollowingModel.objects.filter(user_obj = request.user,following_id = id)

        watchlist_id = WatchlistModel.objects.get(user_id = id)

        watchlist = WatchlistItems.objects.filter(watchlist_id = watchlist_id,watch_status = True)

        review_id = ReviewModel.objects.get(user_id = id)

        reviews = ReviewItems.objects.filter(review_id = review_id)

        return render(request,"user_info.html",{"details":details,"is_following":is_following,"total":total,
                                                "count":count,"watchlist" : watchlist, "reviews" : reviews})
    
class FollowingView(View):

    def get(self,request,**kwargs):

        id = kwargs.get("id")

        another_user = CustomUserModel.objects.get(id = id)

        user = request.user

        FollowingModel.objects.create(following_id = another_user,user_obj = user)

        return redirect("user_info",id = id)
    
class FollowingRemovalView(View):

    def get(self,request,**kwargs):

        user = request.user

        id = kwargs.get("id")

        FollowingModel.objects.get(following_id = id,user_obj = user ).delete()

        return redirect("user_info",id=id)

class UserFollowingView(View):

    def get(self,request):

        user =request.user

        details = FollowingModel.objects.filter(user_obj = user)

        return render(request,"user_following_list.html",{"details":details})

class UserFollowersView(View):

    def get(self,request):

        user =request.user

        details = FollowingModel.objects.filter(following_id = user)

        return render(request,"user_follower_list.html",{"details":details})

class FollowingListRemovalView(View):

    def get(self,request,**kwargs):

        user = request.user

        id = kwargs.get("id")

        FollowingModel.objects.get(following_id = id,user_obj = user ).delete()

        return redirect("user_following_list")

class FollowersListRemovalView(View):

    def get(self,request,**kwargs):

        user = request.user

        id = kwargs.get("id")

        FollowingModel.objects.get(following_id = user,user_obj = id ).delete()

        return redirect("user_followers_list")

class BrowseFollowersView(View):

    def get(self,request,**kwargs):

        id = kwargs.get("id")

        current_user = request.user

        user = CustomUserModel.objects.get(id = id )

        details = FollowingModel.objects.filter(following_id = id)

        return render(request,"browse_follower.html",{"details":details,"user":user,"current_user":current_user})
    
class BrowseFollowingView(View):

    def get(self,request,**kwargs):

        id = kwargs.get("id")

        user = CustomUserModel.objects.get(id = id )

        current_user = request.user

        details = FollowingModel.objects.filter(user_obj = id)

        return render(request,"browse_following.html",{"details":details,"user":user,"current_user":current_user})


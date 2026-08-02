from django.shortcuts import render,redirect

from django.contrib.auth import login,logout,authenticate

from myapp.models import *

from movies.models import *

from myapp.forms import *

from django.conf import settings

from django.views.generic import View

from rest_framework_simplejwt.tokens import RefreshToken

import random

# from django.core.mail import send_mail

from django.utils.decorators import method_decorator

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

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

          # send_mail(
          #   subject="OTP FOR SIGNUP",
          #   message=str(otp),
          #   from_email=settings.EMAIL_HOST_USER,
          #   recipient_list=[email],
          #   fail_silently=False,
          # )

          return redirect("otpverify")

        return render(request, "signup.html", {"form": form}) 

class RegisterResendOtpView(View):
    def get(self,request):
        email = request.session.get("email")    
        if not email:
            messages.error(request, 'Session expired. Please register again.')
            return redirect("signup")
        otp = random.randint(1000,9999)
        print(otp)
        request.session["otp"] = str(otp)
        request.session["email"] = email

        # send_mail(
        #   subject="OTP FOR SIGNUP",
        #   message=str(otp),
        #   from_email=settings.EMAIL_HOST_USER,
        #   recipient_list=[email],
        #   fail_silently=False,
        # )

        messages.success(request, f'A new OTP has been sent to {email}')
        return redirect("otpverify")

class CinelistHomeView(View):

    def get(self,request):

        return render(request,"cinelist_home.html")
    
class IntroView(View):

    def get(self,request):

        return render(request,"home.html")
        
class OtpVerifyView(View):

    def get(self,request):

        form = OtpVerifyForm()

        return render(request,"otpverify.html",{"form":form})
    
    def post(self,request):

        form = OtpVerifyForm(request.POST)

        if form.is_valid():

            entered_otp = str(form.cleaned_data.get("otp"))

            generated_otp = str(request.session.get("otp"))

            # 0000 is a master bypass OTP for testing
            if entered_otp == generated_otp or entered_otp == "0000":

                username = request.session.get("username")

                password = request.session.get("password")

                email = request.session.get("email")

                phone_number = request.session.get("phone_number")

                user = CustomUserModel.objects.create_user(username=username,password=password,email=email,phone_number=phone_number)

                WishlistModel.objects.create(user_id = user)

                WatchlistModel.objects.create(user_id = user)
                ReviewModel.objects.create(user_id = user)

                login(request,user)

                for key in ["otp", "email", "username", "password", "phone_number"]:
                    request.session.pop(key, None)

                return redirect("cinelist_home")
            
            else:
                messages.error(request, 'Invalid OTP. Please check and try again.')
                return redirect("otpverify")

        return render(request, "otpverify.html", {"form": form})

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username").lower()
            password = form.cleaned_data.get("password")
            user_obj = authenticate(request, username=username, password=password)

            if user_obj:
                login(request, user_obj)
                refresh = RefreshToken.for_user(user_obj)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                response = redirect("cinelist_home")

                response.set_cookie('access_token', access_token, httponly=True, samesite='Lax')
                response.set_cookie('refresh_token', refresh_token, httponly=True, samesite='Lax')

                return response
            else:
                form.add_error(None, "Incorrect username or password.")

        return render(request, "login.html", {"form": form})

class ForgetPasswordView(View):

    def get(self, request):
        form = ForgotPasswordForm()
        return render(request, "forgotpswd.html", {"form": form})

    def post(self, request):
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")

            if not CustomUserModel.objects.filter(email=email).exists():
                messages.error(request, "No account found with that email.")
                return render(request, "forgotpswd.html", {"form": form})

            otp = random.randint(1000, 9999)
            request.session["otp"] = str(otp)
            request.session["email"] = email

            # send_mail(
            #   subject="OTP FOR PASSWORD RESET",
            #   message=str(otp),
            #   from_email=settings.EMAIL_HOST_USER,
            #   recipient_list=[email],
            #   fail_silently=False,
            # )

            print(otp)
            return redirect("pswdotp")
        else:
            return render(request, "forgotpswd.html", {"form": form})


class ForgotPswdResendOtpView(View):

    def get(self, request):
        email = request.session.get("email")
        if not email:
            messages.error(request, "Session expired. Please try again.")
            return redirect("forgotpswd")
        otp = random.randint(1000, 9999)
        request.session["otp"] = str(otp)

        # send_mail(
        #   subject="OTP FOR PASSWORD RESET",
        #   message=str(otp),
        #   from_email=settings.EMAIL_HOST_USER,
        #   recipient_list=[email],
        #   fail_silently=False,
        # )

        print(otp)
        messages.success(request, f"A new OTP has been sent to {email}.")
        return redirect("pswdotp")


class ForgotOtpVerifyView(View):

    def get(self, request):
        form = OtpVerifyForm()
        return render(request, "pswdotp.html", {"form": form})

    def post(self, request):
        form = OtpVerifyForm(request.POST)
        if form.is_valid():
            entered_otp = str(form.cleaned_data.get("otp"))
            generated_otp = request.session.get("otp")

            # 0000 is a master bypass OTP for testing
            if entered_otp == generated_otp or entered_otp == "0000":
                request.session.pop("otp", None)
                return redirect("newpswd")
            else:
                messages.error(request, "Invalid OTP. Please check and try again.")
                return redirect("pswdotp")


class NewPasswordView(View):

    def get(self, request):
        form = NewPasswordForm()
        return render(request, "new_password.html", {"form": form})

    def post(self, request):
        form = NewPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get("new_password")
            confirm_password = form.cleaned_data.get("confirm_password")

            if new_password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return render(request, "new_password.html", {"form": form})

            email = request.session.get("email")
            if not email:
                messages.error(request, "Session expired. Please try again.")
                return redirect("forgotpswd")

            try:
                user_obj = CustomUserModel.objects.get(email=email)
                user_obj.set_password(new_password)
                user_obj.save()
                request.session.pop("email", None)
                messages.success(request, "Password reset successful. Please log in.")
                return redirect("login")
            except CustomUserModel.DoesNotExist:
                messages.error(request, "No account found. Please try again.")
                return redirect("forgotpswd")

        return render(request, "new_password.html", {"form": form})

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
    
@method_decorator(login_required, name="dispatch")
class LogoutView(View):
    def get(self, request):
        logout(request)
        response = redirect("login")

        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response

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

        is_following_user = FollowingModel.objects.filter(user_obj = request.user,following_id = id).exists()

        is_following_back = FollowingModel.objects.filter(user_obj = id, following_id = request.user).exists()

        watchlist_id = WatchlistModel.objects.get(user_id = id)

        watchlist = WatchlistItems.objects.filter(watchlist_id = watchlist_id,watch_status = True)

        review_id = ReviewModel.objects.get(user_id = id)

        reviews = ReviewItems.objects.filter(review_id = review_id)

        follow_request = FollowRequestModel.objects.filter(sender=details,receiver=request.user).first()

        follow_back_request = FollowRequestModel.objects.filter(sender=request.user,receiver=details).first()

        return render(request,"user_info.html",{"details":details,"is_following_user":is_following_user,"is_following_back":is_following_back,"total":total, "friends" : is_following_user,
                                                "count":count,"watchlist" : watchlist, "reviews" : reviews, "follow_request" : follow_request, "follow_back_request" : follow_back_request})
    
class FollowingView(View):
    def get(self,request,**kwargs):
        id = kwargs.get("id")
        another_user = CustomUserModel.objects.get(id = id)
        user = request.user
        if another_user.is_private :
            already_requested = FollowRequestModel.objects.filter(sender=user,receiver=another_user).exists()
            if not already_requested:
             FollowRequestModel.objects.create(sender=user, receiver=another_user)
             NotificationModel.objects.create(
                    sender=user,
                    receiver=another_user,
                    message="sent a follow request"
                )
        elif not another_user.is_private:
                NotificationModel.objects.create(
                       sender=user,
                       receiver=another_user,
                       message="started following you"
                   )
                FollowingModel.objects.get_or_create(following_id = another_user,user_obj = user)
            
        return redirect("user_info",id = id)

class NotificationView(View):
    def get(self,request):
        NotificationModel.objects.filter(
            receiver=request.user,
            is_read=False
        ).update(is_read=True)
        return render(request,"notifications.html")

class AcceptrequestView(View):
    def post(self,request,**kwargs):
        user = request.user
        id = kwargs.get("id")
        notification = NotificationModel.objects.get(sender = id, receiver = user)
        FollowingModel.objects.create(following_id = user,user_obj = notification.sender)
        follow_request = FollowRequestModel.objects.get(sender = id, receiver =user)
        follow_request.accept = True
        follow_request.save()
        notification.delete()
        return redirect("user_info",id)

class RejectrequestView(View):
    def post(self,request,**kwargs):
        id = kwargs.get("id")
        user = request.user
        notification = NotificationModel.objects.filter(sender = id, receiver = user)
        follow_request = FollowRequestModel.objects.filter(sender = id, receiver = user)
        follow_request.delete()
        if notification:
         notification.delete()
        return redirect("user_info",id)
    
class DeleteNotificationView(View):
    def post(self, request, **kwargs):
        id = kwargs.get("id")
        NotificationModel.objects.filter(id=id, receiver=request.user).delete()
        return redirect(request.META.get('HTTP_REFERER', '/'))

class MarkNotificationsReadView(LoginRequiredMixin, View):
    def post(self, request):
        NotificationModel.objects.filter(
            receiver=request.user,
            is_read=False
        ).update(is_read=True)
        return JsonResponse({'status': 'ok'})

    def handle_no_permission(self):
        return JsonResponse({'status': 'error'}, status=401)

class FollowingRemovalView(View):

    def get(self,request,**kwargs):
        user = request.user
        id = kwargs.get("id")
        another_user = CustomUserModel.objects.get(id=id)
        FollowingModel.objects.get(following_id = id,user_obj = user ).delete()
        FollowRequestModel.objects.filter(sender=user, receiver=another_user).delete()
        NotificationModel.objects.filter(sender=user, receiver=another_user).delete()

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

class UpdateProfilePictureView(LoginRequiredMixin, View):

     def post(self, request):
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile picture updated successfully.")
        else:
            messages.error(request, "Failed to update profile picture.")
        return redirect("user_profile")

class DeleteProfilePictureView(LoginRequiredMixin, View):

    def post(self, request):
        user = request.user
        if user.profile_picture:
            user.profile_picture.delete(save=True)
            messages.success(request, "Profile picture removed.")
        else:
            messages.error(request, "No profile picture to remove.")
        return redirect("user_profile")

class ToggleAcoountPrivacyView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        make_private = request.POST.get('is_private') == '1'
        password = request.POST.get('password', '')

        if make_private:
            if not request.user.check_password(password):
                return JsonResponse({'success': False, 'error': 'Incorrect password'})

        request.user.is_private = make_private
        request.user.save()

        return JsonResponse({'success': True})

    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({'success': False, 'error': 'Invalid method'}, status=405)

class DeleteUserAccountView(View):
    def post(self, request, **kwargs):
        user = request.user
        password = request.POST.get('password', '')

        if not user.check_password(password):
            return JsonResponse({'success': False, 'error': 'Incorrect password'})
        logout(request)
        user.delete()
        return JsonResponse({'success': True, 'redirect': '/'})
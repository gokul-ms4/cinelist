"""
URL configuration for cinelist2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from myapp.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path("movies/",include("movies.urls")),
    path("user/signup/",UserRegisterView.as_view(),name="signup"),
    path("user/register_resend_otp/",RegisterResendOtpView.as_view(),name = "register_resend_otp"),
    path("user/otpverify/",OtpVerifyView.as_view(),name="otpverify"),
    path("user/login/",LoginView.as_view(),name="login"),
    path('',IntroView.as_view()),
    path('intro/', IntroView.as_view(), name="intro"),
    path("user/forgot_password/",ForgetPasswordView.as_view(),name="forgotpswd"),
    path("user/password_resend_otp/",ForgotPswdResendOtpView.as_view(),name = "pswdresendotp"),
    path("user/new_password/",NewPasswordView.as_view(),name="newpswd"),
    path("user/password_otp_verify/",ForgotOtpVerifyView.as_view(),name="pswdotp"),
    path("user_profile/",UserProfileView.as_view(),name="user_profile"),
    path("user/logout/",LogoutView.as_view(), name="logout"),
    path("user/update/",UserUpdateView.as_view(),name="update"),
    path("user/current_password/",ResetPasswordView.as_view(), name="current_password"),
    path("user/change_password/",ChangePasswordView.as_view(),name="change_password"),
    path("users_list/",UsersListView.as_view(),name="users"),
    path("user_info/<int:id>",UserInfoView.as_view(),name="user_info"),
    path("follower/<int:id>",FollowingView.as_view(),name="follower"),
    path("followers_remove/<int:id>",FollowingRemovalView.as_view(),name="following_removal"),
    path("user_following_list/",UserFollowingView.as_view(),name="user_following_list"),
    path("user_followers_list/",UserFollowersView.as_view(),name="user_followers_list"),
    path("following_list_removal/<int:id>",FollowingListRemovalView.as_view(),name="following_list_removal"),
    path("followers_list_removal/<int:id>",FollowersListRemovalView.as_view(),name="followers_list_removal"),
    path("browse_follower/<int:id>",BrowseFollowersView.as_view(),name="browse_follower"),
    path("browse_following/<int:id>",BrowseFollowingView.as_view(),name="browse_following"),
    path('user/update_profile_picture/', UpdateProfilePictureView.as_view(), name='update_profile_picture'),
    path('user/delete_profile_picture/', DeleteProfilePictureView.as_view(), name='delete_profile_picture'),

    path("user/notification/",NotificationView.as_view(),name="notification"),
    path("user/accept_request/<int:id>",AcceptrequestView.as_view(),name="accept_request"),
    path("user/reject_request/<int:id>", RejectrequestView.as_view(),name="reject_request"),
    path("user/delete_notification/<int:id>",DeleteNotificationView.as_view(),name="delete_notification"),
    path('notifications/mark-read/', MarkNotificationsReadView.as_view(), name='mark_notifications_read'),
    path('user/toggle_private_account',ToggleAcoountPrivacyView.as_view(),name='toggle_private_account'),

    path('delete_account/',DeleteUserAccountView.as_view(),name="delete_account")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

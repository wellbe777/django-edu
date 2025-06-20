from django.urls import path, re_path
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView
from dj_rest_auth.views import LoginView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('verify-email/', VerifyEmailView.as_view(), name='rest_verify_email'),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(), name='account_email_verification_sent'),
]


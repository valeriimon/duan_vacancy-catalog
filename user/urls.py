from django.urls import path
from .views import SigninView, SignupView, SignoutView, SignupCompanyView

app_name = 'user'

urlpatterns = [
    path('sign-in/', SigninView.as_view(), name='sign-in'),
    path('sign-up/', SignupView.as_view(), name='sign-up'),
    path('company-sign-up/', SignupCompanyView.as_view(), name='company-sign-up'),
    path('sign-out/', SignoutView.as_view(), name='sign-out'),
]
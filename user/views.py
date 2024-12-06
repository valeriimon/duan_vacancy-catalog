from django.http import HttpRequest
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.views.generic import View
from .models import User

# Create your views here.
class SignUpView(View):
    def post(self, request: HttpRequest):
        email = request.POST.get('email')
        password = request.POST.get('password')
        User.objects.create_user('', email, password)
        return


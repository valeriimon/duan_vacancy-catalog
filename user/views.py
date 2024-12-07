from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.views.generic import View
from .models import User

# Create your views here.
class SigninView(View):
    def post(self, request: HttpRequest):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username = email, password = password)
        
        if user is None:
            return render('user/sign-in.html', {
                'error': 'Unauthorized'
            })

        return redirect('main:home')

    def get(self, request: HttpRequest):
        return render(request, 'user/sign-in.html')


class SignupView(View):
    def post(self, request: HttpRequest):
        pass

    def get(self, request: HttpRequest):
        return render(request, 'user/sign-up.html')


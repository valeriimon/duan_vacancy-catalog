from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.urls import reverse

from utils import Utils
from .forms import SigninForm, SignupForm, CompanyForm
from .models import User, Company, UserRole


# Create your views here.
class SigninView(View):
    def post(self, request: HttpRequest):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username = email, password = password)
        if user is None:
            return render('user/sign-in.html', Utils.html_context(
            request,
            context={
                'errors': 'Unauthorized'
            }
        ))

        login(request, user)
        return redirect('main:home')

    def get(self, request: HttpRequest):
        return render(request, 'user/sign-in.html', Utils.html_context(
            request,
            context={
                'form': SigninForm()
            }
        ))


class SignupView(View):
    template_name = 'user/sign-up.html'

    def post(self, request: HttpRequest):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.save()

            user.assign_role(UserRole.JOB_SEEKER)

            login(request, user)
            return redirect('main:home')

        return render(request, 'user/sign-up.html', Utils.html_context(
            request,
            context={
                'form': form,
                'errors': form.errors
            }
        ))

    def get(self, request: HttpRequest):
        return render(request, 'user/sign-up.html', Utils.html_context(
            request,
            context={
                'form': SignupForm()
            }
        ))

class SignupCompanyView(View):
    def post(self, request: HttpRequest):
        user_form = SignupForm(request.POST, prefix='user')
        company_form = CompanyForm(request.POST, prefix='company')

        if user_form.is_valid() and company_form.is_valid():
            user = user_form.save()
            company = company_form.save(commit=False)

            user.assign_role(UserRole.EMPLOYER)

            company.created_by = user
            company.save()

            login(request, user)
            return redirect('main:home')

        print('errors - ', user_form.errors)
        return render(
            request,
            'user/sign-up-company.html',
            Utils.html_context(
                request,
                context={
                    'user_form': user_form,
                    'company_form': company_form,
                    'user_form_errors': user_form.errors,
                    'company_form_errors': company_form.errors
                }
            )
        )

    def get(self, request: HttpRequest):
        user_form = SignupForm(prefix='user')
        company_form = CompanyForm(prefix='company')
        return render(
            request,
            'user/sign-up-company.html',
            Utils.html_context(
                request,
                context={
                    'user_form': user_form,
                    'company_form': company_form
                }
            )
        )



class SignoutView(View):
    def get(self, request: HttpRequest):
        logout(request)
        return redirect('main:home')


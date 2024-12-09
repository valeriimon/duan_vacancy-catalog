from django.contrib.auth import logout
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views.generic import View

from .models import Resume
from resume.forms import ResumeForm
from utils import Utils


class ResumeView(View):
    def get(self, request: HttpRequest, id: int):
        resume = (
            Resume.objects
                .select_related('position', 'created_by')
                .prefetch_related('skills')
                .get(id=id)
        )

        return render(request, 'resume/view-resume.html', {
            'resume': resume
        })

class ManageResumeView(View):
    def get(self, request: HttpRequest, id: int | None = None):
        auth_action = self.auth_redirect_check()
        if auth_action is not None:
            return auth_action

        form = None
        if id is not None:
            resume = Resume.objects.get(id=id)
            form = ResumeForm(instance=resume)
        else:
            form = ResumeForm(initial={
                'region': request.user.region,
                'email': request.user.email,
                'phone_number': request.user.phone_number
            })

        return render(request, 'resume/manage-resume.html', Utils.html_context(
            request,
            context={
                'resume_id': id,
                'form': form
            }
        ))

    def post(self, request, id: int | None = None):
        auth_action = self.auth_redirect_check()
        if auth_action is not None:
            return auth_action

        if id is None:
            return self.create()

        return self.update(id)

    def create(self):
        form = ResumeForm(self.request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.created_by = self.request.user
            resume.save()
            form.save_m2m()
            print('resume id -- ', resume.id)
            print('resume id2 -- ', resume.pk)
            return self.redirect_to_view(resume.id)

        return render(self.request, 'resume/manage-resume.html', Utils.html_context(
            self.request,
            context={
                'form': form,
                'form_errors': form.errors
            }
        ))

    def update(self, resume_id):
        resume = Resume.objects.get(id=resume_id)
        form = ResumeForm(self.request.POST, instance=resume)
        if form.is_valid():
            resume = form.save()
            return self.redirect_to_view(resume.id)

        return render(self.request, 'resume/manage-resume.html', Utils.html_context(
            self.request,
            context={
                'form': form,
                'resume_id': resume_id,
                'form_errors': form.errors
            }
        ))

    def redirect_to_view(self, resume_id: int):
        return redirect('resume:view', id=resume_id)

    def auth_redirect_check(self):
        if not self.request.user.is_authenticated:
            return redirect('user:sign-in')

        if self.request.user.is_employer():
            logout(self.request, self.request.user)
            return redirect('user:sign-in')

        return None


from http import HTTPStatus
from urllib.parse import urlencode

from django.contrib.auth import logout
from django.db.models import Count, QuerySet, Case, When, Value, BooleanField
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect

from django.views.generic import View, ListView
from user.models import User, UserRole
from main.forms import MainSearchForm
from resume.models import Resume
from resume.forms import ResumeForm
from utils import Utils

def annotate_is_resume_saved_to_user(qs: QuerySet, user) -> QuerySet:
    return qs.annotate(is_saved=Case(
        When(saved_by=user, then=Value(True)),
        default=Value(False),
        output_field=BooleanField(),
    ))

def save_resume_to_user(request: HttpRequest):
    resume_id = request.POST.get('resume_id')
    try:
        resume = Resume.objects.get(id=resume_id)
    except Resume.DoesNotExist:
        return HttpResponseNotFound()

    request.user.saved_resumes.add(resume)
    return HttpResponse(status=HTTPStatus.OK)

def remove_resume_from_saved_to_user(request: HttpRequest, id):
    try:
        resume = Resume.objects.get(id=id)
    except Resume.DoesNotExist:
        return redirect('main:error')

    request.user.saved_resumes.remove(resume)
    return redirect('resume:list-saved')

def saved_resume_list(request: HttpRequest):
    resume_list = list(
        request.user.saved_resumes.annotate(is_saved=Value(value=True, output_field=BooleanField()))
    )

    return render(request, 'resume/saved-resume-list.html', Utils.html_context(
        request,
        context={
            'resume_list': resume_list
        }
    ))

def user_resume_list(request: HttpRequest):
    return render(request, 'resume/user-resume-list.html', Utils.html_context(
        request,
        context={
            'resume_list': list(request.user.my_resumes.all())
        }
    ))

class ResumeListView(ListView):
    model = Resume
    template_name = 'resume/resume-list.html'
    context_object_name = 'result'
    paginate_by = 5
    searhed_total: int

    def get_queryset(self):
        search_form = MainSearchForm(self.request.GET)
        filtered_qs: QuerySet = self.get_filters_qs(
            search_form['position'].value(),
            search_form['region'].value()
        )
        grouped_qs = filtered_qs.values('created_by').annotate(resumes_count=Count('id'))
        resume_list = []
        for group in grouped_qs:
            user_id = group['created_by']

            resume = filtered_qs.filter(created_by__pk=user_id).first()
            other_resumes = list(Resume.objects
                .filter(created_by__pk=user_id)
                .exclude(id=resume.id))

            resume_list.append({
                'other_resumes': other_resumes,
                'resume': resume,
            })

        self.searhed_total = len(resume_list)
        return resume_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_users = User.objects.filter(groups__name=UserRole.JOB_SEEKER).count()
        total_resumes = Resume.objects.count()

        base_context = Utils.html_context(self.request, context={
            'total_users': total_users,
            'total_resumes': total_resumes,
            'searched_total': self.searhed_total,
            'search_form': MainSearchForm(self.request.GET, initial={
                'region': 'dp'
            }),
            'search_query': self.get_search_query(),
            'save_resume_btn': self.request.user.is_authenticated and self.request.user.is_employer(),
            'show_subheader': True
        })

        return {
            **context,
            **base_context
        }

    def get_filters_qs(self, position, region):
        filtered_qs = Resume.objects.filter(
                position__title__icontains=position,
                region=region
            )

        if self.request.user.is_authenticated:
            filtered_qs = annotate_is_resume_saved_to_user(filtered_qs, self.request.user)

        return filtered_qs

    def get_search_query(self):
        form = MainSearchForm(self.request.GET)
        if form.is_valid():
            return urlencode(form.cleaned_data)
        return ''

class ResumeView(View):
    def get(self, request: HttpRequest, id: int):
        try:
            resume_qs = (
                Resume.objects
                .select_related('position', 'created_by')
                .prefetch_related('skills')
            )

            resume = annotate_is_resume_saved_to_user(resume_qs, request.user).get(id=id)
        except Resume.DoesNotExist:
            return redirect('main:error')

        # If the user is not requesting their own resume,
        # query other user's resumes
        if request.user.id != resume.created_by:
            other_resumes = self.get_user_other_resumes(resume.created_by.id, resume.id)


        parent_template = 'main/base-employer.html' if request.user.is_employer() else 'main/base-job-seeker.html'
        return render(request, 'resume/view-resume.html', Utils.html_context(
            request,
            context={
                'resume': resume,
                'other_resumes': other_resumes,
                'is_employer': request.user.is_employer(),
                'parent_template': parent_template
            }
        ))

    def get_user_other_resumes(self, user_id, resume_id):
        filtered_qs = (Resume.objects
                    .filter(created_by__pk=user_id)
                    .exclude(id=resume_id)
                    .select_related('position')
                )

        if self.request.user.is_authenticated:
            filtered_qs = annotate_is_resume_saved_to_user(filtered_qs, self.request.user)

        return filtered_qs

class ManageResumeView(View):
    def get(self, request: HttpRequest, id: int | None = None):
        auth_action = self.auth_redirect_check()
        if auth_action is not None:
            return auth_action

        form = None
        if id is not None:
            try:
                resume = Resume.objects.get(id=id)
                form = ResumeForm(instance=resume)
            except Resume.DoesNotExist:
                return redirect('main:error')

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
            logout(self.request)
            return redirect('user:sign-in')

        return None


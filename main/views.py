from django.http import HttpRequest
from django.shortcuts import render, redirect
from utils import Utils
from dal import autocomplete
from .models import JobPosition, JobSkill


def index_route(request: HttpRequest):
    print('user', request.user)
    print('is auth -- ', request.user.is_authenticated)
    if request.user.is_authenticated and request.user.is_employer():
        return redirect('main:home-employer')

    return render(request, 'main/index-job-seeker.html', Utils.html_context(request))

def employer_index_route(request: HttpRequest):
    return render(request, 'main/index-employer.html', Utils.html_context(request))


class JobPositionAutocompleteView(autocomplete.Select2QuerySetView):
    model = JobPosition
    create_field = 'title'

    def has_add_permission(self, request):
        return True

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return self.model.objects.none()

        qs = self.model.objects.all()

        if self.q:
            qs = qs.filter(title__icontains=self.q)
        return qs

    def get_result_label(self, item):
        return item.title


class JobSkillAutocompleteView(autocomplete.Select2QuerySetView):
    create_field = 'value'
    model = JobSkill

    def has_add_permission(self, request):
        return True

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return JobSkill.objects.none()

        qs = JobSkill.objects.all()

        if self.q:
            qs = qs.filter(value__icontains=self.q)
        return qs

    def get_result_label(self, item):
        return item.value



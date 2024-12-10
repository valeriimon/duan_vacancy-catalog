from django.http import HttpRequest
from django.shortcuts import render, redirect
from utils import Utils
from dal import autocomplete
from .models import JobPosition, JobSkill


def index_route(request: HttpRequest):
    if request.user.is_authenticated and request.user.is_employer():
        return redirect('resume:list')

    return redirect('vacancy:list')

def employer_index_route(request: HttpRequest):
    return render(request, 'main/base-employer.html', Utils.html_context(request))

def error_route(request):
    return render(request, 'main/error.html')


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



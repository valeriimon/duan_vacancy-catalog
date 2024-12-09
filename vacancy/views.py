from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic import View

class VacancyView(View):
    def get(self, request: HttpRequest):
        return render(request, 'vacancy/view-vacancy.html')

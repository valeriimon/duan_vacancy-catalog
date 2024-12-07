from django.http import HttpRequest
from django.shortcuts import render

from main.forms import SearchVacancyForm


def index_route(request: HttpRequest):
    print('user', dir(request.user))
    print('is auth -- ', request.user.is_authenticated)
    return render(request, 'main/index.html', {
        'user': request.user
    })

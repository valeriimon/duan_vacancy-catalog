from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index_route, name='home'),

    path('autocomplete/jobposition/', views.JobPositionAutocompleteView.as_view(), name='jobposition-autocomplete'),
    path('autocomplete/jobskill/', views.JobSkillAutocompleteView.as_view(), name='jobskill-autocomplete'),

    path('error', views.error_route, name='error'),
]
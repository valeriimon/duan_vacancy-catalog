from django.urls import path
from . import views
from .models import JobSkill

app_name = 'main'

urlpatterns = [
    path('', views.index_route, name='home'),
    path('employer', views.employer_index_route, name='home-employer'),

    path('autocomplete/jobposition/', views.JobPositionAutocompleteView.as_view(), name='jobposition-autocomplete'),
    path('autocomplete/jobskill/', views.JobSkillAutocompleteView.as_view(), name='jobskill-autocomplete'),
]
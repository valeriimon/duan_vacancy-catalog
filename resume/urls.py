from django.urls import path
from .views import ResumeView, ManageResumeView

app_name = 'resume'

urlpatterns = [
    path('view/<int:id>/', ResumeView.as_view(), name = 'view'),
    path('manage/', ManageResumeView.as_view(), name = 'manage'),
    path('manage/<int:id>/', ManageResumeView.as_view(), name = 'manage'),
]
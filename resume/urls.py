from django.urls import path
from .views import (
    ResumeView,
    ManageResumeView,
    ResumeListView,
    save_resume_to_user,
    remove_resume_from_saved_to_user,
    saved_resume_list,
    user_resume_list,
)

app_name = 'resume'

urlpatterns = [
    path('list/', ResumeListView.as_view(), name='list'),
    path('list/saved/', saved_resume_list, name='list-saved'),
    path('list/my', user_resume_list, name='list-user'),

    path('view/<int:id>/', ResumeView.as_view(), name = 'view'),

    path('manage/', ManageResumeView.as_view(), name = 'manage'),
    path('manage/<int:id>/', ManageResumeView.as_view(), name = 'manage'),

    path('remove-resume-from-saved-to-user/<int:id>/', remove_resume_from_saved_to_user, name = 'remove-saved'),
    path('save-resume-to-user/', save_resume_to_user, name='save-resume-to-user')
]
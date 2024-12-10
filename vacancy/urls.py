from django.urls import path
from .views import (
    VacancyView,
    VacancyListView,
    ManageVacancyView,
    save_vacancy_to_user,
    saved_vacancy_list,
    user_vacancy_list,
    remove_vacancy_from_saved_to_user,
)

app_name = 'vacancy'

urlpatterns = [
    path('list/', VacancyListView.as_view(), name='list'),
    path('list/saved/', saved_vacancy_list, name='list-saved'),
    path('list/my', user_vacancy_list, name='list-user'),

    path('view/<int:id>/', VacancyView.as_view(), name = 'view'),
    path('manage/', ManageVacancyView.as_view(), name = 'manage'),
    path('manage/<int:id>/', ManageVacancyView.as_view(), name = 'manage'),

    path('remove-vacancy-from-saved-to-user/<int:id>/', remove_vacancy_from_saved_to_user, name = 'remove-saved'),
    path('save-vacancy-to-user/', save_vacancy_to_user, name='save-vacancy-to-user')
]
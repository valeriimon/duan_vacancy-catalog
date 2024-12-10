from http import HTTPStatus

from django.contrib.auth import logout
from django.db.models import QuerySet, Q, Case, When, Value, BooleanField, Count
from django.http import HttpRequest, HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View, ListView

from utils import Utils
from vacancy.forms import VacancySearchForm, VacancyForm
from vacancy.models import Vacancy
from user.models import User, UserRole


def annotate_is_vacancy_saved_to_user(qs: QuerySet, user) -> QuerySet:
    return qs.annotate(is_saved=Case(
        When(saved_by=user, then=Value(True)),
        default=Value(False),
        output_field=BooleanField(),
    ))

def save_vacancy_to_user(request: HttpRequest):
    vacancy_id = request.POST.get('vacancy_id')
    try:
        vacancy = Vacancy.objects.get(id=vacancy_id)
    except Vacancy.DoesNotExist:
        return HttpResponseNotFound()

    request.user.saved_vacancies.add(vacancy)
    return HttpResponse(status=HTTPStatus.OK)

def remove_vacancy_from_saved_to_user(request: HttpRequest, id):
    try:
        vacancy = Vacancy.objects.get(id=id)
    except Vacancy.DoesNotExist:
        return redirect('main:error')

    request.user.saved_vacancies.remove(vacancy)
    return redirect('vacancy:list-saved')

def saved_vacancy_list(request: HttpRequest):
    vacancy_list = list(
        request.user.saved_vacancies.annotate(is_saved=Value(value=True, output_field=BooleanField()))
    )

    return render(request, 'vacancy/saved-vacancy-list.html', Utils.html_context(
        request,
        context={
            'vacancy_list': vacancy_list
        }
    ))

def user_vacancy_list(request: HttpRequest):
    return render(request, 'vacancy/user-vacancy-list.html', Utils.html_context(
        request,
        context={
            'vacancy_list': list(request.user.my_vacancies.all())
        }
    ))

class VacancyListView(ListView):
    model = Vacancy
    template_name = 'vacancy/vacancy-list.html'
    context_object_name = 'result'
    paginate_by = 10

    def get_queryset(self):
        search_form = VacancySearchForm(self.request.GET)
        filtered_qs: QuerySet = self.get_filters_qs(
            search_form['position'].value(),
            search_form['region'].value()
        )
        grouped_qs = filtered_qs.values('created_by').annotate(vacancy_count=Count('id'))
        vacancy_list = []
        for group in grouped_qs:
            user_id = group['created_by']

            vacancy = filtered_qs.filter(created_by__pk=user_id).first()
            other_vacancies= list(Vacancy.objects
                .filter(created_by__pk=user_id)
                .exclude(id=vacancy.id))

            vacancy_list.append({
                'other_vacancies': other_vacancies,
                'vacancy': vacancy
            })

        return vacancy_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_vacancies = Vacancy.objects.count()
        base_context = Utils.html_context(self.request, context={
            'total_vacancies': total_vacancies,
            'search_form': VacancySearchForm(self.request.GET, initial={
                'region': 'dp'
            }),
            'save_vacancy_btn': self.request.user.is_authenticated and self.request.user.is_job_seeker(),
            'show_subheader': True
        })

        return {
            **context,
            **base_context
        }


    def get_filters_qs(self, position, region):
        filtered_qs = Vacancy.objects.filter(
                Q(position__title__icontains=position) | Q(created_by__company__name=position),
                created_by__company__region=region
            )

        if self.request.user.is_authenticated:
            filtered_qs = annotate_is_vacancy_saved_to_user(filtered_qs, self.request.user)

        return filtered_qs

class VacancyView(View):
    def get(self, request: HttpRequest, id: int):
        try:
            vacancy_qs = (
                Vacancy.objects
                .select_related('position', 'created_by', 'created_by__company')
                .prefetch_related('skills')
            )

            vacancy = annotate_is_vacancy_saved_to_user(vacancy_qs, request.user).get(id=id)
        except Vacancy.DoesNotExist:
            return redirect('main:error')

        # If the user is not requesting their own vacancy,
        # query other user's vacancies
        if request.user.id != vacancy.created_by:
            other_vacancies = self.get_user_other_vacancies(vacancy.created_by.id, vacancy.id)


        parent_template = 'main/base-employer.html' if request.user.is_employer() else 'main/base-job-seeker.html'
        return render(request, 'vacancy/view-vacancy.html', Utils.html_context(
            request,
            context={
                'vacancy': vacancy,
                'other_vacancies': other_vacancies,
                'is_job_seeker': request.user.is_job_seeker(),
                'parent_template': parent_template
            }
        ))

    def get_user_other_vacancies(self, user_id, vacancy_id):
        filtered_qs = (Vacancy.objects
                    .filter(created_by__pk=user_id)
                    .exclude(id=vacancy_id)
                    .select_related('position')
                )

        if self.request.user.is_authenticated:
            filtered_qs = annotate_is_vacancy_saved_to_user(filtered_qs, self.request.user)

        return filtered_qs

class ManageVacancyView(View):
    def get(self, request: HttpRequest, id: int | None = None):
        auth_action = self.auth_redirect_check()
        if auth_action is not None:
            return auth_action

        form = None
        if id is not None:
            try:
                vacancy = Vacancy.objects.get(id=id)
                form = VacancyForm(instance=vacancy)
            except Vacancy.DoesNotExist:
                return redirect('main:error')

        else:
            form = VacancyForm(initial={
                'email': request.user.email,
                'phone_number': request.user.company.phone_number
            })

        return render(request, 'vacancy/manage-vacancy.html', Utils.html_context(
            request,
            context={
                'vacancy_id': id,
                'form': form
            }
        ))

    def post(self, _request, id: int | None = None):
        auth_action = self.auth_redirect_check()
        if auth_action is not None:
            return auth_action

        if id is None:
            return self.create()

        return self.update(id)

    def create(self):
        form = VacancyForm(self.request.POST)
        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.created_by = self.request.user
            vacancy.save()
            form.save_m2m()
            return self.redirect_to_view(vacancy.id)

        return render(self.request, 'vacancy/manage-vacancy.html', Utils.html_context(
            self.request,
            context={
                'form': form,
                'form_errors': form.errors
            }
        ))

    def update(self, vacancy_id):
        vacancy = Vacancy.objects.get(id=vacancy_id)
        form = VacancyForm(self.request.POST, instance=vacancy)
        if form.is_valid():
            vacancy = form.save()
            return self.redirect_to_view(vacancy.id)

        return render(self.request, 'vacancy/manage-vacancy.html', Utils.html_context(
            self.request,
            context={
                'form': form,
                'vacancy_id': vacancy_id,
                'form_errors': form.errors
            }
        ))

    def redirect_to_view(self, vacancy_id: int):
        return redirect('vacancy:view', id=vacancy_id)

    def auth_redirect_check(self):
        if not self.request.user.is_authenticated:
            return redirect('user:sign-in')

        if self.request.user.is_job_seeker():
            logout(self.request)
            return redirect('user:sign-in')

        return None

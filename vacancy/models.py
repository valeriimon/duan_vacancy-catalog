from django.db import models

from main.models import JobPosition, JobSkill, CustomBaseManager
from user.models import User, EMPLOYMENT_TYPE
from tinymce.models import HTMLField

# Create your models here.
class Vacancy(models.Model):
    title = models.CharField(max_length=100)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE, null=True)
    salary = models.CharField(max_length=100)
    position = models.ForeignKey(JobPosition, on_delete=models.DO_NOTHING)
    skills = models.ManyToManyField(JobSkill)
    email = models.EmailField()
    phone_number = models.CharField(max_length=100)
    description = HTMLField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_vacancies')

    objects = CustomBaseManager()
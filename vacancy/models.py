from django.db import models

from main.models import JobPosition, JobSkill
from user.models import User
from tinymce.models import HTMLField

# Create your models here.
class Vacancy(models.Model):
    title = models.CharField(max_length=100)
    employment_type = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    position = models.ForeignKey(JobPosition, on_delete=models.DO_NOTHING)
    skills = models.ManyToManyField(JobSkill)
    description = HTMLField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
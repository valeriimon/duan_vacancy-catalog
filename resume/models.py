from django.db import models

from main.models import JobPosition, JobSkill, CustomBaseManager
from user.models import User, REGIONS, EMPLOYMENT_TYPE
from tinymce.models import HTMLField

class Resume(models.Model):
    position = models.ForeignKey(JobPosition, on_delete=models.DO_NOTHING)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE, null=True)
    salary = models.CharField(max_length=100)
    description = HTMLField()
    skills = models.ManyToManyField(JobSkill)
    region = models.CharField('Регіон', max_length=2, choices=REGIONS, null=False)
    phone_number = models.CharField(max_length=100)
    email = models.EmailField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_resumes')

    objects = CustomBaseManager()




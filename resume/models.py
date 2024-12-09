from django.db import models

from main.models import JobPosition, JobSkill
from user.models import User, REGIONS
from tinymce.models import HTMLField

class Resume(models.Model):
    position = models.ForeignKey(JobPosition, on_delete=models.DO_NOTHING)
    description = HTMLField()
    skills = models.ManyToManyField(JobSkill)
    region = models.CharField('Регіон', max_length=2, choices=REGIONS, null=False)
    phone_number = models.CharField(max_length=100)
    email = models.EmailField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)




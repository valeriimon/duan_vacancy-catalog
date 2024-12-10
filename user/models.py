from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from enum import Enum



class UserRole(Enum):
    JOB_SEEKER = 'job_seeker'
    EMPLOYER = 'employer'

REGIONS = [
    ('dp', 'Дніпро'),
    ('kv', 'Київ'),
    ('od', 'Одеса'),
    ('lv', 'Львів')
]

EMPLOYMENT_TYPE = [
    ('full', 'Повна зайнятість'),
    ('part', 'Неповна зайнятість')
]

class User(AbstractUser):
    region = models.CharField(max_length=2, choices=REGIONS, default=REGIONS[0][0])
    auth_complete = models.BooleanField(default=True)
    age = models.IntegerField(blank=True)
    phone_number = models.CharField(max_length=100)

    saved_resumes = models.ManyToManyField('resume.Resume', related_name='saved_by')
    saved_vacancies = models.ManyToManyField('vacancy.Vacancy', related_name='saved_by')

    def assign_role(self, role: UserRole):
        group, created = Group.objects.get_or_create(name=role)
        self.groups.add(group)

    def is_job_seeker(self) -> bool:
        return self.groups.filter(name = UserRole.JOB_SEEKER).exists()

    def is_employer(self) -> bool:
        return self.groups.filter(name = UserRole.EMPLOYER).exists()

class Company(models.Model):
    name = models.CharField(null=False, max_length=100)
    address_text = models.CharField(max_length=100)
    region = models.CharField(max_length=2, choices=REGIONS, default=REGIONS[0][0])
    phone_number = models.CharField(max_length=100)
    employees_count = models.IntegerField()
    created_by = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='company')



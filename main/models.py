from django.db import models
# Create your models here.

class JobPosition(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class JobSkill(models.Model):
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.value




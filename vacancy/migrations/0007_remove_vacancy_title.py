# Generated by Django 4.2.16 on 2024-12-12 08:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vacancy', '0006_alter_vacancy_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vacancy',
            name='title',
        ),
    ]
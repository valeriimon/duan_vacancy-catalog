# Generated by Django 4.2.16 on 2024-12-09 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_age_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='phone_number',
            field=models.CharField(max_length=100),
        ),
    ]

# Generated by Django 4.2.16 on 2024-12-08 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0002_rename_create_by_resume_created_by_resume_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='email',
            field=models.EmailField(default='test@d1.com', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resume',
            name='phone_number',
            field=models.CharField(default='80000000000', max_length=100),
            preserve_default=False,
        ),
    ]

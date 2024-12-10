# Generated by Django 4.2.16 on 2024-12-10 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0006_alter_resume_region'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='region',
            field=models.CharField(choices=[('dp', 'Дніпро'), ('kv', 'Київ'), ('od', 'Одеса'), ('lv', 'Львів')], default='dp', max_length=2),
        ),
    ]

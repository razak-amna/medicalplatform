# Generated by Django 5.1.3 on 2024-12-29 13:34

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicalapp', '0014_remove_appointment_appointment_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='appointment_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
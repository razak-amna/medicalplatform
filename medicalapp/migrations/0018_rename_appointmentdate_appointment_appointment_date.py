# Generated by Django 5.1.4 on 2024-12-30 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medicalapp', '0017_rename_appointment_date_appointment_appointmentdate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='appointmentDate',
            new_name='appointment_date',
        ),
    ]
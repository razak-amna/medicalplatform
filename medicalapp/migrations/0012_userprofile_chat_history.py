# Generated by Django 5.1.3 on 2024-12-29 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicalapp', '0011_userprofile_address_userprofile_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='chat_history',
            field=models.JSONField(blank=True, null=True),
        ),
    ]

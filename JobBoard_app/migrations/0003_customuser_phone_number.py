# Generated by Django 4.2.4 on 2023-08-14 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JobBoard_app', '0002_jobpost_candidate_application'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
# Generated by Django 4.2.4 on 2023-08-16 23:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('JobBoard_app', '0005_jobpost_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('text', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('JobPost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='JobBoard_app.jobpost')),
            ],
        ),
    ]

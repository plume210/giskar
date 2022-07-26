# Generated by Django 4.0.6 on 2022-07-26 08:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('A_and_R', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendar',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calendars', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='availabilities',
            name='calendar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='availabilities', to='A_and_R.calendar'),
        ),
    ]

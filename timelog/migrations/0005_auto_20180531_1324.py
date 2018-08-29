# Generated by Django 2.0.5 on 2018-05-31 13:24

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0002_auto_20180125_2004'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reasons', '0004_auto_20180531_1227'),
        ('timelog', '0004_auto_20180531_1227'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='timelog',
            unique_together={('user', 'reason', 'facility', 'work_start_time', 'work_end_time')},
        ),
    ]

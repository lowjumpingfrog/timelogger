# Generated by Django 2.0.6 on 2018-07-05 11:42

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0002_auto_20180125_2004'),
        ('reasons', '0005_reasons_group'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('timelog', '0015_auto_20180705_1136'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='timelog',
            unique_together={('user', 'reason', 'facility', 'work_start_time', 'work_end_time')},
        ),
    ]

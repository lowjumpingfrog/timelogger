# Generated by Django 2.0.5 on 2018-05-31 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reasons', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reasons',
            name='group',
        ),
        migrations.AddField(
            model_name='reasons',
            name='billable',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 2.0.6 on 2018-07-05 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timelog', '0014_auto_20180705_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timelog',
            name='comment',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Comment'),
        ),
    ]

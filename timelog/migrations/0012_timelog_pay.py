# Generated by Django 2.0.6 on 2018-06-23 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timelog', '0011_remove_timelog_base_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='timelog',
            name='pay',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
# Generated by Django 2.0.5 on 2018-06-02 16:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('work_type', '0002_auto_20180602_1422'),
        ('reasons', '0004_auto_20180531_1227'),
    ]

    operations = [
        migrations.AddField(
            model_name='reasons',
            name='group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='work_type.WorkGroup', verbose_name='Group'),
            preserve_default=False,
        ),
    ]

# Generated by Django 2.0.5 on 2018-06-06 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_type', '0003_auto_20180606_0903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workcategory',
            name='day_flag',
            field=models.CharField(choices=[('wkd', 'Week Day'), ('wkend', 'Week End'), ('hol', 'Holiday'), ('any', 'Any Day')], max_length=6, verbose_name='Day'),
        ),
        migrations.DeleteModel(
            name='WorkDay',
        ),
    ]

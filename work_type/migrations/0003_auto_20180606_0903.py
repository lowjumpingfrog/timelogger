# Generated by Django 2.0.5 on 2018-06-06 09:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('work_type', '0002_auto_20180602_1422'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('wkd', 'Week Day'), ('wkend', 'Week End'), ('hol', 'Holiday')], max_length=125)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-updated', '-timestamp'],
            },
        ),
        migrations.RenameField(
            model_name='workcategory',
            old_name='name',
            new_name='work_category',
        ),
        migrations.RenameField(
            model_name='workgroup',
            old_name='name',
            new_name='group',
        ),
        migrations.AddField(
            model_name='workcategory',
            name='day_flag',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='work_type.WorkDay', verbose_name='Day'),
            preserve_default=False,
        ),
    ]
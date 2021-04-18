# Generated by Django 3.1.7 on 2021-04-13 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_auto_20210412_2141'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentsubject',
            old_name='abs',
            new_name='abs_1',
        ),
        migrations.RenameField(
            model_name='studentsubject',
            old_name='grade',
            new_name='period_1',
        ),
        migrations.AddField(
            model_name='studentsubject',
            name='abs_2',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='studentsubject',
            name='period_2',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='studentsubject',
            name='period_3',
            field=models.IntegerField(default=0),
        ),
    ]
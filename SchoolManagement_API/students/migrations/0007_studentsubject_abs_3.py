# Generated by Django 3.1.7 on 2021-04-13 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0006_auto_20210413_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentsubject',
            name='abs_3',
            field=models.IntegerField(default=0),
        ),
    ]

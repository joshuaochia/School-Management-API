# Generated by Django 3.1.7 on 2021-04-20 03:12

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0019_auto_20210416_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='country',
            field=django_countries.fields.CountryField(default='PH', max_length=2),
        ),
    ]
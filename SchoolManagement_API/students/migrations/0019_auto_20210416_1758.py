# Generated by Django 3.1.7 on 2021-04-16 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0018_auto_20210416_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='sample',
            field=models.FileField(null=True, upload_to='assignment/'),
        ),
    ]

# Generated by Django 3.1.7 on 2021-04-14 01:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0008_auto_20210413_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentsubject',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_sub', to='students.students'),
        ),
    ]

# Generated by Django 3.1.7 on 2021-04-16 01:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0014_auto_20210415_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileassignment',
            name='assignment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assignment_files', to='students.assignment'),
        ),
        migrations.AlterField(
            model_name='fileassignment',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assignment_file', to='students.studentsubject'),
        ),
    ]

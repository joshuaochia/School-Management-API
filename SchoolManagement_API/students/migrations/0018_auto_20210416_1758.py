# Generated by Django 3.1.7 on 2021-04-16 09:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0017_fileproject'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='file',
            new_name='sample',
        ),
        migrations.AddField(
            model_name='assignment',
            name='sample',
            field=models.FileField(null=True, upload_to='project/'),
        ),
        migrations.AddField(
            model_name='project',
            name='files',
            field=models.ManyToManyField(blank=True, through='students.FileProject', to='students.StudentSubject'),
        ),
        migrations.AlterField(
            model_name='fileproject',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_files', to='students.project'),
        ),
    ]

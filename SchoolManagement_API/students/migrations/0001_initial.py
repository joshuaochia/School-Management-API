# Generated by Django 3.2.1 on 2021-05-06 02:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('school', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('dead_line', models.DateTimeField(verbose_name='Dead Line')),
                ('description', models.TextField(max_length=5006)),
                ('sample', models.FileField(null=True, upload_to='assignment/')),
            ],
        ),
        migrations.CreateModel(
            name='FileProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='project/')),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.ImageField(blank=True, null=True, upload_to='student_pic')),
                ('bday', models.DateField(null=True, verbose_name='Birth Day')),
                ('country', django_countries.fields.CountryField(default='PH', max_length=2)),
                ('city', models.CharField(max_length=255, null=True)),
                ('zip_code', models.PositiveSmallIntegerField(null=True, verbose_name='Zip Code')),
                ('sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=55, null=True)),
                ('civil_status', models.CharField(choices=[('Married', 'Married'), ('Single', 'Single')], max_length=55, null=True, verbose_name='Civil Status')),
                ('school_yr', models.CharField(default='2012', max_length=255)),
                ('sem', models.CharField(choices=[('First', 'First'), ('Second', 'Second')], max_length=55)),
                ('slug', models.SlugField(null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='school.courses')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='school.school')),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
            },
        ),
        migrations.CreateModel(
            name='StudentSubject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period_1', models.IntegerField(default=0)),
                ('abs_1', models.IntegerField(default=0)),
                ('period_2', models.IntegerField(default=0)),
                ('abs_2', models.IntegerField(default=0)),
                ('period_3', models.IntegerField(default=0)),
                ('abs_3', models.IntegerField(default=0)),
                ('avg', models.IntegerField(default=0)),
                ('status', models.CharField(choices=[('Passed', 'Passed'), ('Completed', 'Completed'), ('Failed', 'Failed'), ('INC', 'INC')], max_length=255)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_sub', to='students.students')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student', to='school.teachersubject')),
            ],
        ),
        migrations.AddField(
            model_name='students',
            name='subjects',
            field=models.ManyToManyField(through='students.StudentSubject', to='school.TeacherSubject'),
        ),
        migrations.AddField(
            model_name='students',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('dead_line', models.DateTimeField(verbose_name='Dead Line')),
                ('description', models.TextField(max_length=5006)),
                ('sample', models.FileField(null=True, upload_to='project/')),
                ('assign', models.ManyToManyField(related_name='my_project', to='students.StudentSubject', verbose_name='Members')),
                ('files', models.ManyToManyField(blank=True, through='students.FileProject', to='students.StudentSubject')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='school.teachersubject')),
            ],
        ),
        migrations.AddField(
            model_name='fileproject',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_files', to='students.project'),
        ),
        migrations.AddField(
            model_name='fileproject',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_file', to='students.studentsubject'),
        ),
        migrations.CreateModel(
            name='FileAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='assignment/')),
                ('assignment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assignment_files', to='students.assignment')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assignment_file', to='students.studentsubject')),
            ],
        ),
        migrations.AddField(
            model_name='assignment',
            name='assign',
            field=models.ManyToManyField(blank=True, related_name='my_assignment', to='students.StudentSubject', verbose_name='Members'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='files',
            field=models.ManyToManyField(blank=True, through='students.FileAssignment', to='students.StudentSubject'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignment', to='school.teachersubject'),
        ),
    ]

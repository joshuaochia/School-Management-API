# Generated by Django 3.2.1 on 2021-05-06 02:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.CharField(choices=[('BSBA', 'Bachelor of Science in Business'), ('BMS', 'Bachelor of Management Studies'), ('B.Acc', 'Bachelor of Accountancy'), ('BComp', 'Bachelor of Computing'), ('BCompSc', 'Bachelor of Computer Science'), ('BSc IT', 'Bachelor of Science in Information Technology'), ('Minor', 'Minor')], max_length=556)),
                ('major', models.CharField(choices=[('MM', 'Marketing'), ('FM', 'Financial Management'), ('HRDM ', 'Human Resource Development'), ('Minor', 'Minor')], max_length=556)),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Employees',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=255, null=True)),
                ('bday', models.DateField(null=True, verbose_name='Birth Day')),
                ('country', django_countries.fields.CountryField(default='PH', max_length=2)),
                ('city', models.CharField(max_length=255, null=True)),
                ('zip_code', models.PositiveSmallIntegerField(null=True, verbose_name='Zip Code')),
                ('sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=55, null=True)),
                ('civil_status', models.CharField(choices=[('Married', 'Married'), ('Single', 'Single')], default='Single', max_length=55, null=True, verbose_name='Civil Status')),
                ('rate', models.PositiveSmallIntegerField(verbose_name='Daily Rate')),
                ('days_week', models.PositiveSmallIntegerField(verbose_name='Weekly Hrs')),
                ('salary', models.PositiveIntegerField(default=0)),
                ('slug', models.SlugField(null=True)),
                ('is_employee', models.BooleanField(default=True)),
                ('is_teacher', models.BooleanField(default=False)),
                ('is_hr', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee', to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workers', to='school.department')),
            ],
            options={
                'verbose_name': 'Employee',
                'verbose_name_plural': 'Employees',
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.TimeField()),
                ('end', models.TimeField()),
                ('day', models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=55)),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('vision', models.CharField(max_length=255, null=True)),
                ('mission', models.CharField(max_length=255, null=True)),
                ('street', models.CharField(max_length=255, null=True)),
                ('country', django_countries.fields.CountryField(max_length=2, null=True)),
                ('city', models.CharField(max_length=255)),
                ('zip_code', models.PositiveSmallIntegerField(null=True, verbose_name='Zip Code')),
                ('date_funded', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=255, verbose_name='Room Code')),
            ],
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=556)),
                ('code', models.CharField(max_length=55, verbose_name='Subject Code')),
                ('unit', models.PositiveSmallIntegerField()),
                ('lab', models.PositiveSmallIntegerField()),
                ('cost', models.IntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject_course', to='school.courses')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.school')),
            ],
            options={
                'verbose_name': 'Subject',
                'verbose_name_plural': 'Subjects',
            },
        ),
        migrations.CreateModel(
            name='TeacherSubject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.schedule')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.section')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_teacher', to='school.subjects')),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teacher_sub', to='school.employees')),
            ],
        ),
        migrations.CreateModel(
            name='Policies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('policy', models.CharField(max_length=556)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='policies', to='school.school')),
            ],
            options={
                'verbose_name': 'Policie',
                'verbose_name_plural': 'Policies',
            },
        ),
        migrations.AddField(
            model_name='employees',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='school.school'),
        ),
        migrations.AddField(
            model_name='employees',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='e_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='department',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='school.school'),
        ),
        migrations.AddField(
            model_name='courses',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='school.school'),
        ),
    ]

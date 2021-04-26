# Generated by Django 3.1.7 on 2021-04-26 01:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0012_auto_20210422_1130'),
        ('students', '0021_auto_20210423_2246'),
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeLeave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeOT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hrs', models.PositiveIntegerField()),
                ('day', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='SchoolPayedHolidays',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='StudentPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
        migrations.RemoveField(
            model_name='studentbalance',
            name='user',
        ),
        migrations.AddField(
            model_name='employeesalary',
            name='employee',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='employee_salary', to='school.employees'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employeesalary',
            name='salary',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentbalance',
            name='student',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='bal', to='students.students'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentpayment',
            name='balance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_balance', to='finance.studentbalance'),
        ),
        migrations.AddField(
            model_name='employeeot',
            name='salary',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.employeesalary'),
        ),
        migrations.AddField(
            model_name='employeeleave',
            name='salary',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.employeesalary'),
        ),
    ]

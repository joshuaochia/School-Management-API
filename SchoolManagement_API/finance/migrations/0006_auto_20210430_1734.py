# Generated by Django 3.1.7 on 2021-04-30 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0020_auto_20210430_1734'),
        ('finance', '0005_auto_20210429_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeleave',
            name='salary',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leave', to='school.employees'),
        ),
        migrations.AlterField(
            model_name='employeeot',
            name='salary',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='overtime', to='school.employees'),
        ),
        migrations.DeleteModel(
            name='EmployeeSalary',
        ),
    ]

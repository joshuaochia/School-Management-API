# Generated by Django 3.1.7 on 2021-04-29 01:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0018_remove_department_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjects',
            name='school',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='school.school'),
            preserve_default=False,
        ),
    ]

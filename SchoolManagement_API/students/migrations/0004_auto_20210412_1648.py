# Generated by Django 3.1.7 on 2021-04-12 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_auto_20210412_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subjects',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject', to='students.section'),
        ),
    ]

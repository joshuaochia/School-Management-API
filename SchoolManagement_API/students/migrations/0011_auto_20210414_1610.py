# Generated by Django 3.1.7 on 2021-04-14 08:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0010_auto_20210414_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='subject',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='assignment', to='students.subjects'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='subject',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='students.subjects'),
            preserve_default=False,
        ),
    ]
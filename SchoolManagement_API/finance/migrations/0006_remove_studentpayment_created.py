# Generated by Django 3.1.7 on 2021-05-02 02:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0005_auto_20210502_1016'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentpayment',
            name='created',
        ),
    ]

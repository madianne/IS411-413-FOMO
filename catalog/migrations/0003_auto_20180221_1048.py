# Generated by Django 2.0.1 on 2018-02-21 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20180221_1047'),
    ]

    operations = [
        migrations.RenameField(
            model_name='individualproduct',
            old_name='PID',
            new_name='pid',
        ),
        migrations.RenameField(
            model_name='rentalproduct',
            old_name='PID',
            new_name='pid',
        ),
    ]
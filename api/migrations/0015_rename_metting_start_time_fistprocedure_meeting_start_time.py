# Generated by Django 3.2.9 on 2022-06-30 05:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20220630_1302'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fistprocedure',
            old_name='metting_start_time',
            new_name='meeting_start_time',
        ),
    ]

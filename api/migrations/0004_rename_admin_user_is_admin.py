# Generated by Django 3.2.9 on 2022-06-25 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='admin',
            new_name='is_admin',
        ),
    ]

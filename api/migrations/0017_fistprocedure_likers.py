# Generated by Django 3.2.9 on 2022-06-30 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_news'),
    ]

    operations = [
        migrations.AddField(
            model_name='fistprocedure',
            name='likers',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]

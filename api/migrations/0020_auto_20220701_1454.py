# Generated by Django 3.2.9 on 2022-07-01 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_auto_20220630_2210'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='branding',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='comment',
            name='future_proof',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='comment',
            name='market',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='comment',
            name='profitable',
            field=models.FloatField(default=0.0),
        ),
    ]
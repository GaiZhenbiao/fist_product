# Generated by Django 3.2.9 on 2022-07-04 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_product_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='fistprocedure',
            name='commented',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='graph',
            name='ys',
            field=models.CharField(default='2022年第1季度,2022年第2季度,2022年第3季度,2022年第4季度', max_length=1024),
        ),
    ]

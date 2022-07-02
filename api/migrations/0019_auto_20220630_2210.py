# Generated by Django 3.2.9 on 2022-06-30 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_useruploadedfile_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='procedure',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.fistprocedure'),
        ),
        migrations.AlterField(
            model_name='news',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.product'),
        ),
        migrations.AlterField(
            model_name='useruploadedfile',
            name='procedure',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.fistprocedure'),
        ),
        migrations.CreateModel(
            name='Graph',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('xs', models.CharField(max_length=1024)),
                ('ys', models.CharField(max_length=1024)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('type', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.product')),
            ],
        ),
    ]
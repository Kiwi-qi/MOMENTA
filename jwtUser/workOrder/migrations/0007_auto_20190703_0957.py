# Generated by Django 2.0.4 on 2019-07-03 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workOrder', '0006_auto_20190703_0943'),
    ]

    operations = [
        migrations.AddField(
            model_name='autoactionconf',
            name='method',
            field=models.CharField(default='', max_length=64, verbose_name='请求方式'),
        ),
        migrations.AlterField(
            model_name='autoactionconf',
            name='url',
            field=models.CharField(max_length=64, verbose_name='url'),
        ),
    ]

# Generated by Django 2.0.4 on 2019-07-08 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workOrder', '0019_subordercallbacklog'),
    ]

    operations = [
        migrations.AddField(
            model_name='suborder',
            name='approvetorole',
            field=models.BooleanField(default=False, verbose_name='是否角色组审批'),
        ),
    ]

# Generated by Django 2.0.4 on 2019-07-05 04:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workOrder', '0011_auto_20190705_1208'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='suborder',
            options={'verbose_name_plural': '子工单实例'},
        ),
        migrations.AlterModelOptions(
            name='subordercallbacklog',
            options={'verbose_name_plural': '子工单审批完成自动执行状态'},
        ),
        migrations.AlterModelOptions(
            name='workorder',
            options={'verbose_name_plural': '实例化工单'},
        ),
        migrations.AlterModelOptions(
            name='workordercallbacklog',
            options={'verbose_name_plural': '工单审批完成自动执行状态'},
        ),
    ]

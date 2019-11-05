# Generated by Django 2.0.4 on 2019-07-02 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FlowConf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='工作流名称')),
                ('callback', models.CharField(max_length=64, verbose_name='回调地址')),
                ('creater', models.CharField(max_length=64, verbose_name='创建者(user)')),
                ('customfield', models.CharField(max_length=64, verbose_name='自定义字段')),
                ('desciription', models.CharField(max_length=64, verbose_name='描述')),
            ],
        ),
    ]
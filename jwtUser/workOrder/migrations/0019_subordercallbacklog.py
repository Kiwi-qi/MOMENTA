# Generated by Django 2.0.4 on 2019-07-05 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workOrder', '0018_auto_20190705_1959'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubOrderCallbacklog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('callbackconf', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(choices=[('0', '待执行'), ('1', '完成'), ('2', '执行异常')], max_length=5, verbose_name='回调状态')),
                ('executetime', models.DateTimeField(blank=True, null=True, verbose_name='执行时间')),
                ('log', models.TextField(blank=True, null=True)),
                ('method', models.CharField(blank=True, max_length=24, null=True)),
                ('sub_order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='workOrder.SubOrder', verbose_name='子工单名称')),
            ],
            options={
                'verbose_name_plural': '子工单审批完成自动执行状态',
            },
        ),
    ]
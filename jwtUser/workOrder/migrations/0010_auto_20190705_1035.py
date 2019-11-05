# Generated by Django 2.0.4 on 2019-07-05 02:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workOrder', '0009_auto_20190703_1618'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approve_user_role', models.CharField(max_length=50, verbose_name='审批角色')),
                ('approve_userrole_id', models.IntegerField(blank=True, null=True, verbose_name='审批角色ID')),
                ('sequence_number', models.IntegerField(verbose_name='审批序号')),
                ('approve_ts', models.DateTimeField(blank=True, null=True, verbose_name='审批时间')),
                ('action_status', models.CharField(choices=[('0', '待处理'), ('1', '通过'), ('2', '退回'), ('3', '否决'), ('4', '确认')], max_length=10, verbose_name='审批状态')),
                ('suborder_status', models.CharField(choices=[('0', '待上一节点处理'), ('1', '待处理'), ('2', '已经处理')], max_length=20, verbose_name='子任务状态')),
                ('approve_text', models.TextField(blank=True, verbose_name='审批意见')),
                ('is_auto', models.BooleanField(default=False, verbose_name='自动工单')),
                ('timeout', models.CharField(default='10', max_length=32, verbose_name='超时时间')),
                ('approve_user', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '子工单实例',
            },
        ),
        migrations.CreateModel(
            name='SubOrderCallbacklog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('callbackconf', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(choices=[('0', '待执行'), ('1', '完成'), ('2', '执行异常')], max_length=5, verbose_name='回调状态')),
                ('executetime', models.DateTimeField(blank=True, null=True, verbose_name='执行时间')),
                ('log', models.TextField()),
                ('method', models.CharField(blank=True, max_length=24, null=True)),
                ('sub_order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='workOrder.SubOrder', verbose_name='子工单名称')),
            ],
            options={
                'verbose_name_plural': '子工单审批完成自动执行状态',
            },
        ),
        migrations.CreateModel(
            name='WorkOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_ts', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('order_status', models.CharField(choices=[('0', '审批中'), ('1', '被退回'), ('2', '完成')], default='0', max_length=5, verbose_name='工单状态')),
                ('parameter', models.TextField(default={}, verbose_name='新工单参数')),
                ('description', models.TextField(default='', verbose_name='工单描述')),
                ('create_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
                ('flowconf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workOrder.FlowConf', verbose_name='工单名称')),
            ],
            options={
                'verbose_name_plural': '实例化工单',
            },
        ),
        migrations.CreateModel(
            name='WorkorderCallbacklog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('callbackurl', models.CharField(blank=True, max_length=255, null=True, verbose_name='回调url')),
                ('status', models.CharField(choices=[('0', '待执行'), ('1', '完成'), ('2', '执行异常')], max_length=5, verbose_name='回调状态')),
                ('executetime', models.DateTimeField(blank=True, null=True, verbose_name='执行时间')),
                ('log', models.TextField()),
                ('workorder', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='workOrder.WorkOrder', verbose_name='实例化工单名称')),
            ],
            options={
                'verbose_name_plural': '工单审批完成自动执行状态',
            },
        ),
        migrations.AddField(
            model_name='suborder',
            name='mainorder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workOrder.WorkOrder', verbose_name='实例工单名称'),
        ),
    ]

from django.db import models
from users.models import User,Department
# Create your models here.


class FlowConf(models.Model):
    name = models.CharField(max_length=64,verbose_name='工作流名称')
    callback = models.CharField(max_length=64,verbose_name='回调地址',null=True)
    creater = models.ForeignKey(to=User,on_delete=models.CASCADE)
    customfield = models.TextField(verbose_name='自定义字段')
    description = models.TextField(verbose_name='描述')


    def __str__(self):
        return self.name

class NewFlowUserRoleActionConf(models.Model):    #审批角色配置
    flowconf = models.ForeignKey(to=FlowConf,on_delete=models.CASCADE)
    sequence = models.CharField(max_length=64,verbose_name='审批序号')
    approvetorole = models.BooleanField(default=False,verbose_name='是否角色组审批')
    approve_type_id = models.CharField(max_length=64,verbose_name='审批类型')
    is_auto = models.BooleanField(default=False,verbose_name='是否自动化')

    def __str__(self):
        return self.sequence

class AutoActionConf(models.Model):
    flowconf = models.OneToOneField(to=NewFlowUserRoleActionConf,on_delete=models.CASCADE)
    timeout = models.CharField(max_length = 64,verbose_name='超时时间',default='')
    url = models.CharField(max_length = 64,verbose_name='url')
    method = models.CharField(max_length = 64,default='',verbose_name='请求方式')


    def __str__(self):
        return self.url


class WorkOrder(models.Model):
    flowconf = models.ForeignKey(to='FlowConf',on_delete=models.CASCADE,verbose_name='工单名称')
    create_user = models.ForeignKey(to=User,on_delete=models.CASCADE,verbose_name='创建者')
    create_ts = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    status_cat = (
        ('0', '审批中'),
        ('1', '被退回'),
        ('2', '完成'),
    )
    order_status = models.CharField(max_length=5, verbose_name='工单状态', choices=status_cat, default='0')
    parameter = models.TextField(verbose_name='新工单参数',default={})
    description = models.TextField(verbose_name='工单描述',default='')

    def __str__(self):
        return 'instantiationworkorder'

    class Meta:
        verbose_name_plural = '实例化工单'


class SubOrder(models.Model):
    action_cat = (
        ('0', '待处理'),
        ('1', '通过'),
        ('2', '退回'),
        ('3', '否决'),
        ('4', '确认')
    )
    suborder_cat = (
        ('0', '待上一节点处理'),
        ('1', '待处理'),
        ('2', '已经处理'),
    )
    mainorder = models.ForeignKey(WorkOrder,on_delete=models.CASCADE, verbose_name='实例工单名称')
    approve_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, default='')
    approvetorole = models.BooleanField(default=False,verbose_name='是否角色组审批')
    approve_user_role = models.CharField(verbose_name='审批角色', max_length=50)
    approve_userrole_id = models.IntegerField(verbose_name='审批角色ID', null=True, blank=True)
    dispose_user = models.IntegerField(verbose_name='处理后用户id', null=True, blank=True)
    sequence_number = models.IntegerField(verbose_name='审批序号')
    approve_ts = models.DateTimeField(verbose_name='审批时间', null=True, blank=True)
    action_status = models.CharField(verbose_name='审批状态', choices=action_cat, max_length=10)
    suborder_status = models.CharField(verbose_name='子任务状态', choices=suborder_cat, max_length=20)
    approve_text = models.TextField(verbose_name='审批意见', blank=True)
    is_auto = models.BooleanField(default=False, verbose_name='自动工单')
    timeout = models.CharField(verbose_name='超时时间', default='10',max_length=32)

    def __str__(self):
        return 'sequence_number'
    class Meta:
        verbose_name_plural = '子工单实例'


class WorkorderCallbacklog(models.Model):
    status_cat = (
        ('0', '待执行'),
        ('1', '完成'),
        ('2', '执行异常'),
    )
    workorder = models.OneToOneField(WorkOrder,on_delete=models.CASCADE,verbose_name='实例化工单名称')
    callbackurl = models.CharField(max_length=255, null=True, blank=True,verbose_name='回调url')
    status = models.CharField(max_length=5, verbose_name='回调状态', choices=status_cat)
    executetime = models.DateTimeField(verbose_name='执行时间', null=True, blank=True)
    log = models.TextField(null=True, blank=True)

    def __str__(self):
        return 'status'

    class Meta:
        verbose_name_plural = '工单审批完成自动执行状态'


class SubOrderCallbacklog(models.Model):
    status_cat = (
        ('0', '待执行'),
        ('1', '完成'),
        ('2', '执行异常'),
    )
    sub_order = models.OneToOneField(SubOrder,verbose_name='子工单名称',on_delete=models.CASCADE)
    callbackconf = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=5, verbose_name='回调状态', choices=status_cat)
    executetime = models.DateTimeField(verbose_name='执行时间', null=True, blank=True)
    log = models.TextField(null=True, blank=True)
    method = models.CharField(blank=True, null=True, max_length=24)
    def __str__(self):
        return 'status'
    class Meta:
        verbose_name_plural = '子工单审批完成自动执行状态'

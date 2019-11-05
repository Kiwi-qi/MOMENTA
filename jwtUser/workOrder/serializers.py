from rest_framework import serializers
from users.models import *
from .models import *
import json
from django.core.paginator import Paginator


class FlowConfSerializers(serializers.ModelSerializer):
    creater_user = serializers.SerializerMethodField()
    class Meta:
        model = FlowConf
        fields = ('id','name','callback','customfield','description','creater_user')

    def get_creater_user(self,data):
        use = User.objects.filter(id = data.creater_id).all()
        alist=[]
        for i in use:
            alist.append({'username':i.username})
  
        return alist


class RoleinfoSerializers(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ('id','name')


class UserinfoSerializers(serializers.ModelSerializer):
    name = serializers.CharField(source='username')
    class Meta:
        model = User
        fields = ('id','name')


class UserActionSerializers(serializers.ModelSerializer):
    actionconf = serializers.SerializerMethodField()
    class Meta:
        model = FlowConf
        fields = ('actionconf',)
    
    def get_actionconf(self,obj):
        fl = FlowConf.objects.get(id = obj.id)
        useraction = fl.newflowuserroleactionconf_set.all()
        alist = []
        for i in useraction:   
            if i.is_auto == True:
                if i.approvetorole == False:
                    auto = AutoActionConf.objects.filter(flowconf_id = i.id).all()
                    user = User.objects.filter(id = i.approve_type_id).first()
                    if auto:
                        for url in auto:
                            alist.append({'id':i.id,'approvetype':user.username,'sequence':i.sequence,'approvetorole':i.approvetorole,'is_auto':i.is_auto,'url':url.url})
                    else:
                        alist.append({'id':i.id,'approvetype':user.username,'sequence':i.sequence,'approvetorole':i.approvetorole,'is_auto':i.is_auto})
                else:
                    role = Role.objects.filter(id = i.approve_type_id).first()
                    auto = AutoActionConf.objects.filter(flowconf_id = i.id).all()
                    if auto:  
                        for url in auto: 
                            alist.append({'id':i.id,'approvetype':role.name,'sequence':i.sequence,'approvetorole':i.approvetorole,'is_auto':i.is_auto,'url':url.url})
                    else:
                        alist.append({'id':i.id,'approvetype':role.name,'sequence':i.sequence,'approvetorole':i.approvetorole,'is_auto':i.is_auto})         
            if i.is_auto == False:
                if i.approvetorole == False:
                    user = User.objects.filter(id = i.approve_type_id).first()
                    alist.append({'id':i.id,'approvetype':user.username,'sequence':i.sequence,'approvetorole':i.approvetorole,'is_auto':i.is_auto})
                else:
                    role = Role.objects.filter(id = i.approve_type_id).first()
                    alist.append({'id':i.id,'approvetype':role.name,'sequence':i.sequence,'approvetorole':i.approvetorole,'is_auto':i.is_auto})
        return alist        

    
class UpdateAutoActionConfSerializers(serializers.ModelSerializer):
    Up = serializers.SerializerMethodField()
    class Meta:
        model = NewFlowUserRoleActionConf
        fields = ('Up',)

    def get_Up(self,obj):
        alist = []
        nurac = NewFlowUserRoleActionConf.objects.filter(id=obj.id).first()
        if nurac.approvetorole == False:
            user = User.objects.filter(id = nurac.approve_type_id).first()
            alist.append({'name':user.username,'sequence':nurac.sequence,'approvetorole':nurac.approvetorole,'id':nurac.approve_type_id,'is_auto':nurac.is_auto})
        else:
            role = Role.objects.filter(id = nurac.approve_type_id).first()
            alist.append({'name':role.name,'sequence':nurac.sequence,'approvetorole':nurac.approvetorole,'id':nurac.approve_type_id,'is_auto':nurac.is_auto})
        return alist

    


class InitFormConfSerializers(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()
    class Meta:
        model = FlowConf
        fields = ('data',)

    def get_data(self,obj):
        alist = []
        flw = FlowConf.objects.filter(id = obj.id).first()
        user = flw.creater
        depart = DepartUser.objects.filter(user_id = user.id).first()
        data = json.loads(flw.customfield)
        department = Department.objects.filter(id = depart.department_id).first()
        selfdepartment = Department.objects.filter(fid_id = department)
        for i in selfdepartment:
            alist.append(i.name)
                
        fixed_param = {
                    "ruleForm": {
                        "flowconf_desc": "",
                        "mydeptpath": "",
                        "workorder_name": ""
                    },
                    "rules": {

                    },
                    "field_list": [{
                        "field_type": "input",  
                        "verbos_name": "工单名称",  
                        "name": "workorder_name",  
                        "external": False,  
                        "msg": "",  
                        "field_datasource": [],  
                        "is_disabled": True,  
                        "value": flw.name,
                    }, {
                        "field_type": "select",
                        "verbos_name": "我的部门",
                        "name": "mydeptpath",
                        "external": False,
                        "msg": '',
                        "field_datasource": alist,
                        "is_disabled": True,
                        "value": alist[0],
                    }, {
                        "field_type": "textarea",
                        "verbos_name": "工单描述",
                        "name": "flowconf_desc",
                        "external": False,
                        "msg": '',
                        "field_datasource": [],
                        "is_disabled": False,
                        "value": flw.description,
                    }]      
                    }
        data['ruleForm'].update(fixed_param['ruleForm'])
        data['rules'].update(fixed_param['rules'])
        data['field_list'] = fixed_param['field_list'] + data['field_list']
            
        return data

class InitFlowStepInfoSerializers(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    class Meta:
        model = FlowConf
        fields = ('data',)
        
    def get_data(self,obj):
        alist = []

        flw = FlowConf.objects.filter(id = obj.id).first()
        nfurac = flw.newflowuserroleactionconf_set.all()
        for i in nfurac:
            if i.approvetorole == False:
                user = User.objects.filter(id = i.approve_type_id).first()
                alist.append(user.username)
            else:
                role = Role.objects.filter(id = i.approve_type_id).first()
                alist.append(role.name)

        adict = {"data": {
                    "flow_step": alist
        }
        }

        return adict
        


class CustomSerializers(serializers.ModelSerializer):
    class Meta:
        model = FlowConf
        fields = ('description',)


class WorkOrderSerializers(serializers.ModelSerializer):
    id = serializers.CharField()
    flowconf = serializers.CharField(source = 'flowconf.name')
    create_ts = serializers.CharField()
    create_user = serializers.CharField(source = 'create_user.username')
    order_status = serializers.SerializerMethodField()
    description = serializers.CharField()
    
    class Meta:
        model = WorkOrder
        fields = ('id','flowconf','create_ts','create_user','order_status','description')

    def get_order_status(self,obj):
        workorder = WorkOrder.objects.filter(id = obj.id).all()
        for work in workorder:
            if work.order_status == '0':
                work.order_status = '审批中'
            if work.order_status == '1':
                work.order_status = '被退回'
            if work.order_status == '2':
                work.order_status = '完成'
        return work.order_status


class SubOrderSerializers(serializers.ModelSerializer):
    id = serializers.CharField()
    wid = serializers.CharField(source = 'mainorder.id')
    mainorder = serializers.CharField(source = 'mainorder.flowconf.name')
    create_user = serializers.CharField(source='mainorder.create_user.username')
    approve_user_role = serializers.CharField()
    action_status = serializers.SerializerMethodField()
    description = serializers.CharField(source = 'mainorder.flowconf.description')
    
    class Meta:
        model = SubOrder
        fields = ('id','mainorder','create_user','approve_user_role','action_status','description','wid')

    def get_action_status(self,obj):
        suborder = SubOrder.objects.filter(id = obj.id).all()
        for sub in suborder:
            work = sub.mainorder
            if work.order_status == '0':
                work.order_status = '审批中'
            if work.order_status == '1':
                work.order_status = '被退回'
            if work.order_status == '2':
                work.order_status = '完成'
        return work.order_status


class DetailWorkerSerializers(serializers.ModelSerializer):
    id = serializers.CharField()
    flowconf = serializers.CharField(source = 'flowconf.name')
    create_ts = serializers.CharField()
    parameter = serializers.SerializerMethodField()
    create_user = serializers.CharField(source = 'create_user.username')
    create_user_email = serializers.CharField(source = 'create_user.email')
    order_status = serializers.SerializerMethodField()
   
    
    class Meta:
        model = WorkOrder
        fields = ('id','flowconf','create_ts','create_user','create_user_email','order_status','parameter')

    def get_order_status(self,obj):
        workorder = WorkOrder.objects.filter(id = obj.id).first()
       
        if workorder.order_status == '0':
            workorder.order_status = '审批中'
        if workorder.order_status == '1':
            workorder.order_status = '被退回'
        if workorder.order_status == '2':
            workorder.order_status = '完成'
        return workorder.order_status

    def get_parameter(self,obj):
        workorder = WorkOrder.objects.filter(id = obj.id).first()
        parameter = json.loads(workorder.parameter)
        ruleForm = parameter['ruleForm']
        verbos_name = parameter['field_list'][0]['verbos_name']

        return {'ruleForm':ruleForm,'verbos_name':verbos_name}




class DetailSuborderSerializers(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()
    options = serializers.SerializerMethodField()
    active = serializers.SerializerMethodField()
    class Meta:
        model = WorkOrder
        fields = ('data','options','active')


    def get_data(self,obj):
        workorder = WorkOrder.objects.filter(id = obj.id).first()
        suborder = workorder.suborder_set.all()
        alist = []
        for sub in suborder:
            username = User.objects.filter(id = sub.dispose_user).first()
            dispose_user = User.objects.filter(id = sub.approve_userrole_id).first()
            if sub.approvetorole == True:
                if sub.action_status == '3' and sub.suborder_status == '2':
                    sub.suborder_status = '已经处理'
                    sub.action_status = '拒绝'
                    userrole = UserRole.objects.filter(role_id = sub.approve_userrole_id).all()
                    user_list = []
                    for user_role in userrole:
                        user = User.objects.filter(id = user_role.user_id).first()
                        user_list.append(user.username)
                    alist.append({'id':sub.id,'approve_ts':sub.approve_ts,'users':user_list,'suborder_status':sub.suborder_status,'action':True,'dispose_user':username.username})
                else:
                    if sub.suborder_status == '0':
                        
                        sub.suborder_status = '待上一节点处理'

                        userrole = UserRole.objects.filter(role_id = sub.approve_userrole_id).all()
                        user_list = []
                        for user_role in userrole:
                            user = User.objects.filter(id = user_role.user_id).first()
                            user_list.append(user.username)
                        alist.append({'id':sub.id,'approve_ts':sub.approve_ts,'users':user_list,'suborder_status':sub.suborder_status,'examine':False})
                    if sub.suborder_status == '1':
                        
                        sub.suborder_status = '待处理'
                        userrole = UserRole.objects.filter(role_id = sub.approve_userrole_id).all()  
                        user_list = []
                        for user_role in userrole:
                            user = User.objects.filter(id = user_role.user_id).first()
                            user_list.append(user.username)
                        alist.append({'id':sub.id,'approve_ts':sub.approve_ts,'users':user_list,'suborder_status':sub.suborder_status,'examine':True})
                    if sub.suborder_status == '2':

                        
                        sub.suborder_status = '已经处理'
                        userrole = UserRole.objects.filter(role_id = sub.approve_userrole_id).all()  
                        user_list = []
                        for user_role in userrole:
                            user = User.objects.filter(id = user_role.user_id).first()
                            user_list.append(user.username) 
                        alist.append({'id':sub.id,'approve_ts':sub.approve_ts,'users':user_list,'suborder_status':sub.suborder_status,'dispose':True,'dispose_user':username.username})
            else:
                if sub.action_status == '3' and sub.suborder_status == '2':
                    sub.suborder_status = '已经处理'
                    sub.action_status = '拒绝'
                    userrole = UserRole.objects.filter(role_id = sub.approve_userrole_id).all()
                    user_list = []
                    for user_role in userrole:
                        user = User.objects.filter(id = user_role.user_id).first()
                        user_list.append(user.username)
                    alist.append({'id':sub.id,'approve_ts':sub.approve_ts,'users':user_list,'suborder_status':sub.suborder_status,'action':True,'dispose_user':username.username})
                else:
                    if sub.suborder_status == '0':
                        
                        sub.suborder_status = '待上一节点处理'
        
                        alist.append({'id':sub.id,'approve_ts':sub.approve_ts,'users':[sub.approve_user_role],'suborder_status':sub.suborder_status,'examine':False})
                    if sub.suborder_status == '1':

                        
                        sub.suborder_status = '待处理'

                        alist.append({'id':sub.id,'approve_ts':sub.approve_ts,'users':[sub.approve_user_role],'suborder_status':sub.suborder_status,'examine':True})
                    if sub.suborder_status == '2':
                        sub.suborder_status = '已经处理'   
                        alist.append({'id':sub.id,'approve_ts':sub.approve_ts,'users':[sub.approve_user_role],'suborder_status':sub.suborder_status,'dispose':True,'dispose_user':username.username})
        return alist
    
    def get_options(self,obj):
        workorder = WorkOrder.objects.filter(id = obj.id).first()
        suborder = workorder.suborder_set.all()
        alist = []
        for sub in suborder:
            alist.append({'role_user':sub.approve_user_role})

        return alist

    def get_active(self,obj):
        workorder = WorkOrder.objects.filter(id = obj.id).first()
        suborder = workorder.suborder_set.all()
        
        for sub in suborder:
            if sub.suborder_status == '1':
                return sub.sequence_number


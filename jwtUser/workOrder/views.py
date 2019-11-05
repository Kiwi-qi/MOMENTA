from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.utils import jwt_decode_handler
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import *
from workOrder.models import *
from django.db.models import Q
import json
from django.core.paginator import Paginator
import datetime
# Create your views here.

def is_approve_user_role(uid):
    alist = []
    user_suborder = SubOrder.objects.filter(approve_userrole_id = uid,suborder_status = '1').all()
    if user_suborder:
        alist.append(user_suborder)

    userrole = UserRole.objects.filter(user_id=uid).all()
    for userrole in userrole:
        suborder = SubOrder.objects.filter(approve_userrole_id = userrole.role_id,suborder_status = '1').all()
        if suborder:
            alist.append(suborder)
    new_query = []
    
    for i in alist:
        for a in i:
            new_query.append(a)
    return new_query
        
            
           
    
            
            
def detail_examine(uid,wid):
    workorder = WorkOrder.objects.get(pk = wid)

    suborder = workorder.suborder_set.all()
    for sub in suborder:
        if sub.approvetorole == True:
            userrole = UserRole.objects.filter(role_id = sub.approve_userrole_id,user_id=uid).first()
            if userrole:
                workorder = WorkOrder.objects.get(pk = wid)
                suborder = workorder.suborder_set.all()
                for sub in suborder:
         
                    if sub.approve_userrole_id == userrole.role_id and sub.suborder_status == '1':
                        return sub
                
        else:
            workorder = WorkOrder.objects.get(pk = wid)
            suborder = workorder.suborder_set.all()
            for sub in suborder:
                if sub.approve_userrole_id == uid and sub.suborder_status == '1':
                    return sub
            
        

class ViewWorkOrder(APIView):
    def get(self,request):
        
        work = FlowConf.objects.all()
        data = FlowConfSerializers(work,many=True)
        
        return Response(data=data.data,status=200)


class CreateWork(APIView):
    permission_classes = [IsAuthenticated]  # 接口中加权限
    authentication_classes = [JSONWebTokenAuthentication]
    def post(self,request):
        data = request.data
        user_token = jwt_decode_handler(data['token'])
        
        FlowConf.objects.create(
            name = data['name'],
            callback = data['callback'],
            creater_id = user_token['user_id'],
            customfield = data['customfield'],
            description = data['description']
        )
        
        return Response(status=200)

class UpdateWork(APIView):
    permission_classes = [IsAuthenticated]  # 接口中加权限
    authentication_classes = [JSONWebTokenAuthentication]
    def post(self,request):
        
        data = request.data
        flw = FlowConf.objects.get(pk = int(data['wid']))
        flw.name = data['name']
        flw.callback = data['callback']
        flw.customfield = data['customfield']    
        flw.description = data['description']  
        flw.save() 
        
        return Response(status=200)


class SearchWork(APIView):
    permission_classes = [IsAuthenticated]  # 接口中加权限
    authentication_classes = [JSONWebTokenAuthentication]
    def post(self,request):
        con = request.data['content']
       
        work_queryset = FlowConf.objects.filter(Q(id__icontains=con)|Q(name__icontains=con)|Q(callback__icontains=con)|Q(customfield__icontains=con)|Q(description__icontains=con))
        
        if work_queryset:
            data = FlowConfSerializers(instance = work_queryset,many=True)
            return Response(data=data.data,status=200)
        else:
            return Response(status=400)


class ActionRoleinfo(APIView):   #角色信息
    def get(self,request):
        
        role = Role.objects.all()
        data = RoleinfoSerializers(role,many=True)
        
        return Response(data=data.data,status=200)

class ActionUserinfo(APIView):   #用户信息
    def get(self,request):
        
        user = User.objects.all()
        data = UserinfoSerializers(user,many=True)
        
        return Response(data=data.data,status=200)


class UserAction(APIView):   
    def get(self,request):
        
        wid = request.query_params.get('wid')
        fl = FlowConf.objects.filter(id = wid).all()
        # fl = FlowConf.objects.get(id = wid)
        data = UserActionSerializers(fl,many=True)
        # print(fl.newflowuserroleactionconf_set.all())
        

        # user = User.objects.all()
        # data = UserinfoSerializers(user,many=True)
        
        # return Response(data=data.data,status=200)
        return Response(data=data.data,status=200)



class AddActionFlow(APIView):
    def post(self,request):
        data = request.data
        approvetorole = data['approvetorole']
        is_auto = data['is_auto']

        if approvetorole == 'true':
            approvetorole=1
        else:
            approvetorole=0
    
        if is_auto == 'true':
            is_auto=1
        else:
            is_auto=0
    
        try:
                NewFlowUserRoleActionConf.objects.create(
                    sequence = data['sequence'],
                    approvetorole = approvetorole,
                    approve_type_id =data['approve_type_id'],
                    is_auto = is_auto,
                    flowconf_id = data['wid']
                )
                msg = {'code':200,'message':'成功'}
                return Response (data=msg,status=200)
        except:
            msg = {'code':1001,'message':'创建流程失败'}
            return Response (data=msg,status=200)


class AddAutomation(APIView):
    def post(self,request):
        data = request.data

        auto = AutoActionConf.objects.filter(flowconf_id=data['autoactionconf_id']).first()
        if auto:
            auto.timeout = data['timeout']
            auto.url = data['url']
            auto.method = data['method']
            auto.save()
        else:
            try:
                AutoActionConf.objects.create(
                    timeout = data['timeout'],
                    url = data['url'],
                    method = data['method'],
                    flowconf_id = data['autoactionconf_id'],
                )
                msg = {'code':200,'message':'自动化创建成功'}
                return Response (data=msg,status=200)
            except:
                msg = {'code':1001,'message':'创建自动化失败'}
                return Response (data=msg,status=200)
        
        msg = {'code':200,'message':'修改自动化成功'}
        return Response (data=msg,status=200)
  
        
class DeleteActionFlow(APIView):
    def get(self,request):
        data = request.query_params.get('nid')

        nfrac = NewFlowUserRoleActionConf.objects.get(pk=data)
        nfrac.delete()


        return Response(status=200)

class UpdateAutoActionConf(APIView):
    def get(self,request):
        nid = request.query_params.get('nid')
        nurac = NewFlowUserRoleActionConf.objects.filter(id=nid).first()
        data = UpdateAutoActionConfSerializers(nurac)
        return Response(data=data.data,status=200)


class UpdateActionFlow(APIView):
    def post(self,request):
        data = request.data
        approvetorole = data['approvetorole']
        is_auto = data['is_auto']
        nid = data['nid']
    
        if approvetorole == 'true':
            approvetorole=1
        else:
            approvetorole=0
    
        if is_auto == 'true':
            is_auto=1
        else:
            is_auto=0
        
        upnurac = NewFlowUserRoleActionConf.objects.filter(id=nid)[0]
        upnurac.sequence = data['sequence']
        upnurac.approvetorole = approvetorole
        upnurac.approve_type_id = data['approve_type_id']
        upnurac.is_auto = is_auto
        upnurac.save()

        try:
            AutoActionConf.objects.get(flowconf_id = upnurac.id).delete()
        except:
            msg = {'code':200,'message':'成功'}
            return Response(data=msg,status=200)

        msg = {'code':200,'message':'成功'}
        return Response(data=msg,status=200)
         
        
class InitFormConf(APIView):
    def get(self,request):
        data = request.query_params.get('id')

        flw = FlowConf.objects.get(pk = data)
        data = InitFormConfSerializers(flw)

        return Response(data=data.data,status=200)

class InitFlowStepInfo(APIView):
    def get(self,request):
        data = request.query_params.get('id')

        flw = FlowConf.objects.get(pk = data)
       
        data = InitFlowStepInfoSerializers(flw)

        return Response(data=data.data,status=200)
            
class Custom(APIView):
    def get(self,request):
        data = request.query_params.get('id')

        flw = FlowConf.objects.get(pk = data)
        data = CustomSerializers(flw)

        return Response(data=data.data,status=200)


class InstantiationWorkOrder(APIView):
    def post(self,request):
        data = request.data
        user_token = jwt_decode_handler(data['token'])
        flowconf = FlowConf.objects.filter(id = data['fid']).first()   #工单模板
        customfield = json.loads(flowconf.customfield)
        customfield['ruleForm'] = data['parameter']
        customfield['field_list'][0]['value'] = data['parameter']
        new_customfield = json.dumps(customfield)
        user = flowconf.creater   #用户
        wk = WorkOrder.objects.filter(flowconf_id = flowconf.id).first()
        
        workorder = WorkOrder.objects.create(   #实例工单
            flowconf_id = flowconf.id,
            create_user_id = user_token['user_id'],
            parameter = new_customfield,
            description = data['description'], 
        )
        
        WorkorderCallbacklog.objects.create(   #初始工单审批完成自动执行状态
            workorder_id = workorder.id,
            callbackurl = flowconf.callback,
            status = 0,
        )

        nfurac = flowconf.newflowuserroleactionconf_set.all()  #子工单配置
        for nfurac1 in nfurac:
            if nfurac1.sequence == '1':
                if nfurac1.approvetorole == True:   #角色组
                    role = Role.objects.filter(id = nfurac1.approve_type_id).first()
                    autorole = AutoActionConf.objects.filter(flowconf_id = nfurac1.id).first()
                    if autorole:
                        rsbo = SubOrder.objects.create(      #实例子工单
                                mainorder_id = workorder.id,
                                approvetorole = nfurac1.approvetorole,
                                approve_user_role = role.name,
                                approve_userrole_id = nfurac1.approve_type_id,
                                sequence_number = nfurac1.sequence,
                                action_status = 0,
                                suborder_status = 1,
                                is_auto = nfurac1.is_auto,
                                timeout = autorole.timeout,
                            )

                        SubOrderCallbacklog.objects.create(   #子工单审批完成自动执行状态
                            sub_order_id = rsbo.id,
                            callbackconf = autorole.url,
                            status = 0,
                            method = autorole.method
                        )
                    else:
                        SubOrder.objects.create(
                            mainorder_id = workorder.id,
                            approvetorole = nfurac1.approvetorole,
                            approve_user_role = role.name,
                            approve_userrole_id = nfurac1.approve_type_id,
                            sequence_number = nfurac1.sequence,
                            action_status = 0,
                            suborder_status = 1,
                            is_auto = nfurac1.is_auto,
                        )
                else:
                    user = User.objects.filter(id = nfurac1.approve_type_id).first()
                    autouser = AutoActionConf.objects.filter(flowconf_id = nfurac1.id).first()
                    if autouser:
                        usbo = SubOrder.objects.create(      #子工单实例化
                                mainorder_id = workorder.id,
                                approvetorole = nfurac1.approvetorole,
                                approve_user_role = user.username,
                                approve_userrole_id = nfurac1.approve_type_id,
                                sequence_number = nfurac1.sequence,
                                action_status = 0,
                                suborder_status = 1,
                                is_auto = nfurac1.is_auto,
                                timeout = autouser.timeout,
                            )
                        SubOrderCallbacklog.objects.create(   #子工单审批完成自动执行状态
                            sub_order_id = usbo.id,
                            callbackconf = autouser.url,
                            status = 0,
                            method = autouser.method
                        )
                    else:
                        SubOrder.objects.create(
                            mainorder_id = workorder.id,
                            approvetorole = nfurac1.approvetorole,
                            approve_user_role = user.username,
                            approve_userrole_id = nfurac1.approve_type_id,
                            sequence_number = nfurac1.sequence,
                            action_status = 0,
                            suborder_status = 1,
                            is_auto = nfurac1.is_auto,
                        )
            else:
                if nfurac1.approvetorole == True:   #角色组
                    role = Role.objects.filter(id = nfurac1.approve_type_id).first()
                    autorole = AutoActionConf.objects.filter(flowconf_id = nfurac1.id).first()
                    if autorole:
                        rsbo = SubOrder.objects.create(      #实例子工单
                                mainorder_id = workorder.id,
                                approvetorole = nfurac1.approvetorole,
                                approve_user_role = role.name,
                                approve_userrole_id = nfurac1.approve_type_id,
                                sequence_number = nfurac1.sequence,
                                action_status = 0,
                                suborder_status = 0,
                                is_auto = nfurac1.is_auto,
                                timeout = autorole.timeout,
                            )

                        SubOrderCallbacklog.objects.create(   #子工单审批完成自动执行状态
                            sub_order_id = rsbo.id,
                            callbackconf = autorole.url,
                            status = 0,
                            method = autorole.method
                        )
                    else:
                        SubOrder.objects.create(
                            mainorder_id = workorder.id,
                            approvetorole = nfurac1.approvetorole,
                            approve_user_role = role.name,
                            approve_userrole_id = nfurac1.approve_type_id,
                            sequence_number = nfurac1.sequence,
                            action_status = 0,
                            suborder_status = 0,
                            is_auto = nfurac1.is_auto,
                        )
                else:
                    user = User.objects.filter(id = nfurac1.approve_type_id).first()
                    autouser = AutoActionConf.objects.filter(flowconf_id = nfurac1.id).first()
                    if autouser:
                        usbo = SubOrder.objects.create(      #子工单实例化
                                mainorder_id = workorder.id,
                                approvetorole = nfurac1.approvetorole,
                                approve_user_role = user.username,
                                approve_userrole_id = nfurac1.approve_type_id,
                                sequence_number = nfurac1.sequence,
                                action_status = 0,
                                suborder_status = 0,
                                is_auto = nfurac1.is_auto,
                                timeout = autouser.timeout,
                            )
                        SubOrderCallbacklog.objects.create(   #子工单审批完成自动执行状态
                            sub_order_id = usbo.id,
                            callbackconf = autouser.url,
                            status = 0,
                            method = autouser.method
                        )
                    else:
                        SubOrder.objects.create(
                            mainorder_id = workorder.id,
                            approvetorole = nfurac1.approvetorole,
                            approve_user_role = user.username,
                            approve_userrole_id = nfurac1.approve_type_id,
                            sequence_number = nfurac1.sequence,
                            action_status = 0,
                            suborder_status = 0,
                            is_auto = nfurac1.is_auto,
                        )

        msg = {'code':200,'message':'成功'}
        return Response(data=msg,status=200)

        

        # msg = {'code':200,'message':'成功'}
        # return Response(data=msg,status=200)
        
            
        
class ApplyOrder(APIView):
    def get(self,request):
        token = request.query_params.get('token')
        user_token = jwt_decode_handler(token)
        workorder = WorkOrder.objects.get_queryset().filter(create_user_id = user_token['user_id']).order_by('id')
        page = request.query_params.get('page')
        pagesize = request.query_params.get('pagesize')
        page_size = pagesize
        paginator = Paginator(workorder,page_size)
        total = paginator.num_pages   #总页数
        total_count = paginator.count  #总数量
        objs = paginator.page(int(page))     
        data = WorkOrderSerializers(objs,many=True)

        msg = {'data':data.data,'total':total_count}

        return Response(data=msg,status=200)


class AfterHandle(APIView):
    def get(self,request):
        data = request.query_params
        
        user_token = jwt_decode_handler(data['token'])
        query_set = is_approve_user_role(int(user_token['user_id']))
      
          
        if not query_set:
            msg = {'code':200,'message':'无审批'}
            return Response(data=msg,status=200)
        else:
            pagesize = request.query_params.get('pagesize')
            page_size = pagesize
            paginator = Paginator(query_set,page_size)
            total = paginator.num_pages   #总页数
            total_count = paginator.count  #总数量
            objs = paginator.page(int(data['page']))  
            data = SubOrderSerializers(instance = objs,many=True)

            msg = {'data':data.data,'total':total_count}
            return Response(msg,status=200)
        # return Response({'aa':'aa'})
    

class DetailWorker(APIView):
    def get(self,request):
        wid = request.query_params.get('wid')
        workorder = WorkOrder.objects.filter(id = wid).first()

        data = DetailWorkerSerializers(workorder)

        return Response(data=data.data,status=200)


class DetailSuborder(APIView):
    def get(self,request):
        data = request.query_params
        
        user_token = jwt_decode_handler(data['token'])
       
        workorder = WorkOrder.objects.filter(id = data['wid']).first()
        suborder = workorder.suborder_set.all()
        # alist = []
        # for sub in suborder:
        #     dispose_user = User.objects.filter(id = sub.dispose_user).first()
        #     print(dispose_user)
        #     if dispose_user:
        #         alist.append({'dispose_user':dispose_user.username})
       
        query_set = detail_examine(int(user_token['user_id']),data['wid'])
    
        data = DetailSuborderSerializers(workorder)
        
        if not query_set:
            msg = {'data':data.data,'examin':False}
            return Response(data=msg,status=200)
        else:
            msg = {'data':data.data,'examin':query_set.id}
            return Response(data=msg,status=200)

class PassSuborder(APIView):
    nexts = 1
    def post(self,request):
        data = request.data    
        user_token = jwt_decode_handler(data['token'])
        suborder = SubOrder.objects.get(id = data['sid'])
        suborder.dispose_user = user_token['user_id']
        suborder.approve_ts = datetime.datetime.now()
        suborder.action_status = '1'
        suborder.suborder_status = '2'
        suborder.approve_text = data['textarea']
        suborder.save()
        
        next_suborder = SubOrder.objects.filter(id = suborder.id+1,sequence_number = int(suborder.sequence_number) + self.nexts).first()
        if not next_suborder:
            workorder = WorkOrder.objects.get(pk = data['wid'])
            workorder.order_status = '2'
            workorder.save()
        else:
            next_suborder.suborder_status = '1'
            next_suborder.save()
        return Response(status=200)

class RefuseSuborder(APIView):
    nexts = 1
    def post(self,request):     
        data = request.data    
        user_token = jwt_decode_handler(data['token'])
        suborder = SubOrder.objects.get(id = data['sid'])

        suborder.dispose_user = user_token['user_id']
        suborder.approve_ts = datetime.datetime.now()
        suborder.action_status = '3'
        suborder.suborder_status = '2'
        suborder.approve_text = data['textarea']
        suborder.save()

        workorder = WorkOrder.objects.get(pk = data['wid'])
        workorder.order_status = '2'
        workorder.save()

        return Response(status=200)
    
        
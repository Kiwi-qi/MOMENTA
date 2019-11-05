from django.shortcuts import render
from users.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import *
import json
from django.db.models import Q


class Register(APIView):
    def post(self,request,*args,**kwargs):
        serializer = UserSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data =serializer.data,status=200)
        else:
            return Response(serializer.errors)

class Info(APIView):
    def get(self,request):
        data = User.objects.all()
        data = UserInfoSerializers(instance = data,many=True)

        return Response(data=data.data,status=200)
        # return Response(status=200)

class UpdateUserinfo(APIView):   #修改信息
    permission_classes = [IsAuthenticated]  # 接口中加权限
    authentication_classes = [JSONWebTokenAuthentication]
    def post(self,request):
        
        us = User.objects.get(pk = request.data.get('uid'))
        serializer = UserSerializers(instance = us,data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        else:
            return Response(status=200)

class Searchuserinfo(APIView):   #搜索
    permission_classes = [IsAuthenticated]  # 接口中加权限
    authentication_classes = [JSONWebTokenAuthentication]
    def post(self,request):
        con = request.data['content']
       
        user_queryset = User.objects.filter(Q(id__icontains=con)|Q(username__icontains=con)|Q(mobile__icontains=con)|Q(weixinid__icontains=con)|Q(email__icontains=con))
        print(user_queryset)
        if user_queryset:
            data = UserInfoSerializers(instance = user_queryset,many=True)
            return Response(data=data.data,status=200)
        else:
            return Response(status=400)

class DeleteUserinfo(APIView):   #删除信息
    permission_classes = [IsAuthenticated]  # 接口中加权限
    authentication_classes = [JSONWebTokenAuthentication]
    def post(self,request):
        
        data = request.data
        try:
            User.objects.get(pk = data['uid']).delete()
        
            return Response(status=200)
        except:
            return Response(status=400)


# 获取角色信息
class Roleuser(APIView):
    def get(self,request):
        

        roles = Role.objects.all()
        role = USerializers(roles,many=True)

        return Response(data=role.data,status=200)

# 添加角色信息
class Addrole(APIView):
    permission_classes = [IsAuthenticated]  # 接口中加权限
    authentication_classes = [JSONWebTokenAuthentication]
    def post(self,request):
        data1 = request.data.get('uid')
        data2 = request.data.getlist('r_id')
        for i in data2:
            us = UserRole.objects.create(user_id = data1,role_id=i)
        
        return Response(status=200)

class RoleInfo(APIView):
    def get(self,request):
        
        data = Role.objects.all()
        role = Role_Serializers(data,many=True)
        
        return Response(data=role.data,status=200)

class CreateRoleinfo(APIView):
    permission_classes = [IsAuthenticated]  # 接口中加权限
    authentication_classes = [JSONWebTokenAuthentication]
    def post(self,request):
        data = request.data
        Role.objects.create(
            zh_name = data['zh_name'],
            name = data['name'],
            description = data['description']
        )

        
        return Response(status=200)
        
class UpdateRoleinfo(APIView):
    permission_classes = [IsAuthenticated]  # 接口中加权限
    authentication_classes = [JSONWebTokenAuthentication]
    def post(self,request):
        data = request.data
        ro = Role.objects.get(pk = data['rid'])
        ro.zh_name = data['zh_name']
        ro.name = data['name']
        ro.description = data['description']
        ro.save()
        return Response(status=200)
       
class DeleteRoleinfo(APIView):
    permission_classes = [IsAuthenticated]  # 接口中加权限
    authentication_classes = [JSONWebTokenAuthentication]
    def post(self,request):
        data = request.data
        Role.objects.get(pk = data['rid']).delete()
        
        return Response(status=200)

class SearchRoleinfo(APIView):
    permission_classes = [IsAuthenticated]  # 接口中加权限
    authentication_classes = [JSONWebTokenAuthentication]
    def post(self,request):
        con = request.data['content']
       
        user_queryset = Role.objects.filter(Q(id__icontains=con)|Q(zh_name__icontains=con)|Q(name__icontains=con)|Q(description__icontains=con))
        print(user_queryset)
        if user_queryset:
            data = RoleInfoSerializers(instance = user_queryset,many=True)
            return Response(data=data.data,status=200)
        else:
            return Response(status=400)

       
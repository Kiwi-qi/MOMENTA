from rest_framework_jwt.settings import api_settings
from rest_framework import serializers
from users.models import *
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password

#用户注册
class UserSerializers(serializers.Serializer):  
    username = serializers.CharField()
    password = serializers.CharField()
    mobile = serializers.CharField()
    weixinid = serializers.CharField()
    email = serializers.CharField()

    class Meta:
        model = User

    def create(self,data):
        user = User.objects.create(**data)
        user.set_password(data.get('password'))
        user.save()

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token
        return user


    def update(self,instance,data):
        instance.username = data.get('username',instance.username)
        instance.mobile = data.get('mobile',instance.mobile)
        instance.password = make_password(data.get('password',instance.password)) 
        instance.weixinid = data.get('weixinid',instance.weixinid)
        instance.email = data.get('email',instance.email)
        instance.save()
        return instance

# class USerializers(serializers.Serializer):
#     role_list = serializers.SerializerMethodField()
    
#     class Meta:
#         model = User
        

#     def get_role_list(self,row):
#         RoleUser = UserRole.objects.filter(user_id = row.id).all()
#         alist = []
#         for i in RoleUser:
#             role = Role.objects.filter(id = i.role_id)[0]
#             alist.append({'id':role.id,'name':role.name})
#         return alist
    
class USerializers(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = "__all__"



class UserRoleSerializers(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name')
    role_id = serializers.CharField(source='role.id')

    class Meta:
        model = UserRole
        fields = ('role_name','role_id')



class DepartUserSerializers(serializers.ModelSerializer):  

    department_name = serializers.CharField(source='department.name')
    department_id = serializers.CharField(source='department.id')

    class Meta:
        
        model = DepartUser
        fields = ('department_name','department_id')

# class DepartmentSerializers(serializers.ModelSerializer):  
#     # role_name = serializers.CharField(source='role.name')
#     fid = serializers.CharField(source='fid.name')
#     class Meta:
        
#         model = Department
#         fields = ('name',)

#用户信息

class UserInfoSerializers(serializers.ModelSerializer):  
    # role_name = serializers.CharField(source='role.name')
    ro_user = UserRoleSerializers(many=True)
    de_user = DepartUserSerializers(many=True)
    
    class Meta:
        
        model = User
        fields = ('id','username','password','mobile','weixinid','email','ro_user','de_user')



class RoleSerializers(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user.id')
    user_name = serializers.CharField(source='user.username')
    
    class Meta:
        model = UserRole
        fields = ('user_name','user_id')


# class RoleSerializers(serializers.ModelSerializer):
#     user_class = serializers.SerializerMethodField()
    
#     class Meta:
#         model = UserRole
#         fields = ('user_name',)

#         def get_user_class(self,data):
#             user_ = User.objects.filter(id = data.id).all()
#             user_class = DepartUserSerializers(user_,many=True)
#             return user_class.data


class RoleInfoSerializers(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = ('id','zh_name','name','description','user_name')

    def get_user_name(self,data):
        user_ = UserRole.objects.filter(role_id = data.id).all()
        user_name = RoleSerializers(user_,many=True)

        return user_name.data


    # def get_department(self.data):
    #     dep = DepartUser.objects.filter()



class User_Serializers(serializers.ModelSerializer):
    de = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id','username','de')

    def get_de(self,obj):
        par = DepartUser.objects.filter(user_id = obj['id']).all()
        alist = []
        for i in par:
            depart = Department.objects.filter(id = i.department_id)[0]
            alist.append({'id':depart.id,'name':depart.name})

        return alist
        # us =  User_Serializers(alist,many=True)
        # de = Depart_Serializers(us)
        
        # return de.data
    


class Role_Serializers(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    class Meta:
        model = Role
        fields = ('id','zh_name','description','name','user_name')

    def get_user_name(self,obj):
        user_ = UserRole.objects.filter(role_id = obj.id).all()

        alist = []
        for i in user_:
            usr = User.objects.filter(id = i.user_id)[0]
            alist.append({'id':usr.id,'username':usr.username})

        us =  User_Serializers(alist,many=True)
    
        # return us
        return us.data
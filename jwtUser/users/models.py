from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=255)
    mobile = models.CharField(max_length=64,verbose_name='手机号',default='')
    weixinid = models.CharField(max_length=64,verbose_name='微信id',default='')
    email = models.CharField(max_length=64,verbose_name = '邮箱',default='')

    def __str__(self):
        return self.username


class Role(models.Model):
    zh_name = models.CharField(max_length=64)
    name = models.CharField(max_length=64,verbose_name='角色名称')
    description = models.CharField(max_length=64,verbose_name='描述')

    def __str__(self):
        return self.zh_name


class UserRole(models.Model):

    role = models.ForeignKey("Role",on_delete=models.CASCADE,related_name='ro_role')
    user = models.ForeignKey("User",on_delete=models.CASCADE,related_name='ro_user')


class Department(models.Model):
    name = models.CharField(max_length=255)
    fid = models.ForeignKey('self',on_delete=models.SET_NULL,null=True,blank=True,default=None)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '部门表'


class DepartUser(models.Model):

    department = models.ForeignKey("Department",on_delete=models.CASCADE,related_name='us_de')
    user = models.ForeignKey("User",on_delete=models.CASCADE,related_name='de_user')

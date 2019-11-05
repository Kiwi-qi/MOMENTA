from django.urls import path,re_path,include
from users import views
from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token #验证密码返回token

app_name = 'users'

urlpatterns = [
    path('register/', views.Register.as_view(),name='register'),
    path('login/', obtain_jwt_token,name='login'),

    path('info/', views.Info.as_view(), name='info'),
    path('deleteuserinfo/', views.DeleteUserinfo.as_view(), name='deleteuserinfo'),
    path('updateuserinfo/', views.UpdateUserinfo.as_view(), name='updateuserinfo'),
    path('searchuserinfo/', views.Searchuserinfo.as_view(), name='searchuserinfo'),

    path('roleinfo/', views.RoleInfo.as_view(), name='roleinfo'),
    path('role/', views.Roleuser.as_view(), name='role'),
    path('addrole/', views.Addrole.as_view(), name='addrole'),
    path('createroleinfo/', views.CreateRoleinfo.as_view(), name='createroleinfo'),
    path('updateroleinfo/', views.UpdateRoleinfo.as_view(), name='updateroleinfo'),
    path('deleteroleinfo/', views.DeleteRoleinfo.as_view(), name='deleteroleinfo'),
    path('searchroleinfo/', views.SearchRoleinfo.as_view(), name='searchroleinfo'),
]
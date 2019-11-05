from django.urls import path,re_path,include
from workOrder import views


app_name = 'work'

urlpatterns = [
    path('workorder/', views.ViewWorkOrder.as_view()),
    path('creatework/', views.CreateWork.as_view()),
    path('updatework/', views.UpdateWork.as_view()),
    path('searchwork/', views.SearchWork.as_view()),

    path('actionroleinfo/', views.ActionRoleinfo.as_view()),
    path('actionuserinfo/', views.ActionUserinfo.as_view()),

    path('useraction/', views.UserAction.as_view()),
    path('addactionflow/', views.AddActionFlow.as_view()),    #审批流程
    path('addautomation/', views.AddAutomation.as_view()),    #添加自动化
    path('deleteactionflow/', views.DeleteActionFlow.as_view()),    #删除自动化
    path('updateautoactionconf/', views.UpdateAutoActionConf.as_view()),    #流程数据

    path('updateactionflow/', views.UpdateActionFlow.as_view()),    #修改审批流

    path('initformconf/', views.InitFormConf.as_view()),    #渲染工单页面
    path('initflowstepinfo/', views.InitFlowStepInfo.as_view()),    
    path('custom/', views.Custom.as_view()),    

    path('instantiationworkorder/', views.InstantiationWorkOrder.as_view()),    #实例化工单
    path('applyorder/', views.ApplyOrder.as_view()),    #我申请的工单
    path('afterhandle/', views.AfterHandle.as_view()),    #待审批工单

    path('detailworker/', views.DetailWorker.as_view()),    #工单
    path('detailsuborder/', views.DetailSuborder.as_view()),    #子工单
    path('passsuborder/', views.PassSuborder.as_view()),    #审批
    path('refusesuborder/', views.RefuseSuborder.as_view()),    #拒绝
]
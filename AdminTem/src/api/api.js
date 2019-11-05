import URLS from '../../config/urls'
import { get, post } from './ajax'
let base = URLS.API_URL

// 用户相关
export const Register = p => post(`${base}/users/register/`, p);  //注册
export const Login = p => post(`${base}/users/login/`, p);    //登录
export const Userinfo = p => get(`${base}/users/info/`, p);  //用户主页
export const SearchUserinfo = p => post(`${base}/users/searchuserinfo/`, p);   //搜索用户信息
export const Updateuserinfo = p => post(`${base}/users/updateuserinfo/`, p);   //编辑用户信息
export const Delete = p => post(`${base}/users/deleteuserinfo/`, p);   //删除用户信息

export const Role = p => get(`${base}/users/role/`, p);   //获取角色信息
export const addRole = p => post(`${base}/users/addrole/`, p);   //获取角色信息

export const Roleinfo = p => get(`${base}/users/roleinfo/`, p);  //角色主页
export const SearchRoleinfo = p => post(`${base}/users/searchroleinfo/`, p);   //搜索角色信息
export const CreateRoleinfo = p => post(`${base}/users/createroleinfo/`, p);   //添加角色信息
export const UpdateRoleinfo = p => post(`${base}/users/updateroleinfo/`, p);   //编辑角色信息
export const DeleteRoleinfo = p => post(`${base}/users/deleteroleinfo/`, p);   //删除用户信息

// 模板相关
export const WorkOrder = p => get(`${base}/work/workorder/`, p);   //模板信息
export const CreateWork = p => post(`${base}/work/creatework/`, p);   //添加模板
export const UpdateWork = p => post(`${base}/work/updatework/`, p);   //修改模板
export const SearchWork = p => post(`${base}/work/searchwork/`, p);   //搜索模板

export const ActionRoleinfo = p => get(`${base}/work/actionroleinfo/`, p);   //获取角色信息
export const ActionUserinfo = p => get(`${base}/work/actionuserinfo/`, p);   //获取用户信息

export const UserAction = p => get(`${base}/work/useraction/`, p);   //获取用户对应的审批流程
export const AddActionFlow = p => post(`${base}/work/addactionflow/`, p);   //添加审批流程

export const AddAutomation  = p => post(`${base}/work/addautomation/`, p);   //添加自动化

export const DeleteActionFlow  = p => get(`${base}/work/deleteactionflow/`, p);   //删除自动化


export const UpdateAutoActionConf  = p => get(`${base}/work/updateautoactionconf/`, p);   //获取审批流程数据


export const UpdateActionFlow  = p => post(`${base}/work/updateactionflow/`, p);   //修改审批流程

export const InitFormConf  = p => get(`${base}/work/initformconf/`, p);   //修改审批流程
export const InitFlowStepInfo  = p => get(`${base}/work/initflowstepinfo/`, p);   //修改审批流程
export const Custom = p => get(`${base}/work/custom/`, p);   //修改审批流程


export const InstantiationWorkOrder = p => post(`${base}/work/instantiationworkorder/`, p);   //实例化工单信息


export const ApplyOrder = p => get(`${base}/work/applyorder/`, p);   //我申请的工单

export const AfterHandle = p => get(`${base}/work/afterhandle/`, p);   //待处理的工单


export const DetailWorker = p => get(`${base}/work/detailworker/`, p);   //待处理的工单
export const DetailSuborder = p => get(`${base}/work/detailsuborder/`, p);   //待处理的工单



export const PassSuborder = p => post(`${base}/work/passsuborder/`, p);   //待处理的工单

export const RefuseSuborder = p => post(`${base}/work/refusesuborder/`, p);   //待处理的工单
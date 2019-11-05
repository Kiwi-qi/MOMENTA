import Vue from 'vue'
import Router from 'vue-router'
Vue.use(Router)

import Home from '../views/Home.vue'

const page = name => () => import('@/views/' + name)
export default new Router({
    mode: 'history',
    routes: [
        {path: '/login',component: page('Login'),name: '登录',hidden:true},
        // {path: '/404',component: page('404'),name: '',hidden: true},
		{path: '/register', component: page('Register'), name: '注册',hidden: true},
		
        {path: '/',component: Home,name: '用户管理',iconCls: 'el-icon-message',//图标样式class
            children: [
				{ path: '/userinfo', component: page('nav1/UserInfo'), name: '用户信息' },
				{ path: '/roleinfo', component: page('nav1/RoleInfo'), name: '角色信息' },
            ]
        },
		{path: '/',component: Home,name: '工单管理',iconCls: 'el-icon-message',//图标样式class
		    children: [
				{ path: '/workorder', component: page('nav2/WorkOrder'), name: '工单信息' },
				{path: '/flowroleconf', component: page('nav2/FlowRoleConf'), name:'审批流程',hidden: true },
				{path: '/actionconf', component: page('nav2/ActionConf'), name: '配置自动化工单',hidden: true },
				{path: '/upactionConf', component: page('nav2/UpActionConf'), name: '修改自动化工单',hidden: true },
				
				{path: '/ordertemplatelist', component: page('nav2/OrderTemplateList'), name: '新建工单'},
				{path: '/index/:id', component: page('nav2/Index'), name: '实例化工单',hidden:true},
				
				{path: '/applyorder', component: page('nav2/ApplyOrder'), name: '我申请的工单'},
				{path: '/afterhandle', component: page('nav2/AfterHandle'), name: '待我审批'},
				
				
				{path: '/workdetail/:id', component: page('nav2/WorkDetail'), name: '审批详情',hidden:true},
				
		    ]
		},
        {path: '*',hidden: true,
		redirect: { path: '/404' }
        }
    ]
})

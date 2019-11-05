import babelpolyfill from 'babel-polyfill'
import Vue from 'vue'
import App from './App.vue'
import NProgress from 'nprogress'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import VueRouter from 'vue-router'
import store from './vuex/store'
import Vuex from 'vuex'
import router from './router'
import Mock from './mock'
Mock.bootstrap();
import 'font-awesome/css/font-awesome.min.css'

Vue.use(ElementUI)
Vue.use(VueRouter)
Vue.use(Vuex)

/*  定义：路由钩子主要是给使用者在路由发生变化时进行一些特殊的处理而定义的函数 */
router.afterEach(transition => {
    setTimeout(() => {
        NProgress.done()
    })
})

window.APP_INFO = process.env.APP_INFO

router.beforeEach((to, from, next) => {
    /*
    * to: router即将进入的路由对象
    * from: 当前导航即将离开的路由
    * next: 进行管道中的一个钩子，如果执行完了，则导航的状态就是 confirmed （确认的）；否则为false，终止导航。
    * */
    NProgress.start()
    // 使用假数据模拟张三已经登录
    localStorage.setItem('user', JSON.stringify({'username':'zhangsan'}) )
    if (to.path === '/login') {
        localStorage.removeItem('user')
    }
    let user = JSON.parse(localStorage.getItem('user'))
    if (!user && to.path !== '/login') {  // 如果用户没有登录，且访问url不是 '/login' 调整到登录页
        next({ path: '/login' })
    } else {
        next()
    }
})
/*  拦截器介绍位置 */

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')


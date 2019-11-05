**演示地址**: [https://taylorchen709.github.io/vue-admin/](https://taylorchen709.github.io/vue-admin/)

## 1.1 安装项目依赖&启动项目
``` python
npm install    # 安装依赖
npm run dev    # 启动项目
```
## 1.2 目录结构
* build : webpack配置文件
* config : webpack配置文件
* dist : build编译后文件
* src : 自己写代码文件件
    * api : 使用axios对请求封装模块
    * assets : 图片等资产文件夹
    * common : 常用公共方法文件夹
    * components : 官方建议存放组件位置
    * mock : 模拟后端返回数据模块(无需关注)
    * router : vue路由文件
    * styles : css样式
    * views : 自己开发的 .vue 页面
    * vuex : vue团队简化组件间的通信定义的规范
    * App.vue : 一般用做网站首页
    * main.js : 入口文件,主要作用是初始化vue实例
* static : css等静态资源存放位置
## 1.3 登录页面介绍(发送post请求)
> 1. 创建 src/views/Login.vue 文件

> 2. src\router\index.js配置路由
```python
{
    path: '/login',
    component: page('Login'),
    name: '',
    hidden: true
},
```
> 3.在src\api\api.js 定义发送请求函数
```javascript
export const requestLogin = params => { return axios.post(`${base}/login`, params).then(res => res.data); };
```
> 4.在src/views/Login.vue发送post请求
```javascript
//1、导入方法
import { requestLogin } from '../api/api';  

//2、直接使用导入的方法即可
var loginParams = { username: this.ruleForm2.account, password: this.ruleForm2.checkPass };
requestLogin(loginParams).then(data => {
  this.logining = false;
  let { msg, code, user } = data;
  if (code !== 200) {
	this.$message({
	  message: msg,
	  type: 'error'
	});
  } else {
	sessionStorage.setItem('user', JSON.stringify(user));
	this.$router.push({ path: '/' });
  }
});
```
## 1.4 用户list页(发送get请求)
> 1.创建 src/views/User.vue 文件

> 2.src\router\index.js配置路由
```python
{
    path: '/',
    component: Home,
    name: '导航一',
    iconCls: 'el-icon-message',//图标样式class
    children: [
        { path: '/user', component: page('nav1/User'), name: '用户' },
    ]
},
```
> 3.在src\api\api.js 定义发送请求函数
```javascript
export const getUserList = params => { return axios.get(`${base}/user/list`, { params: params }); };
```
> 4.在src/views/User.vue发送get请求
```python
//1、导入方法
import { getUserList } from '../../api/api';

//2、直接使用导入的方法即可
getUser: function () {
    let para = {
        name: this.filters.name
    };
    this.loading = true;
    getUserList(para).then((res) => {
        this.users = res.data.users;
        this.loading = false;
    });
}
```

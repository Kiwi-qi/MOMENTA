import Qs from 'qs'
import instance from './axiosinstance'  // 导入自定义 axios 实例
// import instance from 'axios'           // 也可以直接使用原生 axios 实例，但无法添加拦截器

/* 1. 发送GET请求 */
export function get(url, params){
    return new Promise((resolve, reject) =>{
        // 1、发送get请求
        instance({
            url: url,                     //1、请求地址
            method: 'get',                //2、请求方法
            params: params,                //3、get请求参数
            headers: {
                'Content-Type': 'application/json'
            },
            paramsSerializer: params => {                          //4、可选函数、序列化`params`
                return Qs.stringify(params, { indices: false })
            },
        })
        // 2、回调函数
            .then(res => {
                resolve(res.data);
            })
            // 3、捕获异常
            .catch(err => {
                reject(err.data)
            });

    });
}

/* 2. 发送POST请求 */
export function post(url, params) {
    var isFormData = Object.prototype.toString.call(params) === '[object FormData]'
    var data = '';  // 如果是上传文件传入的 params是一个 FormData对象，不要用Qs序列化
    if(isFormData){
        data = params
    }else {
        data = Qs.stringify(                               //3、可选函数、序列化`data`
            params,                                        //4、提交数据
            { indices: false }                            // indices: false
        )
    }
    return new Promise((resolve, reject) => {
        instance({
            url: url,             //1、请求地址
            method: 'post',                                  // 2、请求方法
            data: data,
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
            },
        })
        // 2、回调函数
            .then(res => {
                resolve(res.data);
            })
            // 3、捕获异常
            .catch(err => {
                reject(err.data)
            })
    });
}

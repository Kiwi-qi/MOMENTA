<template>

<div>
<el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm" style='width:300px; margin-left: 600px; margin-top: 200px;' >
	<el-form-item label="用户名" prop="username">
	  <el-input type="text" v-model="ruleForm.username" autocomplete="off" ></el-input>
	</el-form-item>
  <el-form-item label="密码" prop="pass">
    <el-input type="password" v-model="ruleForm.pass" autocomplete="off" ></el-input>
  </el-form-item>
  <el-form-item>
    <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
    <el-button @click="resetForm('ruleForm')">重置</el-button>
  </el-form-item>
</el-form>
</div>

</template>
<script>
	
	import {Login} from '../api/api.js'
	
  export default {
    data() {
			var username = (rule, value, callback) => {
			  if (value === '') {
			    callback(new Error('请输入用户名'));
				}	callback();
				};
			 var validatePass = (rule, value, callback) => {
			  if (value === '') {
			    callback(new Error('请输入密码'));
			  } 
			    callback();
			};
     
 
      return {
        ruleForm: {
					username:'',
          pass: '',
        },
        rules: {
					username: [
					  { validator: username, trigger: 'blur' }
					],
          pass: [
            { validator: validatePass, trigger: 'blur' }
          ]
        }
      };
    },
    methods: {
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
        if (valid) {
					console.log({'username':this.ruleForm.username,
									'password':this.ruleForm.pass,
				 					})
				 Login({'username':this.ruleForm.username,
									'password':this.ruleForm.pass,
				 					})
									
				.then(resp=>{
					// var token = 'JWT'+' '+resp.token;
					var token = resp.token;
					console.log(resp)
					localStorage.setItem('token',token)
				
					window.location='/userinfo/'
				})
				.catch(err=>{
					console.log(err.status)
				})
            
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      resetForm(formName) {
        this.$refs[formName].resetFields();
      }
    }
  }
</script>

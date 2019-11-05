<template>


<el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm" style='width:300px; margin-left: 600px; margin-top: 200px;'>
	<el-form-item label="用户名" prop="username">
	  <el-input type="text" v-model="ruleForm.username" autocomplete="off"></el-input>
	</el-form-item>
  <el-form-item label="密码" prop="pass">
    <el-input type="password" v-model="ruleForm.pass" autocomplete="off"></el-input>
  </el-form-item>
  <el-form-item label="确认密码" prop="checkPass">
    <el-input type="password" v-model="ruleForm.checkPass" autocomplete="off"></el-input>
  </el-form-item>
  <el-form-item label="手机号" prop="phone">
    <el-input v-model.number="ruleForm.phone"></el-input>
  </el-form-item>
	  <el-form-item label="微信号" prop="weixinid">
	  <el-input v-model.number="ruleForm.weixinid"></el-input>
	</el-form-item>
	  <el-form-item label="邮箱" prop="email">
	  <el-input v-model.number="ruleForm.email"></el-input>
	</el-form-item>
  <el-form-item>
    <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
    <el-button @click="resetForm('ruleForm')">重置</el-button>
  </el-form-item>
</el-form>


</template>
<script>
	
	import {Register} from '../api/api.js'
	
  export default {
    data() {
			var username = (rule, value, callback) => {
			  if (value === '') {
			    callback(new Error('请输入用户名'));
				}	callback();
				};
      var checkPhone = (rule, value, callback) => {
        if (!value) {
          return callback(new Error('手机号不能为空'));
        }
        setTimeout(() => {
          if (!Number.isInteger(value)) {
            callback(new Error('请输入数字值'));
          } {
              callback();
          }
        }, 1000);
      };
      var validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入密码'));
        } else {
          if (this.ruleForm.checkPass !== '') {
            this.$refs.ruleForm.validateField('checkPass');
          }
          callback();
        }
      };
      var validatePass2 = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请再次输入密码'));
        } else if (value !== this.ruleForm.pass) {
          callback(new Error('两次输入密码不一致!'));
        } else {
          callback();
        }
      };
      return {
        ruleForm: {
					username:'',
          pass: '',
          checkPass: '',
          phone: '',
					weixinid:'',
					email:'',
        },
        rules: {
					username: [
					  { validator: username, trigger: 'blur' }
					],
          pass: [
            { validator: validatePass, trigger: 'blur' }
          ],
          checkPass: [
            { validator: validatePass2, trigger: 'blur' }
          ],
          phone: [
            { validator: checkPhone, trigger: 'blur' }
          ],
        }
      };
    },
    methods: {
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
        if (valid) {
				var params = {'username':this.ruleForm.username,
									'password':this.ruleForm.pass,
									'mobile':this.ruleForm.phone,
									'weixinid':this.ruleForm.weixinid,
									'email':this.ruleForm.email}
				console.log(params)
				Register(params)
									
				.then(resp=>{
					window.location = '/login/'
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

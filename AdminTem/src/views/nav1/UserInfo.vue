<template>
	<div>
		<br>
		<div>
			<el-input
			placeholder="请输入内容"
			v-model="input"
			clearable style='width: 200px;'>
			</el-input>
			<el-button type="primary" icon="el-icon-search" @click="search">搜索</el-button>
		</div>
		
	
	<div>
	<el-table
      :data="tableData"
      style="width: 100%"
	   >
	  
	  <el-table-column
	    prop="id"
	    label="用户id"
	    width="100">
	  </el-table-column>
 
      <el-table-column
      label="姓名"
      width="180">
      <template slot-scope="scope">
        <el-popover trigger="hover" placement="top">
          角色: <p v-for="i in scope.row.ro_user">{{ i.role_name }}</p>
          部门: <p v-for="i in scope.row.de_user"> {{ i.department_name }}</p>
          <div slot="reference" class="name-wrapper">
            <el-tag size="medium">{{ scope.row.username }}</el-tag>
          </div>
        </el-popover>
      </template>
    </el-table-column>
	  
	  <el-table-column
	    prop="mobile"
	    label="手机号"
	    width="180">
	  </el-table-column>
	  
      <el-table-column
        prop="weixinid"
        label="微信号"
		width="180">
      </el-table-column>
	  
	  <el-table-column
      prop="email"
      label="邮箱"
      width="280">
    </el-table-column>
	
	<el-table-column label="添加角色">
	  <template slot-scope="scope">
	    <el-button
	      size="mini"
	      @click="addrole(scope.$index, scope.row)">添加角色</el-button>
	  </template>
	</el-table-column>
	
	
	 <el-table-column label="操作">
		 
		  
      <template slot-scope="scope">
        <el-button
          size="mini"
          @click="updateuserinfo(scope.$index, scope.row)">编辑</el-button>
        <el-button
          size="mini"
          type="danger"
          @click="handleDelete(scope.$index, scope.row)">删除</el-button>
      </template>
    </el-table-column>
	
	  
    </el-table>
	<!-- 添加角色 -->
	<el-dialog title="添加角色" :visible.sync="udialogFormVisible"> 
	  <el-form :model="form"  style='width: 650px;'>
	    <el-form-item label="用户名" :label-width="formLabelWidth" >
	      <el-input :disabled="true" v-model="form.username" autocomplete="off"></el-input>  <br>
		 
		  <br><el-select v-model="value1" multiple placeholder="请选择">   
			<el-option
			  v-for="item in options"
			  :key="item.id"
			  :label="item.name"
			  :value="item.id">
			</el-option>
		  </el-select>
	    </el-form-item>
		
	  </el-form>
	  <div slot="footer" class="dialog-footer">
	    <el-button @click="udialogFormVisible = false">取 消</el-button>
	    <el-button type="primary" @click="AddRole">确 定</el-button>
	  </div>
	  
	</el-dialog>
	
	
	
	
	<!-- 修改 -->
	<el-dialog title="修改信息" :visible.sync="dialogFormVisible">
	  <el-form :model="form"  style='width: 650px;'>
		  
	    <el-form-item label="用户名" :label-width="formLabelWidth">
	      <el-input v-model="form.username" autocomplete="off" ></el-input>
	    </el-form-item>
		<el-form-item label="手机号" :label-width="formLabelWidth">
		  <el-input v-model="form.mobile" autocomplete="off"></el-input>
		</el-form-item>
		<el-form-item label="微信号" :label-width="formLabelWidth">
		  <el-input v-model="form.weixinid" autocomplete="off"></el-input>
		</el-form-item>
		<el-form-item label="邮箱" :label-width="formLabelWidth">
		  <el-input v-model="form.email" autocomplete="off"></el-input>
		</el-form-item>
	  </el-form>
	  <div slot="footer" class="dialog-footer">
	    <el-button @click="dialogFormVisible = false">取 消</el-button>
	    <el-button type="primary" @click="submitForm()">确 定</el-button>
	  </div>
	  
	</el-dialog>
	
	
	</div> <br>
	

	
	</div>
</template>


<script>
	
	import {Userinfo,Delete,Updateuserinfo,SearchUserinfo,Role,addRole} from '../../api/api.js'
	export default{
		data(){
			return{
				options: [{
					id:'',
					name:''
				}],
				value1: [],
				tableData: '',
				input:'',
				dialogFormVisible: false,
				udialogFormVisible: false,
				uid:'',
				password:'',
				form: {
				  username: '',
				  password: '',
				  mobile: '',
				  weixinid: '',
				  email: '',
				  region: '',
				  date1: '',
				  date2: '',
				  delivery: false,
				  type: [],
				  resource: '',
				  desc: ''
				},
				formLabelWidth: '120px'
			}
		},
		mounted() {
		            this.mounted();
		        },
		methods:{
			
			addrole(index,row){
				this.value1 = []
				 for(var i in row['ro_user']){
					 this.value1.push(parseInt(row['ro_user'][i].role_id))
				 }
				 
				this.udialogFormVisible = true
				this.form = row
				this.uid = row.id
				Role()
				.then(resp=>{
					this.options = resp
					
				})
				.catch(err => {
					this.$message({
					  type: 'info',
					  message: '搜索异常'
						
					})
				});
			},
			AddRole(){
				addRole({'uid':this.uid,'r_id':this.value1})
				.then(resp=>{
					this.$message({
					  type: 'info',
					  message: '添加成功'
						
					})
					this.mounted();
				})
				.catch(err => {
					this.$message({
					  type: 'info',
					  message: '添加失败'
						
					})
				});
				this.udialogFormVisible=false;
				
			},
			search(){
				SearchUserinfo({'content':this.input})
				.then(resp=>{
					this.$message({
					
					  type: 'info',
					  message: '搜索成功'
					});
					this.tableData = resp
					
				})
				.catch(err => {
					this.$message({
					  type: 'info',
					  message: '搜索异常'
						
					})
				});
			},
		
			
			updateuserinfo(index,row){
				this.dialogFormVisible = true;
				this.form = row
				this.uid = row.id
				this.password = row.password
				
				
			},
			
			submitForm() {
				
				
				var params = {
							'username':this.form.username,
							'password':this.password,
							'mobile':this.form.mobile,
							'weixinid':this.form.weixinid,
							'email':this.form.email,
							'uid': this.uid,
				}
				console.log(params)
				Updateuserinfo(params)
				.then(resp=>{
					this.$message({
					
					  type: 'info',
					  message: '修改成功'
					});
					this.mounted();
				})
				.catch(err => {
					this.$message({
					  type: 'info',
					  message: '修改失败'
						
					})
				});
				this.dialogFormVisible=false;
			},
			
			  handleDelete(index, row) {     //删除
				 
				  this.$confirm('是否删除当条信息','确认信息', {
					  distinguishCancelAndClose: true,
					  confirmButtonText: '删除',
					  cancelButtonText: '取消删除'
				  })
				
				  .then(() => {
					  
					  Delete({'uid':row.id})
					  .then(resp=>{
						  this.$message({
						  
						    type: 'info',
						    message: '删除成功'
						  });
						  this.mounted()
					  })
						.catch(err => {
							this.$message({
							  type: 'info',
							  message: '删除失败'
								
							})
						});
					 
					
				  })
				  .catch(action => {
					this.$message({
					  type: 'info',
					  message: action === 'cancel'
						? '放弃删除'
						: '停留在当前页面'
					})
				  });
				// console.log(index, row);
			  },
			  
			mounted(){
				Userinfo().then(resp=>{
					this.tableData = resp
					
				}).catch(err=>{
					console.log(err.status)
				})
			}
			
		},
		resetForm(formName) {
		  this.$refs[formName].resetFields();
		}
				
	}
</script>

<style>
  body {
    margin: 0;
  }
</style>

<template>
	<div>
		<br>
		<div>
			 <el-button type="primary" @click = "cdialogFormVisible = true">添加角色</el-button> 
		</div>
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
	    width="180">
	  </el-table-column>
 
      <el-table-column
      label="姓名"
      width="280">
      <template slot-scope="scope">
        <el-popover trigger="hover" placement="top">
          角色: <p v-for="i in scope.row.user_name">{{ i.username }}</p>
		  部门: <p v-for="i in scope.row.user_name">
			<span v-for="i in i.de">
				{{ i.name }}
			</span>
		  </p>
          <div slot="reference" class="name-wrapper">
            <el-tag size="medium">{{ scope.row.name }}</el-tag>
          </div>
        </el-popover>
      </template>
    </el-table-column>
	  
	  <el-table-column
	    prop="zh_name"
	    label="真实姓名"
	    width="280">
	  </el-table-column>
	  
      <el-table-column
        prop="description"
        label="概述"
		width="280">
      </el-table-column>
	  

	
	
	 <el-table-column label="操作">
		 
		  
      <template slot-scope="scope">
        <el-button
          size="mini"
          @click="updaterole(scope.$index, scope.row)">编辑</el-button>
        <el-button
          size="mini"
          type="danger"
          @click="handleDelete(scope.$index, scope.row)">删除</el-button>
      </template>
    </el-table-column>
	
	  
    </el-table>


	<!-- 添加角色 -->
	<!-- <el-dialog title="添加角色" :visible.sync="udialogFormVisible">  
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
		
	  </el-form> -->
	  
<!-- 	  <div slot="footer" class="dialog-footer">
	    <el-button @click="udialogFormVisible = false">取 消</el-button>
	    <el-button type="primary" @click="AddRole">确 定</el-button>
	  </div> -->
	  
	</el-dialog>
	
	<!-- 添加 -->
	<el-dialog title="添加信息" :visible.sync="cdialogFormVisible">
	  <el-form :model="form"  style='width: 650px;'>
	    <el-form-item label="真实姓名" :label-width="formLabelWidth">
	      <el-input v-model="form.zh_name" autocomplete="off"></el-input>
	    </el-form-item>
		<el-form-item label="角色名称" :label-width="formLabelWidth">
		  <el-input  v-model="form.name" autocomplete="off"></el-input>
		</el-form-item>
		<el-form-item label="概述" :label-width="formLabelWidth">
		  <el-input v-model="form.description" autocomplete="off"></el-input>
		</el-form-item>
		
	  </el-form>
	  <div slot="footer" class="dialog-footer">
	    <el-button @click="cdialogFormVisible = false">取 消</el-button>
	    <el-button type="primary" @click="createrole">确 定</el-button>
	  </div>
	  
	</el-dialog>
	
	
	<!-- 修改 -->
	<el-dialog title="修改信息" :visible.sync="dialogFormVisible">
	  <el-form :model="form"  style='width: 650px;'>
		  
	   <el-form-item label="真实姓名" :label-width="formLabelWidth">
	     <el-input v-model="form.zh_name" autocomplete="off"></el-input>
	   </el-form-item>
	   <el-form-item label="角色名称" :label-width="formLabelWidth">
	     <el-input  v-model="form.name" autocomplete="off"></el-input>
	   </el-form-item>
	   <el-form-item label="概述" :label-width="formLabelWidth">
	     <el-input v-model="form.description" autocomplete="off"></el-input>
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
	
	import {Roleinfo,DeleteRoleinfo,UpdateRoleinfo,CreateRoleinfo,SearchRoleinfo,Role,addRole} from '../../api/api.js'
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
				cdialogFormVisible: false,
				dialogFormVisible: false,
				udialogFormVisible: false,
				rid:'',
				password:'',
				form: {
				  zh_name: '',
				  name: '',
				  description: '',
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
			
			search(){
				SearchRoleinfo({'content':this.input})
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
			
			createrole(){
				var params = {
							'zh_name':this.form.zh_name,
							'name':this.form.name,
							'description':this.form.description,
							}
				console.log(params)
				CreateRoleinfo(params)
				.then(resp=>{
					this.$message({
					
					  type: 'info',
					  message: '添加成功'
					});
					
					this.mounted();
					
				})
				.catch(err => {
					this.$message({
					  type: 'info',
					  message: '添加失败'
						
					})
				});
				this.cdialogFormVisible=false;
				
			},
			
			updaterole(index,row){
				this.dialogFormVisible = true;
				this.form = row
				this.rid = row.id
					
			},
			
			submitForm() {
				
				
				var params = {
							'zh_name': this.form.zh_name,
							'name': this.form.name,
							'description': this.form.description,
							'rid': this.rid,
				}
				console.log(params)
				UpdateRoleinfo(params)
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
					  
					  DeleteRoleinfo({'rid':row.id})
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
				// var params = {'Authorization':localStorage.getItem('token')}
				Roleinfo().then(resp=>{
					this.tableData = resp
					console.log(resp)
					
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

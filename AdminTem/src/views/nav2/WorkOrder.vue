<template>
	<div>  <br>
	
		<div>
			<el-input
			placeholder="请输入内容"
			v-model="input"
			clearable style='width: 200px;'>
			</el-input>
			<el-button type="primary" icon="el-icon-search" @click="search()">搜索</el-button>
			
			 <el-button type="primary" @click = "cdialogFormVisible = true">创建工单</el-button> 
		</div>	  <br>
		
		
		<div>
			<el-table
			  :data="tableData"
			  style="width: 100%"
			   >
			
			<el-table-column
			    prop="id"
			    label="工单id"
			    width="180">
			  </el-table-column>
			 
			  <el-table-column
			  label="姓名"
			  width="280">
			  <template slot-scope="scope">
			    <el-popover trigger="hover" placement="top">
			      创建人: <p v-for="i in scope.row.creater_user">{{ i.username }}</p>
				  
			      <div slot="reference" class="name-wrapper">
			        <el-tag size="medium">{{ scope.row.name }}</el-tag>
			      </div>
			    </el-popover>
			  </template>
			</el-table-column>
			  
			  <el-table-column
			    prop="callback"
			    label="回调"
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
			        @click="updatework(scope.$index, scope.row)">编辑</el-button>
					
					<el-button
					  size="mini"
					  @click="ActionConf(scope.$index, scope.row)">审批流设置</el-button>
									
			    </template>
			  </el-table-column>
			
			</el-table>
			
			
			<!-- 新建工单 -->
			<el-dialog title="新建工单" :visible.sync="cdialogFormVisible">
			  <el-form :model="form1"  style='width: 650px;'>
			    <el-form-item label="工单名称" :label-width="formLabelWidth">
			      <el-input v-model="form1.name" autocomplete="off"></el-input>
			    </el-form-item>
				<el-form-item label="回调地址" :label-width="formLabelWidth">
				  <el-input  v-model="form1.callback" autocomplete="off"></el-input>
				</el-form-item>
				<el-form-item label="自定义字段" :label-width="formLabelWidth">
				  <el-input  v-model="form1.customfield" autocomplete="off"></el-input>
				</el-form-item>
				<el-form-item label="概述" :label-width="formLabelWidth">
				  <el-input v-model="form1.description" autocomplete="off"></el-input>
				</el-form-item>
				
			  </el-form>
			  <div slot="footer" class="dialog-footer">
			    <el-button @click="cdialogFormVisible = false">取 消</el-button>
			    <el-button type="primary" @click="creatework()">确 定</el-button>
			  </div>
			  
			</el-dialog>
			
			<!-- 修改工单信息 -->
			<el-dialog title="修改工单" :visible.sync="udialogFormVisible">
			  <el-form :model="form"  style='width: 650px;'>
			    <el-form-item label="工单名称" :label-width="formLabelWidth">
			      <el-input v-model="form.name" autocomplete="off"></el-input>
			    </el-form-item>
				<el-form-item label="回调地址" :label-width="formLabelWidth">
				  <el-input  v-model="form.callback" autocomplete="off"></el-input>
				</el-form-item>
				<el-form-item label="自定义字段" :label-width="formLabelWidth">
				  <el-input  v-model="form.customfield" autocomplete="off"></el-input>
				</el-form-item>
				<el-form-item label="概述" :label-width="formLabelWidth">
				  <el-input v-model="form.description" autocomplete="off"></el-input>
				</el-form-item>
				
			  </el-form>
			  <div slot="footer" class="dialog-footer">
			    <el-button @click="udialogFormVisible = false">取 消</el-button>
			    <el-button type="primary" @click="submitForm()">确 定</el-button>
			  </div>
			  
			</el-dialog>
		</div>
	</div>
</template>

<script>
	import {CreateWork,WorkOrder,UpdateWork,SearchWork} from "../../api/api.js"
	export default{
		data() {
			return {
				cdialogFormVisible:false,
				udialogFormVisible:false,
				tableData: '',
				input:'',
				wid:'',
				form: {
				  name: '',
				  callback: '',
				  creater: '',
				  customfield: '',
				  description: '',
				  region: '',
				  date1: '',
				  date2: '',
				  delivery: false,
				  type: [],
				  resource: '',
				  desc: ''
				},
				form1: {
				  name: '',
				  callback: '',
				  creater: '',
				  customfield: '',
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
		methods: {
			ActionConf(index,row){
				this.wid = row.id;
				
				this.$router.push({
					path: '/flowroleconf',
					query: {
					  wid:this.wid
					}
				  })
				
			},
			search(){
				
				SearchWork({'content':this.input})
				
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
					  message: '搜索失败'
						
					})
				});
			},
			updatework(index,row){
				this.udialogFormVisible = true,
				this.form = row
				this.wid = row.id
			},
			submitForm(){
				var params = {
							'name':this.form.name,
							'callback':this.form.callback,
							'customfield':this.form.customfield,
							'description':this.form.description,
							'wid':this.wid
							}
							console.log(params)
				UpdateWork(params)
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
				this.udialogFormVisible=false;
			},
			
			// 'Authorization':localStorage.getItem('token'),
			creatework(){
				var params = {
							'token':localStorage.getItem('token'),
							'name':this.form1.name,
							'callback':this.form1.callback,
							'customfield':this.form1.customfield,
							'description':this.form1.description,
							}
							console.log(params)
				CreateWork(params)
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
			mounted(){
				
				// var params = {'Authorization':localStorage.getItem('token')}
				WorkOrder().then(resp=>{
					this.tableData = resp		
				}).catch(err=>{
					console.log(err.status)
				})
			},
		},
		
	}
</script>

<style>
</style>

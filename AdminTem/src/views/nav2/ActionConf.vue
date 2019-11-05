<template>
	<div>
		<br> <br>	
		<el-form ref="form" :model="form" label-width="80px">
			
		<el-form-item label="池审批">
		<el-switch
		  v-model="value3"
		  @change='pool'
		  >
		</el-switch>
		</el-form-item>
			
		<el-form-item label="审批序号">
		<el-input-number v-model="num" controls-position="right" @change="handleChange" :min="1" :max="10"></el-input-number>	
		</el-form-item>
		
		
		<el-form-item label="审批方式">
		
			  	<el-select v-model="value1" placeholder="请选择">
					<el-option
					  v-for="item in options"
					  :key="item.id"
					  :label="item.name"
					  :value="item.id">
					</el-option>
				  </el-select>
		
			&nbsp;&nbsp;&nbsp; <!-- 用户审批 -->
		</el-form-item>
		
		<el-form-item label="审批类型" >
			<el-tag>{{value1}}</el-tag>
			<!-- <el-input  style='width: 250px;' :disabled="true" v-model="form.atype" autocomplete="off"></el-input> -->
		</el-form-item>
				
		<el-form-item label="自动化">
			<el-switch
			  v-model="value"
			  >
			</el-switch>
		</el-form-item>		
				
		<el-form-item>
		<el-button type="primary" size="medium" @click="onSubmit">立即创建</el-button>
		<el-button size="medium" @click="cancel">取消</el-button>
		</el-form-item>

		
		
		</el-form>
	</div>
</template>

<script>
	import {ActionRoleinfo,ActionUserinfo,AddActionFlow} from "../../api/api.js"
	export default{
		data() {
			return {
				 value3:false,
				 visible :false,
				 value:false,
				 ru_id:'',
				 num: 1,
				 AS:'',
				 radio1: true,
				 value1: [],
				 
				 options: [{
					  id: '',
					  name: '',
				}],
				
				
				 form: {
					  atype:'',
					  name: '',
					  region: '',
					  date1: '',
					  date2: '',
					  type: [],
					  resource: '',
					  desc: ''
					},
			}
		},
		mounted(){
			this.mounted()
		},
		methods: {
			
			mounted(){
				ActionUserinfo()
				.then(resp=>{
					this.options = resp
					
				})
				.catch(err => {
					this.$message({
					  type: 'info',
					  message: '获取数据异常'
						
					})
				});
			},
			
			pool(){
				if (this.value3 == true) {
					ActionRoleinfo()
					.then(resp=>{
						this.options = resp
						
					})
					.catch(err => {
						this.$message({
						  type: 'info',
						  message: '获取数据异常'
							
						})
					});
				} else {
					this.mounted()
				}
			},
			
	
			onSubmit(){
				var params = {
					'approvetorole':this.value3,
					'approve_type_id':this.value1,
					'wid':this.$route.query.wid,
					'sequence':this.num,
					'is_auto':this.value
				}
			
				AddActionFlow(params)
				.then(resp=>{
					console.log(resp)
					if (resp.code == 200) {
						this.$router.push({
							path: '/flowroleconf',
							query: {
							  wid:this.$route.query.wid,
							}
						})
					} else{
						this.$message({
						  type: 'info',
						  message: resp.message
						})
					}
					
				})
				.catch(err => {
					this.$message({
					  type: 'info',
					  message: '添加流程异常'
						
					})
				});
			},
			cancel(){
				this.$router.push({
					path: '/flowroleconf',
					query: {
					  wid:this.$route.query.wid,
					}
				})
			}
		}
	}
</script>

<style>
</style>

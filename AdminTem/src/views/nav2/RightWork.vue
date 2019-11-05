<template>
	<div>
		
		<div>
			<div class="detail">
			<i class="el-icon-success" style="font-size: 25px; color: #409EFF; margin-left: 10px;
			margin-top: 5px;" ></i>
			<span style="font-size: 18px; ">审批流程</span>
			</div>
			
			<br>
			
				<el-steps :active="active" space="20%" style="margin-left: 20px;">
				  <el-step :title="step.role_user" v-for="(step,key) in flow_step" :key="key"></el-step>
				</el-steps>
		
			
			<br>
			
				
			<div v-for="item in data">
			
			<p  class="flow" style="font-size: 15px; color: #FFFFFF;">指定人员: <span v-for="s in item.users">{{s}}&nbsp;&nbsp;</span></p>
			
			<br>
			<table style="margin-left: 20px;">
				<tr>
					<td style="width: 180px;">子工单ID</td>
					<td style="width: 180px;" v-if="item.dispose">操作人员</td>
					<td style="width: 180px;" v-if="item.action">操作人员</td>
					<td style="width: 180px;">工单状态</td>
					<td style="width: 180px;">操作</td>
				</tr>
				<br>
				<tr>
					<td>{{item.id}}</td>
					<td v-if="item.dispose">{{item.dispose_user}}</td>
					<td v-if="item.action">{{item.dispose_user}}</td>
					<td>{{item.suborder_status}}</td>
					<td>
						<el-button v-if="item.examine" @click="handleClick(item.id)" type="text" size="small">审批</el-button>
						<i v-if="item.dispose" class="el-icon-circle-check" style="color: #13CE66;">通过</i>
						<i v-if="item.action" class="el-icon-circle-close" style="color: red;">拒绝</i>
					</td>
				</tr>
			</table>
			
			
			</div>
			
			
			
		</div>
		<el-dialog title="审批" :visible.sync="udialogFormVisible"> 
		  <el-form :model="form"  style='width: 650px;'>
		    <el-input
			  type="textarea"
			  :rows="2"
			  placeholder="审批意见"
			  v-model="textarea">
			</el-input>
			
		  </el-form>
		  <div slot="footer" class="dialog-footer">
		    <el-button @click="refuse">拒 绝</el-button>
		    <el-button type="primary" @click="pass">通 过</el-button>
		  </div>
		  
		</el-dialog>
		
		
		
			
	</div>
</template>

<script>
	import {DetailSuborder,PassSuborder,RefuseSuborder} from "../../api/api.js"
	export default{
		data() {
			return {
				examin:true,
				sid:'',
				textarea:'',
				data:'',
				active: '',
				flow_step:'',
				dispose:false,
				udialogFormVisible:false,
				form: {
				  name: '',
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
			mounted(){
				DetailSuborder({'wid':this.$route.params.id,'token':localStorage.getItem('token')})
				.then(resp=>{
					
					this.active = resp['data']['active']
					this.data = resp['data']['data']
					this.flow_step = resp['data']['options']
					
					console.log(resp)
				
					for (var i in resp['data']['data']){
						if (resp['data']['data'][i]['id'] != resp['examin']) {
							resp['data']['data'][i]['examine'] = false
						} 
					}
		
				})
				.catch(err => {
					this.$message({
					  type: 'info',
					  message: '数据异常'
					})
				});
			},
			handleClick(row) {
				this.udialogFormVisible=true;
				this.sid = row;
			},
			pass(){
				var params = {
					wid : this.$route.params.id,
					sid : this.sid,
					textarea : this.textarea,
					token : localStorage.getItem('token')
				}
				console.log(params)
				PassSuborder(params)
				.then(resp=>{	
				
					this.mounted();
					this.udialogFormVisible = false
				
				
				})
				.catch(err => {
					this.$message({
					  type: 'info',
					  message: '审批失败'
						
					})
				});
			},
			refuse(){
				var params = {
					wid : this.$route.params.id,
					sid : this.sid,
					textarea : this.textarea,
					token : localStorage.getItem('token')
				}
				console.log(params)
				RefuseSuborder(params)
				.then(resp=>{				
					this.mounted()
				})
				.catch(err => {
					this.$message({
					  type: 'info',
					  message: '拒绝异常'
						
					})
				});
			}
		},
	}
</script>

<style scoped>
	.detail{
		background: #EBEEF5;
		
		width: 1000px;
		height: 35px;
		border: 1px;
		border-radius: 30px;
	};
	.flow{
		margin-left: 20px;
		background: #409EFF;
		width: 600px;
		height: 20px;
		border: 1px;
		border-radius: 4px;
	}
</style>
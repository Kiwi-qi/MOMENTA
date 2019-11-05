<template>
	<div>
		
		
		<div class="headers">
		<i class="el-icon-document-copy" style="font-size: 25px; color: #409EFF; margin-left: 10px;
		margin-top: 5px;" ><span class="title">工单详情</span></i>
		
		</div>
				 

		<br>
		<div class="detail" :model="data">
			<span>#工单名称</span>
			<span style="margin-left: 300px;">{{data.flowconf}}</span>
			<el-divider></el-divider>
			<span>#创建时间</span>
			<span style="margin-left: 300px;">{{data.create_ts}}</span>
			<el-divider></el-divider>
			<span>#用户email</span>
			<span style="margin-left: 300px;">{{data.create_user_email}}</span>
			<el-divider></el-divider>
			<span>{{data.parameter.verbos_name}}</span>
			<span style="margin-left: 300px;">{{data.parameter.ruleForm}}</span>
			<el-divider></el-divider>
		</div>
			
	</div>
</template>

<script>
	import {DetailWorker} from "../../api/api.js"
	export default{
		data() {
			return {
				data:'',
			}
		},
		mounted() {
		            this.mounted();
		        },
		methods: {
			mounted(){
				DetailWorker({wid:this.$route.params.id})
				.then(resp=>{
					this.data = resp
				})
				.catch(err => {
					this.$message({
					  type: 'info',
					  message: '数据异常'
						
					})
				});
				
			}
		}
	}
</script>

<style scoped>
	
	.headers{
		background: #EBEEF5;
		width: 1000px;
		height: 35px;
		border: 1px;
		border-radius: 30px;
	};
	.title{
		font-size: 18px; 
		color: #000000;
		margin-left: 5px;
	};
	.detail{
		width: 600px;
		font-size: 12px;
		margin-left: 20px;
		
	};
	el-divider{
		margin-top: 10px;
	}
</style>

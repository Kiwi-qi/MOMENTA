<template>
    <div class="template-table">
        <el-row :gutter="20" style="margin-top: 10px">
            <el-col :span="6" v-for="(tpl,key)  in templateList" :key="key">
                <el-button size="medium">
                    <router-link :to="'/index/' + tpl.id" v-text="tpl.name"
                                 style="display: inline-block;width: 100%;height: 100%;color: #0366d6;">
                    </router-link>
                </el-button>
            </el-col>
        </el-row>
    </div>
</template>

<script>
	import {WorkOrder} from "../../api/api.js"
    export default {
        data () {
            return {
                templateList:  [{
                    "id": '',
                    "name": ""
                }]
            }
        },
		mounted(){
			this.mounted()
		},
		methods: {
			mounted() {
				WorkOrder()
				.then(resp=>{
					console.log(resp)
					this.templateList = resp
					
				})
				.catch(err => {
					this.$message({
					  type: 'info',
					  message: '获取数据异常'
						
					})
				});
			}
		},
    }

</script>

<style scoped>
    .template-table{
        margin-top: 20px;
    }
    a{ text-decoration:none;}
    .el-row {
        margin-bottom: 14px;
    &:last-child {
         margin-bottom: 0;
     }
    }
    .el-button{
        width: 100%;
        border:1px solid gray;
        background-color: #FAFFFF;
        margin-bottom: 10px;
    }
</style>

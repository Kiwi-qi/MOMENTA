<template>
	
    <div style="margin-left: 20px">
		<br>
        <el-row>
            <div style="margin-top: 6px;margin-bottom: 16px">
                <el-row>
                    <el-button type="primary" style="float: left;margin-right: 50px" @click="handleAdd()">
                        <i class="el-icon-plus"></i>
                        &nbsp;添加审批流</el-button>
                </el-row>

            </div>
        </el-row>

        <!--2、table展示页-->
        <el-table
                :data="flowconfRole"
                style="width: 100%">
            <el-table-column
                    label="审批序号"
                    width="120">
                <template slot-scope="scope">
                    <span style="margin-left: 10px">{{ scope.row.sequence }}</span>
                </template>
            </el-table-column>

            <el-table-column
                    label="审批方式"
                    width="140">
                <template slot-scope="scope">
                    <span style="margin-left: 10px">{{ scope.row.approvetype }}</span>
                </template>
            </el-table-column>

            <el-table-column
                    label="是否审批组审批"
                    width="140">
                <template slot-scope="scope">
                    <span style="margin-left: 10px">{{ scope.row.approvetorole }}</span>
                </template>
            </el-table-column>

            <el-table-column
                    label="是否自动化工单"
                    width="140">
                <template slot-scope="scope">
                    <span style="margin-left: 10px">{{ scope.row.is_auto }}</span>
                </template>
            </el-table-column>

            <el-table-column
                    label="自动化配置详情"
                    :show-overflow-tooltip="true"
                    width="140">
                <template slot-scope="scope">
                    <span style="margin-left: 10px">{{ scope.row.url }}</span>
                </template>
            </el-table-column>

            <el-table-column label="操作">
                <template slot-scope="scope">
                    <el-button
                            size="mini"
                            type="primary"
                            @click="handleEdit(scope.row.id)"><i class="el-icon-edit"></i> 修改</el-button>
                    <el-button
                            size="mini"
                            type="danger"
                            @click="handleFlowRoleConfMethod(scope.row.id)"><i class="el-icon-delete"></i> 删除</el-button>

                    <el-button
                            v-if="scope.row.is_auto"
                            size="mini"
                            type="info"
                            @click="configAutoFlowRoleConf(scope.row.id, scope.row.is_auto)"><i class="el-icon-setting"></i> 配置自动化</el-button>
                </template>
            </el-table-column>
        </el-table>

        <!--3、模态对话框，自动化工单配置-->
        <el-row>
            <el-dialog
                    title="配置自动化工单"
                    :visible.sync="centerDialogVisible"
                    width="30%"
                    center>
                <el-form label-position="left" label-width="100px" :model="formLabelAlign">
                    <el-form-item label="自动化url">
                        <el-input v-model="formLabelAlign.url" placeholder="自动化url"></el-input>
                    </el-form-item>
                    <el-form-item label="超时时间" >
                        <el-input-number v-model="formLabelAlign.timeout" :min="10" :max="3600" label="描述文字"></el-input-number>
                    </el-form-item>

                    <el-form-item label="Method">
                        <el-select v-model="formLabelAlign.method" placeholder="选择自动化请求方法" required>
                            <el-option label="get" value="get"></el-option>
                            <el-option label="post" value="post"></el-option>
                        </el-select>
                    </el-form-item>
                </el-form>
                <span slot="footer" class="dialog-footer">
					
        <el-button @click="centerDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleModifyFlowRoleConf()">确 定</el-button>
      </span>
            </el-dialog>
        </el-row>
    </div>


</template>

<script>
	import {UserAction,AddAutomation,DeleteActionFlow} from "../../api/api.js"
    export default {
        data() {
            return {
                formLabelAlign: {
                    url: '',
                    timeout: '',
                    method: '',
                    autoactionconf_id: '',
					
                },
			
                centerDialogVisible: false,
                flowconfRole: [{
					"id":"",
                    "flowconf":"",
                    "sequence": '',
                    "approvetype": "",
                    "approvetorole": '',
                    "is_auto": '',
					"url":'',
                }]
            }
        },
        methods: {
            handleEdit (flowroleconfid) {
                this.$router.push({
                	path: '/upactionConf',
                	query: {
                	  wid:this.$route.query.wid,
					  nid:flowroleconfid
                	}
                })
            },
            handleAdd(flowroleconfid){
                this.$router.push({
					path: '/actionconf',
					query: {
					  wid:this.$route.query.wid
					}
				})
            },
            handleDelete (index, row) {
                console.log(index, row);
            },
            handleFlowRoleConf () {
				UserAction({'wid':this.$route.query.wid})
				.then(resp=>{
					this.flowconfRole = resp[0]['actionconf']
					console.log(this.flowconfRole)
				})
				.catch(err => {
					this.$message({
					  type: 'info',
					  message: '获取数据异常'
						
					})
				});

            },

            handleFlowRoleConfMethod (flowroleconfid) {
				DeleteActionFlow({'nid':flowroleconfid})
				.then(resp=>{
					this.$message({
					
					  type: 'info',
					  message: '删除成功'
					});
					this.handleFlowRoleConf()
					
				})
				.catch(err => {
					this.$message({
					  type: 'info',
					  message: '删除异常'
						
					})
				});
            },

            configAutoFlowRoleConf (flowroleconfid, _is_auto) {
                this.centerDialogVisible = true
				this.formLabelAlign.autoactionconf_id = flowroleconfid
            },
			
            handleModifyFlowRoleConf () {
				var params = {
					'url' : this.formLabelAlign.url,
					'timeout' : this.formLabelAlign.timeout,
					'method' : this.formLabelAlign.method,
					'autoactionconf_id' : this.formLabelAlign.autoactionconf_id
				};
				console.log(params)
				AddAutomation(params)
				.then(resp=>{
					if (resp.code == 200) {
						this.$message({
						
						  type: 'info',
						  message: resp.message
						});
						this.handleFlowRoleConf();
						this.centerDialogVisible = false;
						
					} else{
						this.$message({
						
						  type: 'info',
						  message: resp.message
						});
					}
					
				})
				.catch(err => {
					this.$message({
					  type: 'info',
					  message: '添加自动化异常'
						
					})
				});
				
            }
        },

        created () {
            this.handleFlowRoleConf()
        }
    }
</script>

<style scoped>

</style>

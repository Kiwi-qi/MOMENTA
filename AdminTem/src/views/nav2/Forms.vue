<template>
    <div class="create-order-form">
        <el-col :span="24">
            <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="150px" label-position="top" class="demo-ruleForm"
                     :validate-on-rule-change="false">

                <el-form-item v-for="(field,key)  in field_list" :key="key"
                              :label="field.verbos_name" :prop="field.name">
                    <!--1、input-->
                    <el-input v-model="field.value" v-if="field.field_type === 'input'"
                              :placeholder="field.msg"
                              @change.native.prevent="addDataBind()" :disabled="field.is_disabled">
                    </el-input>

                    <!--2、select-->
                    <el-select filterable v-model="field.value" :placeholder="field.msg" v-if="field.field_type === 'select'" style="min-width: 300px"
                               :disabled="field.is_disabled" @change="addDataBind()">
                        <el-option v-for="(select_val,key)  in field.field_datasource" :key="key" :label="select_val"
                                   :value="select_val" @change="addDataBind()"></el-option>
                    </el-select>

                    <!--2.1、mulselect-->
                    <el-select  filterable v-model="field.value" :placeholder="field.msg" v-if="field.field_type === 'mulselect'" style="min-width: 300px"
                                multiple :disabled="field.is_disabled" @change="addDataBind()">
                        <el-option v-for="(select_val,key)  in field.field_datasource" :key="key" :label="select_val"
                                   :value="select_val" @change="addDataBind()"></el-option>
                    </el-select>

                    <!--3、switch (button按钮标签)-->
                    <el-switch v-model="field.value" v-if="field.field_type === 'switch'" :disabled="field.is_disabled"></el-switch>

                    <!--4、checkbox (多选)-->
                    <el-checkbox-group  v-model="field.value" v-if="field.field_type === 'm_checkbox'" :disabled="field.is_disabled">
                        <el-checkbox v-for="(select_val,key)  in field.field_datasource" :key="key" :label="select_val"
                                     name="type" @click.native.prevent="addValToBind(field.name, select_val)"></el-checkbox>
                    </el-checkbox-group>

                    <!--5、checkbox (单选)-->
                    <el-radio-group v-model="field.value" v-if="field.field_type === 'only_checkbox'" :disabled="field.is_disabled">
                        <el-radio v-for="(select_val,key)  in field.field_datasource" :key="key" :label="select_val"
                                  @change.native.prevent="addDataBind()"></el-radio>
                    </el-radio-group>

                    <!--6、textarea (多行输入)-->
                    <el-input autosize type="textarea" v-model="field.value" :placeholder="field.msg" :disabled="field.is_disabled"
                              :autosize="{ minRows: 6, maxRows: 20}" v-if="field.field_type === 'textarea'" @change.native.prevent="addDataBind()">
                    </el-input>

                    <!--7、级联选择器-->
                    <el-cascader
                            v-if="field.field_type === 'cascader'"
                            :options="field.field_datasource"
                            v-model="field.value"
                            :placeholder="field.msg"
                            :disabled="field.is_disabled"
                            @change="handleChange">
                    </el-cascader>

                    <!--8、kvselect-->
                    <el-select filterable v-model="field.value" :placeholder="field.msg" v-if="field.field_type === 'kvselect'" style="min-width: 300px"
                               :disabled="field.is_disabled" @change="addDataBind()">
                        <el-option v-for="(select_val,key)  in field.field_datasource" :key="key" :label="select_val.label"
                                   :value="select_val.value" @change="addDataBind()"></el-option>
                    </el-select>

                </el-form-item>


                <el-form-item style="margin-bottom: 40px">
                    <h3>审批流程</h3>
                    <el-steps :active="0" finish-status="success">
                        <el-step :title="step" v-for="(step,key) in flow_step" :key="key"></el-step>
                    </el-steps>
                </el-form-item>

                <!--提交按钮-->
                <el-form-item>
                    <el-button type="primary" @click="submitForm('ruleForm')" style="min-width: 50px;max-width: 180px;background-color: #409eff;">创建工单</el-button>
                    <el-button @click="resetForm('ruleForm')" style="min-width: 50px;max-width: 180px">重置</el-button>
                </el-form-item>
            </el-form>
        </el-col>
    </div>
</template>

<script>
	import {InitFormConf,InitFlowStepInfo,InstantiationWorkOrder} from "../../api/api.js"
    export default {
        data() {
            return {
                field_list:[],
                ruleForm: {},
                rules: {},
                flow_step:[],
            };
        },
		
        methods: {
            //1、submitForm：提交表单
            submitForm(formName) {
                this.addDataBind();
                this.$refs[formName].validate((valid) => {
                    if (valid) {
						console.log(this.ruleForm)
						var params = {
							fid : this.$route.params.id,
							description: this.ruleForm.flowconf_desc,
							parameter : this.ruleForm.parameter,
							token:localStorage.getItem('token')
						}
						console.log(params)
						InstantiationWorkOrder(params)
						.then(resp=>{
							if (resp.code == 200) {
								this.$message({
								  type: 'info',
								  message: 'ok'	,
								})
								this.$router.push({path:'/applyorder'})
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
							  message: '实例化工单异常'
								
							})
						});
                        
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },

            //2、resetForm：重置表单中输入数据
            resetForm(formName) {
                for(var i=0;i<this.field_list.length;i=i+1){
                    const fileld_dic = this.field_list[i];
                    const inp_val = fileld_dic['value'];
                    const field_name = fileld_dic['name'];
                    var not_reset_fields = ['workorder_name','mydeptpath'];
                    var val_type = typeof inp_val;
                    if(not_reset_fields.indexOf(field_name) == -1){
                        switch (val_type)
                        {
                            case "boolean":
                                fileld_dic['value'] = false;
                                break;
                            case "string":
                                fileld_dic['value'] = '';
                                break;
                            case "object":
                                fileld_dic['value'] = [];
                                break;
                            default:
                                fileld_dic['value'] = '';
                        }
                    }
                }
                this.$refs[formName].resetFields();
            },

            //3、addDataBind：将 field_list 各字典的value值赋值给 ruleForm
            addDataBind: function () {
                console.log(9999999999999999999999999)
                for(var i in this.ruleForm){
                    const val = this.getInputValue(i);
                    this.ruleForm[i] = val;
                }
            },

            //4、getInputValue：找到 ruleForm 中key对应的值
            getInputValue:function (key) {
                for(var i=0;i<this.field_list.length;i=i+1){
                    const fileld_dic = this.field_list[i];
                    const k1 = fileld_dic['name'];
                    if(key == k1){
                        return fileld_dic['value']
                    }
                }
                return ''
            },

            //5、addValToBind：checkbox(多选) 将field_list中个value值赋值给 ruleForm
            addValToBind:function (m_ckeck_key, val) {
                for(var i=0;i<this.field_list.length;i=i+1){
                    const fileld_dic = this.field_list[i];
                    const k1 = fileld_dic['name'];
                    if(m_ckeck_key == k1){
                        var is_in_list = fileld_dic['value'].indexOf(val);
                        if(is_in_list > -1){  // 证明这个值已经在列表中，删除
                            fileld_dic['value'] = fileld_dic['value'].splice(is_in_list,is_in_list)
                        }else {
                            fileld_dic['value'].push(val)
                        }
                        this.addDataBind();  // 将 field_list中个value值赋值给 ruleForm
                    }
                }
            },

            // 级联选择器 值改变调用此方法
            handleChange(value) {
                console.log(value);
                this.addDataBind();
            },

            //6、vue生命周期的created时调用这个函数生成表单
            InitFormConf () {
			
				InitFormConf({'id':this.$route.params.id})
				.then(resp=>{
					var response = resp
					this.field_list = response.data.field_list;
					this.ruleForm = response.data.ruleForm;
					this.rules = response.data.rules;
				})
				.catch(err => {
					this.$message({
					  type: 'info',
					  message: '获取数据异常'
						
					})
				});
                
                
            },

            //7、获取工单执行审批步骤
            InitFlowStepInfo () {
				InitFlowStepInfo({'id':this.$route.params.id})
				.then(resp=>{
					
					var response = resp.data
					this.flow_step = response.data.flow_step;
				})
				.catch(err => {
					this.$message({
					  type: 'info',
					  message: '111'
						
					})
				});
                

                
            },
        },

        created () {
            this.InitFormConf();
            this.InitFlowStepInfo()
        },
    }
</script>

<style scoped>
    .create-order-form {
        margin-top: 30px;
    }
    .upfile {
        /*margin-top: 10px;*/
        min-height: 200px;
        background-color: #F8F8F8;
    }
    .upfile-div {
        /*margin-top: 10px;*/
        margin-left: 20px;
    }
</style>

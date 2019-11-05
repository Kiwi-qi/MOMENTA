<template>
    <div class="approving-order">
        <div class="search-div">
            <div class="search-block">
                <el-date-picker
                        v-model="listQuery.startTime"
                        type="date"
                        value-format="yyyy-MM-dd"
                        placeholder="开始日期">
                </el-date-picker>
            </div>

            <div class="search-block">
                <el-date-picker
                        v-model="listQuery.endTime"
                        type="date"
                        value-format="yyyy-MM-dd"
                        placeholder="结束日期">
                </el-date-picker>
            </div>

            <div class="search-block" style="max-width: 120px">
                <el-select v-model="listQuery.actionStatus" placeholder="状态过滤">
                    <el-option
                            v-for="item in options"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                    </el-option>
                </el-select>
            </div>

            <div class="search-block">
                <el-input
                        placeholder="创建者, 工单名称,工单描述"
                        v-model="listQuery.searchContent"
                        style="min-width: 200px"
                        clearable>
                </el-input>
            </div>

            <div class="search-block">
                <el-button style="background-color: #409eff;" type="primary" icon="el-icon-search" @click="getApproveSubOrderList">搜索</el-button>
            </div>
        </div>

        <div class="search-div">
            <div class="search-block">
                <el-button :class="{timeActive:activeList[0]}" type="info" @click="timeFilter('today',0)">今日工单</el-button>
                <el-button :class="{timeActive:activeList[1]}"  type="info" @click="timeFilter('week',1)">最近一周</el-button>
                <el-button :class="{timeActive:activeList[2]}" type="info" @click="timeFilter('month',2)">最近一月</el-button>
            </div>
        </div>

        <div>
            <el-table
                    :data="tableData"
                    v-loading="loading"
                    tooltip-effect="dark"
                    style="width: 100%;"
            >
                <el-table-column
                        prop="id"
                        label="子工单ID"
                        width="90"
                >
                </el-table-column>
                <el-table-column
                        prop="mainorder"
                        label="工单名称"
                        width="180">
                </el-table-column>
            

                <el-table-column
                        prop="create_user"
                        label="创建者">
                </el-table-column>

                <el-table-column
                        prop="approve_user_role"
                        label="审批人">
                </el-table-column>

                <el-table-column
                        prop="action_status"
                        label="工单状态">
                </el-table-column>

                <el-table-column
                        prop="description"
                        :show-overflow-tooltip="true"
                        label="工单描述">
                </el-table-column>

                <el-table-column
                        fixed="right"
                        label=" 操作"
                        width="100">
                    <template slot-scope="scope">
                        <el-button @click="approving(scope.row.wid)" type="text" size="mini">详情</el-button>
                    </template>
                </el-table-column>
            </el-table>


            <div class="tb-pagination">
                <div class="block">
                    <el-pagination
                            @size-change="handleSizeChange"
                            @current-change="handleCurrentChange"
                            :current-page.sync="listQuery.currentPage"
                            :page-sizes="[3,6]"
                            :page-size="listQuery.defaultPageSize"
                            layout="total, sizes, prev, pager, next"
                            :total="listQuery.total">
                    </el-pagination>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
	import {AfterHandle} from "../../api/api.js"
    export default {
        data() {
            return {
                activeList:[false,false,false],
                loading: true,
                tableData: [],
                listQuery:{
                    currentPage: 1,
                    defaultPageSize: 3,
                    total: 100,
                    startTime: '',
                    endTime: '',
                    searchContent: '',
                    actionStatus:'0',
                    timeTag: '',
                },
                options: [{
                    value: '',
                    label: '所有'
                }, {
                    value: '0',
                    label: '待处理'
                }, {
                    value: '1',
                    label: '通过'
                }, {
                    value: '2',
                    label: '退回'
                }, {
                    value: '3',
                    label: '否决'
                }, {
                    value: '4',
                    label: '确认'
                }],
            }
        },
        methods: {
            getApproveSubOrderList () {
                var parms = {
                    'action_status': this.listQuery.actionStatus,
                    'current_page':this.listQuery.currentPage,
                    'per_page_count':this.listQuery.defaultPageSize,
                    'start_time':this.listQuery.startTime,
                    'end_time':this.listQuery.endTime,
                    'search_content':this.listQuery.searchContent,
                    'suborder_status':'1',
                    'time_tag':this.listQuery.timeTag,
                    'manage_page':true,

                };
				var params = {
							'page':this.listQuery.currentPage,
							'pagesize':this.listQuery.defaultPageSize,
							'token':localStorage.getItem("token"),
							'wid':this.$route.params.id,
					}
				AfterHandle(params)
				.then(resp=>{
					
					this.tableData = resp.data
					this.listQuery.total = resp.total
					this.loading = false  // 取消加载
				})
				.catch(err => {
					this.$message({
					  type: 'info',
					  message: '获取数据异常'
						
					})
				});
            },

            // 每页显示多少条
            handleSizeChange (val) {
                this.listQuery.defaultPageSize = val
                this.getApproveSubOrderList()
            },

            // 上一页，下一页：当前页数
            handleCurrentChange (val) {
                this.listQuery.currentPage = val
                this.getApproveSubOrderList()
            },

            approving (id) {
                let routeData = this.$router.resolve({ path: '/workdetail/' + id  })
                window.open(routeData.href, '_blank');
            },

            timeFilter (timeTag,activeNum) {
                this.listQuery.startTime = ''
                this.listQuery.endTime = ''
                this.listQuery.timeTag = timeTag

                var active = this.activeList[activeNum]
                if (active){
                    this.listQuery.timeTag = ''
                    this.activeList[activeNum] = false
                }else {
                    this.activeList = [false,false,false]
                    this.activeList[activeNum] = true
                }

                this.getApproveSubOrderList()
            }
        },

        created(){
            this.getApproveSubOrderList();  // 获取工单
        },
    }
</script>

<style scoped>
    .approving-order{
        margin-left: 30px;
        margin-top: 20px;
    }
    .tb-pagination{
        float: right;
        margin-top: 30px;
        margin-right: 30px;
    }
    .search-block{
        float: left;
        margin-left: 10px;
    }
    .search-title{
        font-size: 16px;
    }
    .search-div{
        padding-bottom: 60px;
    }
    .timeActive {
        background-color: #67C23A!important;
        color: white;
        font-weight: bold;
    }
</style>

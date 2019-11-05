<template>
    <el-row class="page-body">
        <el-col :span="14" style="margin-left: 50px">
            <!--3、使用组件-->
            <forms></forms>
        </el-col>
        <el-col :span="8" style="margin-left: 20px;">
            <order-desc></order-desc>
        </el-col>
    </el-row>
</template>

<script>
    import forms from './Forms'  // 1、导入组件
    import orderDesc from './OrderDesc'

    export default {
        components:{  // 在components中引入组件
            forms,
            orderDesc
        }
    }
</script>

<style scoped>
    .page-body .page-header{
        background: #f5f7fa;
        padding: 15px;
        margin: -15px -15px 15px -15px;
    }
</style>

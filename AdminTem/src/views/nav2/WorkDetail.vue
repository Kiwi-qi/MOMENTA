<template>
	
	<el-row class="page-body">
		<br>
	    <el-col  style="margin-left: 50px">
	        <topwork></topwork>
	    </el-col>
		<br>
		<el-col  style="margin-left: 50px;">
			<rightwork></rightwork>
		</el-col>
	</el-row>
</template>

<script>
	import topwork from "./LeftWork"
	import rightwork from "./RightWork"
	export default{
		components: {
			topwork,
			rightwork,
		
		},
	}
</script>

<style scoped>
    .page-body .page-header{
        background: #f5f7fa;
        padding: 15px;
        margin: -15px -15px 15px -15px;
    }
</style>
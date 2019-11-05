<template>
    <div class="order-desc">
      <p><h1>工单说明</h1></p>
      <div v-html="flowconf_desc"></div>
    </div>
</template>

<script>
	  import {Custom} from '../../api/api.js'
    export default {
      data() {
        return {
          flowconf_desc: '',
        };
      },
      methods:{
        InitFlowStepInfo () {
						Custom({'id':this.$route.params.id})
						.then(resp=>{
							console.log(resp)
							this.flowconf_desc = resp['description']
						})
						.catch(err => {
							this.$message({
							  type: 'info',
							  message: '获取字段异常'
								
							})
						});
        },
      },

      created () {
        this.InitFlowStepInfo();
      }

    }
</script>

<style scoped>

</style>

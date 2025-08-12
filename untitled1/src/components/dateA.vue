<template>
  <button id="getDataButton"  @click="getAllList()">查询</button>
  <el-form-item label="时间：">
    <el-date-picker
        v-model="value"
        type="daterange"
        range-separator="-"
        start-placeholder="开始时间"
        end-placeholder="结束时间"
        :default-time="defaultTime2"
        format="YYYY年MM月DD日"
        value-format="YYYY-MM-DD"
        @change="changeTime"
    />
  </el-form-item>

</template>

<script>
export default {
  name: "dateA",
  data(){
    return {
      value: []
    }
  },
  methods:{
    changeTime(date){
      if (date!=null){
        // this.value =[]
        // this.value.push(new Date(date.startTime))
        // this.value.push(new Date(date.endTime))
        console.log(" this.value")
        console.log( this.value)
      }
    },
    getAllList(){
      console.log(this.value)
      console.log(this.value[0])
      console.log(this.value[1])
    }
  }
}
</script>

<style scoped>

</style>
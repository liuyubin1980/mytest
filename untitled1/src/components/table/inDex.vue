<!-- 封装table组件 -->
<template>
  <div>
    <el-table :data="props.tableData" border style="width: 100%">
      <el-table-column :prop="item.prop" :label="item.lable" align="center" v-for="(item,index) in props.lable" :key="index" :width="item.width" :type="item.type"/>
    </el-table>
  </div>
</template>

<script setup >
//接收父组件传递的数据
const props = defineProps(['tableData','lable'])



</script>

<style lang="scss" scoped></style>
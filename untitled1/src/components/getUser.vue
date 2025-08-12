<template>
  <div id="getUser">

    <button id="getDataButton"  @click="getAllList()">查看采集数据情况</button>
    <button id="addUser"  @click="addUser()">添加用户</button>
    <el-table :data="users" >
      <el-table-column prop="id" label="id"></el-table-column>
      <el-table-column prop="name" label="姓名"></el-table-column>
      <el-table-column prop="sex" label="性别"></el-table-column>
    </el-table>


  </div>


</template>


<script>


import axios from "axios";

export default {

  name:`getUser`,
  data(){
    return {
      // signName: 'star',
      users: []
    }
  },
  methods:{
    getAllList: function () {
        this.$http.post('/qury2')
          .then((res) => {
            console.log(JSON.stringify(res))
            this.users = res["data"]
          })
          .catch(function (error) {
            console.log(error);
          });
    },
    addUser: function () {
      this.$http.post('/adduser')
      this.getAllList()
    }
  },
  mounted () {
    this.getAllList()
  }

}



</script>


<style scoped>

</style>
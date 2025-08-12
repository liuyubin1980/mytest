<template>
<!--  <get-uer/>-->
<!--  <DateA></DateA>-->
  <myInput></myInput>

</template>

<script>
// import MyTable from './components/table/MyTable.vue'
// import getUer from './components/getUser.vue'
// import DateA from "./components/dateA";
import myinput from "@/components/myinput";

export default {
  name:'App',
  components:{
    myInput:myinput,
    // DateA: DateA,
    // getUer
    // MyTable
  },
  data(){
    return{
      // tablelist:[]
    }
  },

  methods: {
    async getlist() {
      this.$http.post('/qury2')
          .then((res) => {
            // console.log(JSON.stringify(res))
            this.tablelist = res["data"]
          })
          .catch(function (error) {
            console.log(error);
          });
    }
  }
}
</script>

<style lang="less" scoped>
.mytags{
  display: flex;
}
.form-control{
  width: 80px;
}
</style>

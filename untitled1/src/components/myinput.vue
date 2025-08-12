<template>
  <el-form-item label="时间：">
    <el-autocomplete
        class="inline-input"
        v-model="state2"
        :fetch-suggestions="querySearch"
        placeholder="请输入内容"
        :trigger-on-focus="false"
        @select="handleSelect"
    ></el-autocomplete>
  </el-form-item>
</template>

<script>
import {ref} from "vue";

// const list_t = []

export default {
  name: "myInput",
  data(){
    return {
      value: [],
      // users: [],
      state1: '',
      state2: ''
    }
  },
  methods: {
    addNewProperty: async function (obj,newProperty,newValue) {

      //确保对象是响应式的

      if(!obj.isReactive){

        obj = ref(obj);

      }

      //添加新属性

      obj.value[newProperty] = newValue;

    },

    querySearch: async function (queryString, cb) {
      console.log(this.vm);


      await this.$http.post('/qury2')
          .then((res) => {
            // console.log(JSON.stringify(res))
            this.value = res["data"]

          })
          .catch(function (error) {
            console.log(error);
          });
      console.log(this.value)
      this.value.forEach((item) => {
        console.log(item);
        this.addNewProperty(item,"value",item.name)

          }
      )
      console.log(this.value)

      var results = this.value
      // var results = [{value: "111"}, {value: "222"}]
      // 调用 callback 返回建议列表的数据
      cb(results);
    },
    handleSelect(item) {
      console.log(item);
    }

  }

}
</script>

<style scoped>

</style>
<script setup>
import {ref} from "vue";
import axios from "axios";

// 要渲染的数据
const data = ref(null)

// 发送请求
function loadData() {
  axios.get("/data.json").then(function (resp) {
    data.value = resp.data
  }).catch(function (err) {
    console.log("出错了。。。", err)
  })
}
</script>
<template>
  <div>{{ data }}</div>
  <button @click="loadData">这是一个按钮</button>
</template>
<style lang="scss">
button {
  color: red;
  width: 100px;
  height: 30px;
  padding: 5px;
}
</style>
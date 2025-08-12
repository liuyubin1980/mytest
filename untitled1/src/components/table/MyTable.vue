<template>
  <div>MyTable 组件</div>
  <div>
    <table class="table table-striped">
      <thead>
      <tr>
        <slot name="header"></slot>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(item , index) in data" :key="item.id">
        <!-- 为数据行的 td 预留的“作用域插槽” -->
        <slot name="body" :row="item" :index="index"></slot>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>

export default {
  name: "MyTable",
  props: {
    // 表格的数据源
    data: {
      type: Array,
      default: () => [],
      require: true,
    },
  },
}
</script>


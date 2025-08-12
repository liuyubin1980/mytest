const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,

  devServer: {
    proxy: {
      '/': {
        target: 'http://localhost', //设置你调用的接口域名和端口号 别忘了加 http
        changeOrigin: true,
        ws: false,
        pathRewrite: {}
      }
    }
  }
})




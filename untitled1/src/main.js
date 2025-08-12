import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'
/* 引入 ElementPlus */
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App)
axios.defaults.baseURL='/'
app.config.globalProperties.$http=axios
app.use(ElementPlus)
app.mount('#app')


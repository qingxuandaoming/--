import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import '@fortawesome/fontawesome-free/css/all.min.css'
import './assets/styles/base.css'

// 在开发环境中导入数据库测试
if (import.meta.env.DEV) {
  import('./utils/dbTest.js');
}

const app = createApp(App)
app.use(router)
app.mount('#app')

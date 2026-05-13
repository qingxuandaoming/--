<script setup>
import { onMounted } from 'vue';
import Navbar from './components/Navbar.vue';
import Footer from './components/Footer.vue';
import '@fortawesome/fontawesome-free/css/all.min.css';
import './assets/styles/base.css';

onMounted(() => {
  // 在组件挂载后执行的逻辑
  document.title = '灵境骑行 - 探索城市周边最美骑行路线';
});
</script>

<template>
  <div class="app">
    <Navbar />
    <router-view />
    <Footer />
  </div>
</template>

<style>
/* 全局样式 */
* {
  box-sizing: border-box;
}

/* 确保页面占满整个视口高度 */
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 确保主要内容区域可以伸展填充空间 */
main {
  flex: 1;
}
</style>

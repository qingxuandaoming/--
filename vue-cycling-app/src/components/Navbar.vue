<template>
  <header class="navbar">
    <div class="container navbar-container">
      <div class="logo">
        <router-link to="/">灵境骑行</router-link>
      </div>
      <nav class="nav-links">
        <router-link to="/" exact-active-class="active">首页</router-link>
        <router-link to="/route-planning" active-class="active">路线规划</router-link>
        <router-link to="/login" active-class="active">登录</router-link>
        <router-link to="/register" active-class="active">注册</router-link>
        <router-link to="/feedback" active-class="active">建议</router-link>
        <router-link to="/help" active-class="active">帮助</router-link>
        <router-link to="/vr" active-class="active">VR灵境</router-link>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { useRoute } from 'vue-router';

const route = useRoute();
</script>

<style scoped>
/* 导航栏样式 */
.navbar {
  background-color: #fff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.navbar-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
}

.logo a {
  font-size: 1.5rem;
  font-weight: 700;
  color: #D84315; /* 深橙色 */
  text-decoration: none;
  transition: color 0.3s ease;
}

.logo a:hover {
  color: #FF7043; /* 亮橙色 */
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-links a {
  color: #5D4037; /* 深棕色 */
  text-decoration: none;
  font-weight: 500;
  padding: 8px 12px;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.nav-links a:hover {
  background-color: rgba(255, 193, 7, 0.2); /* 淡金色背景 */
  color: #D84315; /* 深橙色 */
}

.nav-links a.active {
  background: linear-gradient(135deg, #FF9800, #F57C00); /* 橙色渐变 */
  color: white !important;
  font-weight: 600;
  padding: 8px 15px;
  border-radius: 20px;
}

.nav-links a.active:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(255, 152, 0, 0.4); /* 橙色阴影 */
  background: linear-gradient(135deg, #FF9800, #F57C00); /* 保持橙色渐变 */
}
</style>
import { createRouter, createWebHistory } from 'vue-router'
import { isAuthenticated } from '../utils/auth.js'

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior(to, from, savedPosition) {
    // 如果有保存的位置（比如浏览器前进后退），则返回到保存的位置
    if (savedPosition) {
      return savedPosition
    }
    // 如果路由有hash，则滚动到对应的元素
    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth'
      }
    }
    // 默认滚动到页面顶部
    return { top: 0, behavior: 'smooth' }
  },
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('../views/Home.vue')
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('../views/Login.vue')
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('../views/Register.vue')
    },
    {
      path: '/feedback',
      name: 'Feedback',
      component: () => import('../views/Feedback.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/help',
      name: 'Help',
      component: () => import('../views/Help.vue')
    },
    {
      path: '/vr',
      name: 'VR',
      component: () => import('../views/VR.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/route-planning',
      name: 'RoutePlanning',
      component: () => import('../views/RoutePlanning.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/safety-guide',
      name: 'SafetyGuide',
      component: () => import('../views/SafetyGuide.vue')
    },
    {
      path: '/maintenance-guide',
      name: 'MaintenanceGuide',
      component: () => import('../views/MaintenanceGuide.vue')
    },
    {
      path: '/event-calendar',
      name: 'EventCalendar',
      component: () => import('../views/EventCalendar.vue')
    },
    {
      path: '/equipment',
      name: 'Equipment',
      component: () => import('../views/Equipment.vue')
    }
  ]
})

// 全局前置守卫 - 检查登录状态
router.beforeEach((to, from, next) => {
  // 检查目标路由是否需要认证
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // 检查用户是否已登录
    if (!isAuthenticated()) {
      // 未登录，跳转到登录页面
      next({
        path: '/login',
        query: { redirect: to.fullPath } // 保存原始目标路径，登录后可以跳转回去
      })
    } else {
      // 已登录，继续访问
      next()
    }
  } else {
    // 不需要认证的路由，直接访问
    next()
  }
})

export default router
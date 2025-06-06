import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
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
      component: () => import('../views/Feedback.vue')
    },
    {
      path: '/help',
      name: 'Help',
      component: () => import('../views/Help.vue')
    },
    {
      path: '/vr',
      name: 'VR',
      component: () => import('../views/VR.vue')
    },
    {
      path: '/route-planning',
      name: 'RoutePlanning',
      component: () => import('../views/RoutePlanning.vue')
    }
  ]
})

export default router
import HomeView from '@/views/HomeView.vue'
import { createRouter, createWebHistory, type RouteLocationNormalized } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
        {
          path: '/',
          name: 'home',
          component: HomeView
        }
  ]
})

export default router

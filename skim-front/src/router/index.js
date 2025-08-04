import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AuthView from '../views/AuthView.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: HomeView,
    },
    {
        path: '/auth',
        name: 'auth',
        component: AuthView,
    },
    {
        path: '/search',
        name: 'SearchView',
        component: () => import('@/views/SearchView.vue'),
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router

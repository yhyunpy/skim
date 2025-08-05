import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import MyPageView from '../views/MyPageView.vue'
import OAuthCallback from '../views/OAuthCallback.vue'
import SearchView from '../views/SearchView.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: HomeView,
    },
    {
        path: '/login',
        name: 'Login',
        component: LoginView,
    },
    {
        path: '/mypage',
        name: 'MyPage',
        component: MyPageView,
    },
    {
        path: '/oauth/callback',
        name: 'OAuthCallback',
        component: OAuthCallback,
    },
    {
        path: '/search',
        name: 'Search',
        component: SearchView,
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router

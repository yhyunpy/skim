<template>
  <nav class="bottom-nav">
    <button 
      v-for="item in navItems" 
      :key="item.name" 
      :class="{ active: isActive(item.path) }"
      @click="goTo(item.path)"
    >
      <span v-if="item.name === 'home'" class="material-icons">home</span>
      <span v-else-if="item.name === 'search'" class="material-icons">search</span>
      <span v-else-if="item.name === 'mypage'" class="material-icons">account_circle</span>
      <span v-else>{{ item.label }}</span>
    </button>
  </nav>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const navItems = [
  { name: 'home', label: '홈', path: '/' },
  { name: 'search', label: '검색', path: '/search' },
  { name: 'mypage', label: '마이페이지', path: '/mypage' },
]

const goTo = (path) => {
  router.push(path)
}

const isActive = (path) => {
  return route.path === path
}
</script>

<style scoped>
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 60px;
  background: #fff;
  display: flex;
  justify-content: space-around;
  padding: 0.5rem 0;
  box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
  z-index: 1000;
}

.bottom-nav button {
  background: none;
  border: none;
  font-size: 1rem;
  padding: 0.5rem 1rem;
  cursor: pointer;
}

</style>

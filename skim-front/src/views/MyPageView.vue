<template>
  <main class="mypage">
    <h2 v-if="!isLoggedIn">로그인 중...</h2>
    <div v-else>
      <h2>마이페이지</h2>
      <p>{{ user.name }}님 환영합니다!</p>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const isLoggedIn = ref(false)
const user = ref({})
const router = useRouter()

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (!token) {
    router.push('/login')  // 토큰 없으면 로그인 페이지로 리다이렉트
    return
  }

  try {
    const res = await fetch('/users/me', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
    if (res.ok) {
      const data = await res.json()
      user.value = data
      isLoggedIn.value = true
    } else {
      // 토큰이 유효하지 않으면 localStorage에서 제거하고 로그인 페이지로 이동
      localStorage.removeItem('token')
      router.push('/login')
    }
  } catch (e) {
    console.error(e)
    router.push('/login')
  }
})
</script>

<style scoped>
.mypage {
  text-align: center;
}
</style>


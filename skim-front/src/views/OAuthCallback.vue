<template>
  <div>로그인 처리 중...</div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

onMounted(async () => {
  const code = route.query.code

  if (code) {
    try {
      // GET 방식 + 쿼리 파라미터로 code 전송
      const res = await fetch(`http://localhost:8000/users/login?code=${code}`, {
        method: 'GET',
        credentials: 'include', // 쿠키 사용하는 경우
      })

      const data = await res.json()
      console.log('로그인 결과:', data)

      // access_token 저장
      localStorage.setItem('token', data.access_token)

      // 홈으로 이동 
      router.push('/')
    } catch (err) {
      console.error('로그인 실패:', err)
    }
  } else {
    console.error('Authorization code 없음')
  }
})
</script>


<template>
  <main class="search">
    <h2>검색 결과</h2>
    <input v-model="query" @keyup.enter="search" placeholder="검색" style="font-size: 1rem;"/>
    <div v-if="results.length">
      <div v-for="item in results" :key="item.id">
        {{ item.title }}
      </div>
    </div>
    <div v-else-if="query">
      검색 결과가 없습니다.
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const query = ref(route.query.q || '')
const results = ref([])

const search = () => {
  router.push({ path: '/search', query: { q: query.value } })
  // 예시: 검색 API 호출
  results.value = mockSearch(query.value)
}

// 페이지 진입 시 or URL 변화 시 검색 실행
onMounted(search)
watch(() => route.query.q, () => {
  query.value = route.query.q || ''
  search()
})

// 예시용 검색 함수
function mockSearch(keyword) {
  if (!keyword) return []
  return [
    { id: 1, title: `🔍 ${keyword} 결과 1` },
    { id: 2, title: `🔍 ${keyword} 결과 2` },
  ]
}
</script>

<style scoped>
.search {
  text-align: center;
}
</style>

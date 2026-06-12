<template>
  <div class="container mt-4">
    <div class="d-flex align-items-center justify-content-between mb-4">
      <div>
        <a class="me-3 text-decoration-none text-secondary" href="#" @click.prevent="goBack">← 뒤로가기</a>
        <span class="h3 mb-0">비디오 검색</span>
      </div>
      <button class="btn btn-outline-secondary" @click="doSearch">찾기</button>
    </div>

    <div class="input-group input-group-lg mb-4">
      <input
        v-model="q"
        @keyup.enter="doSearch"
        class="form-control"
        placeholder="검색어 입력"
        aria-label="검색어 입력"
      />
      <button class="btn btn-success" type="button" @click="doSearch">검색</button>
    </div>

    <div class="row g-3">
      <div class="col-lg-4 col-md-6" v-for="v in videos" :key="v.id.videoId">
        <VideoCard :video="v" />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { searchVideos } from '../api/youtube'
import VideoCard from '../components/VideoCard.vue'

export default {
  components: { VideoCard },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const q = ref(route.query.q || '')
    const videos = ref([])

    async function doSearch(query = q.value) {
      if (!query) return
      q.value = query
      videos.value = await searchVideos(query)
      router.replace({ query: { q: query } })
    }

    watch(
      () => route.query.q,
      (value) => {
        if (value && value !== q.value) {
          q.value = value
          doSearch(value)
        }
      }
    )

    onMounted(() => {
      if (q.value) {
        doSearch(q.value)
      }
    })

    function goBack() {
      router.back()
    }

    return { q, videos, doSearch, goBack }
  }
}
</script>

<style>
.container{padding:20px}
.card{cursor:pointer}
</style>

<template>
  <div class="container mt-4">
    <div class="d-flex align-items-center mb-4">
      <a class="me-3 text-decoration-none text-secondary" href="#" @click.prevent="goBack">← 뒤로가기</a>
      <h1 class="h4 mb-0">나중에 볼 동영상</h1>
    </div>

    <div v-if="savedVideos.length" class="row g-3">
      <div class="col-lg-4 col-md-6" v-for="video in savedVideos" :key="video.id">
        <div class="card h-100">
          <img :src="video.thumbnail" class="card-img-top" alt="video thumbnail" />
          <div class="card-body d-flex flex-column">
            <h5 class="card-title text-truncate" title="{{ video.title }}">{{ video.title }}</h5>
            <p class="card-text text-muted small mb-3">{{ video.channel }}</p>
            <div class="mt-auto d-flex justify-content-between align-items-center">
              <router-link :to="`/video/${video.id}`" class="btn btn-sm btn-outline-primary">보기</router-link>
              <button class="btn btn-sm btn-danger" @click="deleteItem(video.id)">삭제</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-5 text-secondary">
      등록된 비디오 없음
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getSavedVideos, removeSavedVideo } from '../utils/storage'

export default {
  setup() {
    const router = useRouter()
    const savedVideos = ref([])

    function loadSaved() {
      savedVideos.value = getSavedVideos()
    }

    function goBack() {
      router.back()
    }

    function deleteItem(id) {
      removeSavedVideo(id)
      loadSaved()
    }

    onMounted(loadSaved)

    return { savedVideos, goBack, deleteItem }
  }
}
</script>

<style>
.card-img-top{height:180px;object-fit:cover}
</style>

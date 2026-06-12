<template>
  <div class="container mt-4">
    <div class="d-flex align-items-center mb-4">
      <a class="me-3 text-decoration-none text-secondary" href="#" @click.prevent="goBack">← 뒤로가기</a>
      <h1 class="h4 mb-0">좋아하는 채널</h1>
    </div>

    <div v-if="channels.length" class="row g-3">
      <div class="col-lg-4 col-md-6" v-for="channel in channels" :key="channel.id">
        <div class="card h-100 p-3 d-flex flex-column justify-content-between">
          <h5 class="card-title mb-3">{{ channel.name }}</h5>
          <button class="btn btn-sm btn-danger align-self-end" @click="deleteChannel(channel.id)">삭제</button>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-5 text-secondary">
      등록된 채널 없음
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getSavedChannels, removeSavedChannel } from '../utils/storage'

export default {
  setup() {
    const router = useRouter()
    const channels = ref([])

    function loadChannels() {
      channels.value = getSavedChannels()
    }

    function goBack() {
      router.back()
    }

    function viewChannel(id) {
      router.push(`/channel/${id}`)
    }

    function deleteChannel(id) {
      removeSavedChannel(id)
      loadChannels()
    }

    onMounted(loadChannels)

    return { channels, goBack, viewChannel, deleteChannel }
  }
}
</script>

<style>
.card{min-height:140px}
</style>

<template>
  <div class="container mt-4">
    <div class="d-flex align-items-center mb-3">
      <a class="me-3 text-decoration-none text-secondary" href="#" @click.prevent="goBack">← 뒤로가기</a>
      <h1 class="h4 mb-0">{{ video ? video.snippet.title : '로딩 중...' }}</h1>
    </div>

    <div v-if="video" class="mb-4">
      <div class="ratio ratio-16x9 mb-3">
        <iframe :src="frameSrc" title="video player" allowfullscreen></iframe>
      </div>

      <div class="mb-3">
        <h2 class="h5 mb-1">{{ video.snippet.title }}</h2>
        <p class="text-muted mb-1">업로드 날짜: {{ publishedDate }}</p>
        <p class="mb-1"><strong>{{ video.snippet.channelTitle }}</strong></p>
      </div>

      <div class="card p-3 mb-3">
        <p class="mb-0" style="white-space: pre-line">{{ video.snippet.description }}</p>
      </div>

      <div class="d-flex gap-2">
        <button class="btn btn-primary" @click="toggleSave">
          {{ isSaved ? '저장 취소' : '동영상 저장' }}
        </button>
        <button class="btn btn-warning text-white" @click="toggleChannel">
          {{ channelSaved ? '채널 저장 취소' : '채널 저장' }}
        </button>
      </div>
    </div>

    <div v-else class="text-center py-5 text-muted">비디오 정보를 불러오는 중입니다...</div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getVideoById } from '../api/youtube'
import { saveVideo, removeSavedVideo, isVideoSaved, saveChannel, removeSavedChannel, isChannelSaved } from '../utils/storage'

export default {
  props: ['id'],
  setup(props) {
    const router = useRouter()
    const video = ref(null)
    const frameSrc = ref('')
    const saved = ref(false)
    const channelSaved = ref(false)

    const publishedDate = computed(() => {
      if (!video.value) return ''
      return new Date(video.value.snippet.publishedAt).toLocaleDateString('ko-KR')
    })

    function refreshSaved() {
      saved.value = isVideoSaved(props.id)
      if (video.value) {
        channelSaved.value = isChannelSaved(video.value.snippet.channelId)
      }
    }

    async function loadVideo() {
      const v = await getVideoById(props.id)
      video.value = v
      frameSrc.value = `https://www.youtube.com/embed/${props.id}`
      refreshSaved()
      localStorage.setItem('currentVideoContext', JSON.stringify({
        id: props.id,
        title: v.snippet.title,
        thumbnail: v.snippet.thumbnails.medium.url,
        channelId: v.snippet.channelId,
        channelTitle: v.snippet.channelTitle
      }))
    }

    function goBack() {
      router.back()
    }

    function toggleSave() {
      if (!video.value) return
      const item = {
        id: props.id,
        title: video.value.snippet.title,
        thumbnail: video.value.snippet.thumbnails.medium.url,
        channel: video.value.snippet.channelTitle
      }
      if (saved.value) {
        removeSavedVideo(props.id)
      } else {
        saveVideo(item)
      }
      refreshSaved()
    }

    function toggleChannel() {
      if (!video.value) return
      const item = {
        id: video.value.snippet.channelId,
        name: video.value.snippet.channelTitle
      }
      if (channelSaved.value) {
        removeSavedChannel(item.id)
      } else {
        saveChannel(item)
      }
      refreshSaved()
    }

    onMounted(loadVideo)

    return { video, frameSrc, goBack, publishedDate, isSaved: saved, channelSaved, toggleSave, toggleChannel }
  }
}
</script>

<style>
.ratio iframe{border-radius:8px}
</style>

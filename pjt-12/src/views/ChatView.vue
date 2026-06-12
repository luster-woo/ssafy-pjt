<template>
  <div class="container mt-4">
    <div class="d-flex align-items-center mb-4">
      <a class="me-3 text-decoration-none text-secondary" href="#" @click.prevent="goBack">← 뒤로가기</a>
      <h1 class="h4 mb-0">서비스 챗봇</h1>
    </div>

    <div class="card p-4 mb-4">
      <div class="chat-log mb-3">
        <div v-for="(msg, index) in messages" :key="index" :class="['mb-2', msg.type === 'user' ? 'text-end' : 'text-start']">
          <div :class="['d-inline-block p-2 rounded', msg.type === 'user' ? 'bg-primary text-white' : 'bg-light text-dark']">
            {{ msg.text }}
          </div>
        </div>
      </div>

      <div class="input-group">
        <input v-model="text" @keyup.enter="submitCommand" type="text" class="form-control" placeholder="명령어를 입력하세요. 예: SSAFY 검색해줘" />
        <button class="btn btn-success" type="button" @click="submitCommand">전송</button>
      </div>
    </div>

    <div class="alert alert-secondary">
      사용 가능한 예시 명령어:
      <ul class="mb-0">
        <li>SSAFY 검색해줘</li>
        <li>저장한 영상 보여줘</li>
        <li>이 채널 구독해줘</li>
        <li>저장한 채널 보여줘</li>
      </ul>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { parseCommand } from '../services/ai'
import { saveVideo, saveChannel, isVideoSaved, isChannelSaved } from '../utils/storage'

export default {
  setup() {
    const router = useRouter()
    const text = ref('')
    const messages = ref([
      { type: 'bot', text: '안녕하세요! 자연어로 명령을 입력하시면 서비스 기능을 실행합니다.' }
    ])

    function addMessage(type, msg) {
      messages.value.push({ type, text: msg })
      window.requestAnimationFrame(() => {
        const el = document.querySelector('.chat-log')
        if (el) el.scrollTop = el.scrollHeight
      })
    }

    function getCurrentVideoContext() {
      try {
        return JSON.parse(localStorage.getItem('currentVideoContext') || 'null')
      } catch {
        return null
      }
    }

    function submitCommand() {
      const value = text.value.trim()
      if (!value) return
      addMessage('user', value)
      const command = parseCommand(value)

      if (command.type === 'goto') {
        addMessage('bot', command.message)
        router.push(command.payload)
      } else if (command.type === 'search') {
        addMessage('bot', command.message)
        router.push({ path: '/search', query: { q: command.payload } })
      } else if (command.type === 'save-video') {
        const context = getCurrentVideoContext()
        if (!context) {
          addMessage('bot', '현재 상세 페이지에서만 동영상 저장 기능을 사용할 수 있습니다.')
        } else {
          if (isVideoSaved(context.id)) {
            addMessage('bot', '이 영상은 이미 저장되어 있습니다.')
          } else {
            saveVideo({ id: context.id, title: context.title, thumbnail: context.thumbnail, channel: context.channelTitle })
            addMessage('bot', '동영상이 저장되었습니다.')
          }
        }
      } else if (command.type === 'save-channel') {
        const context = getCurrentVideoContext()
        if (!context) {
          addMessage('bot', '현재 상세 페이지에서만 채널 저장 기능을 사용할 수 있습니다.')
        } else {
          if (isChannelSaved(context.channelId)) {
            addMessage('bot', '이 채널은 이미 저장되어 있습니다.')
          } else {
            saveChannel({ id: context.channelId, name: context.channelTitle })
            addMessage('bot', '채널이 저장되었습니다.')
          }
        }
      } else {
        addMessage('bot', command.message)
      }

      text.value = ''
    }

    function goBack() {
      router.back()
    }

    return { text, messages, submitCommand, goBack }
  }
}
</script>

<style>
.chat-log{max-height:320px;overflow:auto}
</style>

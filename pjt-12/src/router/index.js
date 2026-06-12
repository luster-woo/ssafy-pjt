import { createRouter, createWebHistory } from 'vue-router'
import SearchView from '../views/SearchView.vue'
import VideoDetail from '../views/VideoDetail.vue'
import SavedView from '../views/SavedView.vue'
import ChannelView from '../views/ChannelView.vue'
import ChatView from '../views/ChatView.vue'

const routes = [
  { path: '/', redirect: '/search' },
  { path: '/search', component: SearchView },
  { path: '/video/:id', component: VideoDetail, props: true },
  { path: '/saved', component: SavedView },
  { path: '/channels', component: ChannelView },
  { path: '/chat', component: ChatView }
]

export default createRouter({ history: createWebHistory(), routes })

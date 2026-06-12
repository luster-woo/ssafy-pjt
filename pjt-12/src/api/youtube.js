import axios from 'axios'

const BASE = 'https://www.googleapis.com/youtube/v3'
const KEY = import.meta.env.VITE_YOUTUBE_KEY

export async function searchVideos(q) {
  const res = await axios.get(`${BASE}/search`, {
    params: { part: 'snippet', q, key: KEY, type: 'video', maxResults: 12 }
  })
  return res.data.items
}

export async function getVideoById(id) {
  const res = await axios.get(`${BASE}/videos`, {
    params: { part: 'snippet,contentDetails', id, key: KEY }
  })
  return res.data.items?.[0]
}

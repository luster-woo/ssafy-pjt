const STORAGE_KEY = 'savedVideos'

export function getSavedVideos() {
  const raw = localStorage.getItem(STORAGE_KEY)
  if (!raw) return []
  try {
    return JSON.parse(raw)
  } catch (e) {
    return []
  }
}

export function saveVideo(video) {
  const saved = getSavedVideos()
  const exists = saved.find(item => item.id === video.id)
  if (!exists) {
    saved.push(video)
    localStorage.setItem(STORAGE_KEY, JSON.stringify(saved))
  }
}

export function removeSavedVideo(id) {
  const saved = getSavedVideos().filter(item => item.id !== id)
  localStorage.setItem(STORAGE_KEY, JSON.stringify(saved))
}

export function isVideoSaved(id) {
  return getSavedVideos().some(item => item.id === id)
}

const CHANNEL_KEY = 'savedChannels'

export function getSavedChannels() {
  const raw = localStorage.getItem(CHANNEL_KEY)
  if (!raw) return []
  try {
    return JSON.parse(raw)
  } catch (e) {
    return []
  }
}

export function saveChannel(channel) {
  const saved = getSavedChannels()
  const exists = saved.find(item => item.id === channel.id)
  if (!exists) {
    saved.push(channel)
    localStorage.setItem(CHANNEL_KEY, JSON.stringify(saved))
  }
}

export function removeSavedChannel(id) {
  const saved = getSavedChannels().filter(item => item.id !== id)
  localStorage.setItem(CHANNEL_KEY, JSON.stringify(saved))
}

export function isChannelSaved(id) {
  return getSavedChannels().some(item => item.id === id)
}

export function parseCommand(text) {
  const lower = text.trim().toLowerCase()
  const command = { type: 'unknown', payload: null, message: '' }

  if (!lower) {
    command.message = '명령을 입력해주세요.'
    return command
  }

  if (lower.includes('저장한 영상') || lower.includes('나중에 볼 영상')) {
    command.type = 'goto'
    command.payload = '/saved'
    command.message = '저장한 영상 목록으로 이동합니다.'
    return command
  }

  if (lower.includes('채널') && (lower.includes('보여줘') || lower.includes('찾아'))) {
    command.type = 'goto'
    command.payload = '/channels'
    command.message = '저장한 채널 목록으로 이동합니다.'
    return command
  }

  if (lower.includes('검색') || lower.includes('찾아')) {
    const keyword = extractKeyword(lower)
    if (keyword) {
      command.type = 'search'
      command.payload = keyword
      command.message = `"${keyword}"로 검색을 수행합니다.`
      return command
    }
    command.message = '검색어를 찾을 수 없습니다. 예를 들어 "SSAFY 검색해줘"를 입력해보세요.'
    return command
  }

  if (lower.includes('채널 저장') || lower.includes('구독해줘')) {
    command.type = 'save-channel'
    command.message = '현재 보고 있는 영상의 채널을 저장합니다.'
    return command
  }

  if (lower.includes('동영상 저장') || lower.includes('저장해줘')) {
    command.type = 'save-video'
    command.message = '현재 보고 있는 영상을 저장합니다.'
    return command
  }

  command.message = '죄송합니다. 명령을 이해하지 못했습니다. 예: "SSAFY 검색해줘", "저장한 영상 보여줘", "채널 저장"'
  return command
}

function extractKeyword(text) {
  const patterns = [
    /(.+) 검색해줘/,
    /(.+) 찾아줘/,
    /검색 (.+)/,
    /찾아 (.+)/,
    /(.+) 검색해 주세요/,
    /(.+) 찾아 주세요/
  ]
  for (const pattern of patterns) {
    const match = text.match(pattern)
    if (match && match[1]) {
      return match[1].trim()
    }
  }
  const words = text.split(' ')
  if (words.length > 1) {
    return words.filter(w => !['검색', '해줘', '찾아줘', '찾아', '검색해줘', '검색해', 'please', 'please.'].includes(w)).join(' ').trim()
  }
  return ''
}

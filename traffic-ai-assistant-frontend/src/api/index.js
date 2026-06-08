import axios from 'axios'

const API_BASE = 'http://127.0.0.1:8765'

const api = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
})

/**
 * 发送聊天消息（非流式）
 * @param {string} query - 用户问题
 * @param {string} sessionId - 会话ID（可选）
 * @returns {Promise<{answer: string, sources: string[], session_id: string}>}
 */
export function sendChat(query, sessionId = null) {
  return api.post('/chat', { query, session_id: sessionId })
    .then(res => res.data)
}

/**
 * 发送聊天消息（流式 SSE）
 * @param {string} query - 用户问题
 * @param {string} sessionId - 会话ID（可选）
 * @param {object} callbacks - 回调函数
 * @param {function(string): void} callbacks.onToken - 收到 token
 * @param {function(string[]): void} callbacks.onSources - 收到来源
 * @param {function(string): void} callbacks.onDone - 流结束
 * @param {function(Error): void} callbacks.onError - 出错
 */
export async function sendChatStream(query, sessionId = null, callbacks = {}) {
  const { onToken, onSources, onDone, onError } = callbacks

  const response = await fetch(`${API_BASE}/chat/stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, session_id: sessionId }),
  })

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`)
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''

  const processLine = (line) => {
    if (!line.startsWith('data: ')) return
    const event = JSON.parse(line.slice(6))

    switch (event.type) {
      case 'token':
        onToken?.(event.content)
        break
      case 'sources':
        onSources?.(event.sources || [])
        break
      case 'done':
        onDone?.(event.session_id)
        break
      case 'error':
        onError?.(new Error(event.content))
        break
      default:
        break
    }
  }

  let reading = true
  while (reading) {
    const { done, value } = await reader.read()
    if (done) {
      reading = false
    } else {
      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split('\n')
      buffer = lines.pop() || ''

      for (const line of lines) {
        if (line.trim()) processLine(line.trim())
      }
    }
  }

  if (buffer.trim()) {
    processLine(buffer.trim())
  }
}

export default api

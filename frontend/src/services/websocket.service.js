const MAX_RECONNECT_ATTEMPTS = 5
const WS_ENABLED = import.meta.env.VITE_WS_ENABLED !== 'false'

class WebSocketService {
  constructor() {
    this.sockets = {}
    this.listeners = new Map()
    this.retryCounters = {}
  }

  connect(token, role) {
    if (!token || !WS_ENABLED) return

    const baseEnv =
      import.meta.env.VITE_WS_BASE_URL ||
      window.location.origin.replace(/^http/, 'ws')
    const normalizedBase = this.#normalizeBase(baseEnv)

    // Always connect to notifications
    this.#createSocket(
      'notifications',
      `${normalizedBase}/notifications/?token=${token}`
    )

    // Only bosses receive dashboard push updates
    if (role === 'BOSS') {
      this.#createSocket(
        'dashboard',
        `${normalizedBase}/dashboard/?token=${token}`
      )
    }
  }

  disconnect() {
    Object.values(this.sockets).forEach((socket) => {
      socket.onclose = null
      socket.close()
    })
    this.sockets = {}
    this.retryCounters = {}
    this.listeners.clear()
  }

  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, [])
    }
    this.listeners.get(event).push(callback)
  }

  off(event, callback) {
    if (!this.listeners.has(event)) return

    const callbacks = this.listeners.get(event)
    const index = callbacks.indexOf(callback)
    if (index > -1) {
      callbacks.splice(index, 1)
    }
  }

  emit(event, data) {
    if (!this.listeners.has(event)) return

    this.listeners.get(event).forEach((callback) => {
      callback(data)
    })
  }

  #normalizeBase(value) {
    if (!value) return ''
    let base = value.trim()
    if (base.endsWith('/')) {
      base = base.slice(0, -1)
    }
    if (base.startsWith('http')) {
      base = base.replace(/^http/, 'ws')
    }
    return base
  }

  #createSocket(key, url) {
    if (this.sockets[key]) {
      return
    }

    try {
      const socket = new WebSocket(url)
      this.sockets[key] = socket

      socket.onopen = () => {
        this.retryCounters[key] = 0
        console.log(`[WS:${key}] connected`)
      }

      socket.onmessage = (event) => {
        try {
          const payload = JSON.parse(event.data || '{}')
          if (payload.type) {
            this.emit(payload.type, payload)
          }
        } catch (error) {
          console.warn(`[WS:${key}] failed to parse message`, error)
        }
      }

      socket.onerror = (error) => {
        console.warn(`[WS:${key}] error`, error)
      }

      socket.onclose = () => {
        delete this.sockets[key]
        this.#retryConnection(key, url)
      }
    } catch (error) {
      console.error(`[WS:${key}] unable to create connection`, error)
    }
  }

  #retryConnection(key, url) {
    const retries = (this.retryCounters[key] || 0) + 1
    if (retries > MAX_RECONNECT_ATTEMPTS) {
      console.warn(`[WS:${key}] max reconnect attempts reached`)
      return
    }

    this.retryCounters[key] = retries
    const timeout = Math.min(1000 * retries, 5000)

    setTimeout(() => {
      if (!this.sockets[key]) {
        this.#createSocket(key, url)
      }
    }, timeout)
  }
}

export default new WebSocketService()

<template>
  <div class="chat-window">
    <!-- Header -->
    <header class="chat-window__header section-dark">
      <div class="chat-window__header-content">
        <h1 class="chat-window__title bmw-heading">交通法规 AI 助手</h1>
        <p class="chat-window__subtitle">基于 RAG + Agent 的智能法律咨询</p>
      </div>
    </header>

    <!-- Messages -->
    <div class="chat-window__messages" ref="messages">
      <div class="chat-window__welcome" v-if="messages.length === 0">
        <h2 class="bmw-display">交通法规查询</h2>
        <p>输入任何交通法规相关问题，AI 将为您提供专业解答</p>
        <div class="chat-window__examples">
          <button
            v-for="example in examples"
            :key="example"
            class="btn-bmw-outline chat-window__example-btn"
            @click="handleExample(example)"
          >
            {{ example }}
          </button>
        </div>
      </div>
      <ChatMessage
        v-for="(msg, index) in messages"
        :key="index"
        :message="msg.content"
        :is-user="msg.isUser"
        :sources="msg.sources"
      />
      <div v-if="isWaitingForFirstToken" class="chat-window__typing">
        <div class="chat-window__typing-dot"></div>
        <div class="chat-window__typing-dot"></div>
        <div class="chat-window__typing-dot"></div>
      </div>
    </div>

    <!-- Input -->
    <ChatInput :loading="loading" @send="handleSend" />
  </div>
</template>

<script>
import ChatMessage from './ChatMessage.vue'
import ChatInput from './ChatInput.vue'
import { sendChatStream } from '@/api'

export default {
  name: 'ChatWindow',
  components: {
    ChatMessage,
    ChatInput,
  },
  data() {
    return {
      messages: [],
      loading: false,
      sessionId: null,
      examples: [
        '闯红灯扣几分？',
        '酒驾怎么处罚？',
        '发生交通事故怎么处理？',
        '超速50%以上怎么处罚？',
      ],
    }
  },
  computed: {
    isWaitingForFirstToken() {
      if (!this.loading) return false
      const lastMsg = this.messages[this.messages.length - 1]
      return lastMsg && !lastMsg.isUser && !lastMsg.content
    },
  },
  methods: {
    handleExample(example) {
      this.handleSend(example)
    },
    async handleSend(query) {
      this.messages.push({
        content: query,
        isUser: true,
        sources: [],
      })

      const aiIndex = this.messages.length
      this.messages.push({
        content: '',
        isUser: false,
        sources: [],
      })

      this.scrollToBottom()
      this.loading = true

      try {
        await sendChatStream(query, this.sessionId, {
          onToken: (token) => {
            this.messages[aiIndex].content += token
            this.$nextTick(() => this.scrollToBottom())
          },
          onSources: (sources) => {
            this.messages[aiIndex].sources = sources
          },
          onDone: (sessionId) => {
            this.sessionId = sessionId
          },
          onError: (err) => {
            if (!this.messages[aiIndex].content) {
              this.messages[aiIndex].content = '抱歉，服务出现错误，请稍后重试。'
            }
            console.error('Chat stream error:', err)
          },
        })
      } catch (err) {
        this.messages[aiIndex].content = '抱歉，服务出现错误，请稍后重试。'
        console.error('Chat error:', err)
      } finally {
        this.loading = false
        this.$nextTick(() => this.scrollToBottom())
      }
    },
    scrollToBottom() {
      const el = this.$refs.messages
      if (el) {
        el.scrollTop = el.scrollHeight
      }
    },
  },
}
</script>

<style scoped>
.chat-window {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: var(--bmw-dark-surface);
}

/* Header */
.chat-window__header {
  padding: 32px;
  text-align: center;
}

.chat-window__title {
  color: var(--bmw-white);
  margin-bottom: 8px;
}

.chat-window__subtitle {
  color: var(--bmw-gray);
  font-size: 0.875rem;
}

/* Messages */
.chat-window__messages {
  flex: 1;
  overflow-y: auto;
  padding: 32px;
}

/* Welcome */
.chat-window__welcome {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  text-align: center;
  color: var(--bmw-white);
}

.chat-window__welcome h2 {
  margin-bottom: 16px;
}

.chat-window__welcome p {
  color: var(--bmw-gray);
  margin-bottom: 32px;
}

.chat-window__examples {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: center;
  max-width: 600px;
}

.chat-window__example-btn {
  font-size: 0.875rem;
  padding: 8px 16px;
}

/* Typing Indicator */
.chat-window__typing {
  display: flex;
  gap: 4px;
  padding: 16px 20px;
  background: var(--bmw-dark);
  width: fit-content;
}

.chat-window__typing-dot {
  width: 8px;
  height: 8px;
  background: var(--bmw-gray);
  animation: typing 1.4s infinite;
}

.chat-window__typing-dot:nth-child(2) {
  animation-delay: 0.2s;
}

.chat-window__typing-dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-8px);
  }
}
</style>

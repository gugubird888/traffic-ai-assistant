<template>
  <div class="chat-message" :class="{ 'chat-message--user': isUser, 'chat-message--ai': !isUser }">
    <div class="chat-message__avatar">
      <span v-if="isUser">U</span>
      <span v-else>AI</span>
    </div>
    <div class="chat-message__content">
      <div class="chat-message__bubble">
        <div v-if="isUser" class="chat-message__text">{{ message }}</div>
        <div v-else class="chat-message__text chat-message__markdown" v-html="renderedMessage"></div>
      </div>
      <div v-if="sources && sources.length" class="chat-message__sources">
        <p class="chat-message__sources-label">引用来源：</p>
        <ul>
          <li v-for="(source, index) in sources" :key="index">{{ source }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import { marked } from 'marked'

export default {
  name: 'ChatMessage',
  props: {
    message: {
      type: String,
      required: true,
    },
    isUser: {
      type: Boolean,
      default: false,
    },
    sources: {
      type: Array,
      default: () => [],
    },
  },
  computed: {
    renderedMessage() {
      return marked(this.message)
    },
  },
}
</script>

<style scoped>
.chat-message {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}

.chat-message--user {
  flex-direction: row-reverse;
}

.chat-message__avatar {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 900;
  font-size: 0.875rem;
  flex-shrink: 0;
}

.chat-message--user .chat-message__avatar {
  background: var(--bmw-blue);
  color: var(--bmw-white);
}

.chat-message--ai .chat-message__avatar {
  background: var(--bmw-dark);
  color: var(--bmw-white);
}

.chat-message__content {
  max-width: 70%;
}

.chat-message__bubble {
  padding: 16px 20px;
  line-height: 1.5;
}

.chat-message--user .chat-message__bubble {
  background: var(--bmw-blue);
  color: var(--bmw-white);
}

.chat-message--ai .chat-message__bubble {
  background: var(--bmw-dark);
  color: var(--bmw-white);
}

.chat-message__text {
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
}

/* Markdown 样式 */
.chat-message__markdown :deep(h1),
.chat-message__markdown :deep(h2),
.chat-message__markdown :deep(h3) {
  margin: 16px 0 8px;
  font-weight: 700;
}

.chat-message__markdown :deep(p) {
  margin: 8px 0;
}

.chat-message__markdown :deep(ul),
.chat-message__markdown :deep(ol) {
  margin: 8px 0;
  padding-left: 24px;
}

.chat-message__markdown :deep(li) {
  margin: 4px 0;
}

.chat-message__markdown :deep(strong) {
  font-weight: 700;
  color: var(--bmw-blue);
}

.chat-message__markdown :deep(code) {
  background: rgba(255, 255, 255, 0.1);
  padding: 2px 6px;
  font-family: 'Courier New', monospace;
}

.chat-message__markdown :deep(blockquote) {
  border-left: 3px solid var(--bmw-blue);
  padding-left: 12px;
  margin: 8px 0;
  color: var(--bmw-silver);
}

.chat-message__sources {
  margin-top: 12px;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.05);
  font-size: 0.875rem;
  color: var(--bmw-gray);
}

.chat-message__sources-label {
  font-weight: 700;
  margin-bottom: 8px;
  color: var(--bmw-silver);
}

.chat-message__sources ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.chat-message__sources li {
  padding: 4px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.chat-message__sources li:last-child {
  border-bottom: none;
}
</style>

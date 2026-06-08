<template>
  <div class="chat-input">
    <input
      v-model="query"
      class="chat-input__field input-bmw"
      placeholder="输入您的交通法规问题..."
      @keyup.enter="handleSend"
      :disabled="loading"
    />
    <button
      class="chat-input__btn btn-bmw"
      @click="handleSend"
      :disabled="loading || !query.trim()"
    >
      <span v-if="loading">发送中...</span>
      <span v-else>发送</span>
    </button>
  </div>
</template>

<script>
export default {
  name: 'ChatInput',
  props: {
    loading: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      query: '',
    }
  },
  methods: {
    handleSend() {
      if (!this.query.trim() || this.loading) return
      this.$emit('send', this.query.trim())
      this.query = ''
    },
  },
}
</script>

<style scoped>
.chat-input {
  display: flex;
  gap: 12px;
  padding: 24px 32px;
  background: var(--bmw-dark-surface);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.chat-input__field {
  flex: 1;
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.2);
  color: var(--bmw-white);
}

.chat-input__field:focus {
  border-color: var(--bmw-blue);
  background: rgba(255, 255, 255, 0.08);
}

.chat-input__field::placeholder {
  color: var(--bmw-gray);
}

.chat-input__field:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.chat-input__btn {
  min-width: 100px;
}

.chat-input__btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>

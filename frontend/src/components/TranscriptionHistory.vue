<!-- src/components/TranscriptionHistory.vue -->
<template>
  <div class="history-container">
    <h2>Previous Transcriptions</h2>
    <div v-if="history.length === 0" class="no-history">
      <p>No previous transcriptions found.</p>
    </div>
    <div v-else class="history-list">
      <div
        v-for="(item, index) in history"
        :key="index"
        class="history-item"
        @click="selectTranscription(item)"
      >
        <div class="history-item-header">
          <div class="file-info">
            <strong>{{ item.fileName }}</strong>
            <span>({{ item.date }})</span>
          </div>
          <div class="transcription-details">
            <span class="language">{{ item.language.toUpperCase() }}</span>
            <span :class="['mode', item.mode]">{{ item.mode === 'local' ? 'Local' : 'API' }}</span>
          </div>
        </div>
        <p class="transcription-preview">{{ truncatedText(item.transcription) }}</p>
      </div>
    </div>
    <div v-if="history.length > 0" class="clear-history">
      <button @click="clearHistory" class="clear-button">Clear History</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TranscriptionHistory',
  props: {
    history: {
      type: Array,
      default: () => []
    }
  },
  methods: {
    selectTranscription(item) {
      this.$emit('select-transcription', item);
    },
    clearHistory() {
      if (confirm('Are you sure you want to clear all transcription history?')) {
        this.$emit('clear-history');
      }
    },
    truncatedText(text) {
      if (text.length <= 100) return text;
      return text.substring(0, 100) + '...';
    }
  }
};
</script>

<style scoped>
.history-container {
  margin-top: 30px;
  border-top: 1px solid #ddd;
  padding-top: 20px;
}

.history-list {
  margin-top: 10px;
  max-height: 300px;
  overflow-y: auto;
}

.history-item {
  background-color: #f9f9f9;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.history-item:hover {
  background-color: #f0f0f0;
}

.history-item-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}

.transcription-details {
  display: flex;
  gap: 10px;
}

.language {
  font-size: 0.8em;
  background-color: #e9ecef;
  padding: 2px 5px;
  border-radius: 3px;
}

.mode {
  font-size: 0.8em;
  padding: 2px 5px;
  border-radius: 3px;
  font-weight: bold;
}

.mode.local {
  background-color: #e6f3ff;
  color: #0066cc;
}

.mode.api {
  background-color: #e6fff2;
  color: #00994d;
}

.transcription-preview {
  color: #666;
  font-size: 0.9em;
  margin: 5px 0 0 0;
}

.no-history {
  color: #999;
  text-align: center;
  padding: 20px;
}

.clear-button {
  background-color: #f8d7da;
  color: #842029;
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8em;
  margin-top: 10px;
}

.clear-button:hover {
  background-color: #f5c2c7;
}

.clear-history {
  text-align: right;
  margin-top: 10px;
}
</style>
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
            <span class="date-info">({{ formatDate(item.date) }})</span>
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
      if (text.length <= 80) return text;
      return text.substring(0, 80) + '...';
    },
    formatDate(dateString) {
      // Format to show only the date part or shortened version
      const date = new Date(dateString);
      return date.toLocaleDateString();
    }
  }
};
</script>

<style scoped>
.history-container {
  width: 100%;
}

h2 {
  font-size: 1.2rem;
  margin-top: 0;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.history-list {
  margin-top: 10px;
  max-height: calc(100vh - 200px);
  overflow-y: auto;
}

.history-item {
  background-color: #f9f9f9;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.1s;
  border-left: 3px solid transparent;
}

.history-item:hover {
  background-color: #f0f0f0;
  transform: translateX(2px);
  border-left-color: #007BFF;
}

.history-item-header {
  margin-bottom: 5px;
}

.file-info {
  display: flex;
  flex-direction: column;
  margin-bottom: 5px;
}

.date-info {
  font-size: 0.7em;
  color: #666;
}

.transcription-details {
  display: flex;
  gap: 5px;
  margin-top: 3px;
}

.language {
  font-size: 0.7em;
  background-color: #e9ecef;
  padding: 2px 5px;
  border-radius: 3px;
}

.mode {
  font-size: 0.7em;
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
  font-size: 0.8em;
  margin: 5px 0 0 0;
  line-height: 1.4;
}

.no-history {
  color: #999;
  text-align: center;
  padding: 20px 0;
  font-style: italic;
  font-size: 0.9em;
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
  width: 100%;
}

.clear-button:hover {
  background-color: #f5c2c7;
}

.clear-history {
  text-align: center;
  margin-top: 10px;
}
</style>
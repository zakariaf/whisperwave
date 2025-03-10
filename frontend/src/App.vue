<!-- src/App.vue -->
<template>
  <div class="app-container">
    <!-- Left sidebar for history -->
    <div class="sidebar">
      <TranscriptionHistory
        :history="transcriptionHistory"
        @select-transcription="loadHistoryItem"
        @clear-history="clearHistory"
      />
    </div>

    <!-- Main content area -->
    <div class="main-content">
      <header class="header">
        <h1>Audio Transcription</h1>
      </header>

      <!-- File Uploader Component -->
      <FileUploader @file-selected="handleFileSelected" />

      <!-- Language Select Component -->
      <LanguageSelect v-model="language" />

      <!-- Translation Select Component -->
      <TranslationSelect v-model="targetLanguage" :source-language="language" />

      <!-- Transcription Mode Component -->
      <TranscriptionMode v-model="transcriptionMode" />

      <!-- Transcribe Button -->
      <button @click="upload" :disabled="isLoading">
        <span v-if="!isLoading">Transcribe</span>
        <span v-else>Transcribing...</span>
      </button>

      <!-- Loading Indicator -->
      <div v-if="isLoading" class="loading">
        <div class="spinner"></div>
        <p>Processing your audio file...</p>
      </div>

      <!-- Error Message -->
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <!-- Display Transcription -->
      <div v-if="transcription" class="result">
        <h2>Transcription Result:</h2>
        <p>{{ transcription }}</p>

        <!-- Display Translation if available -->
        <div v-if="translation" class="translation">
          <h3>Translation:</h3>
          <p>{{ translation }}</p>
        </div>

        <!-- Analytics Display -->
        <AnalyticsDisplay :analytics="analytics" />
      </div>
    </div>
  </div>
</template>

<script>
import FileUploader from './components/FileUploader.vue';
import LanguageSelect from './components/LanguageSelect.vue';
import TranscriptionMode from './components/TranscriptionMode.vue';
import TranslationSelect from './components/TranslationSelect.vue';
import TranscriptionHistory from './components/TranscriptionHistory.vue';
import AnalyticsDisplay from './components/AnalyticsDisplay.vue';

export default {
  name: 'App',
  components: {
    FileUploader,
    LanguageSelect,
    TranscriptionMode,
    TranslationSelect,
    TranscriptionHistory,
    AnalyticsDisplay,
  },
  data() {
    return {
      file: null,
      language: 'en',
      targetLanguage: '',
      transcriptionMode: 'local',
      transcription: '',
      translation: '',
      isLoading: false,
      errorMessage: '',
      transcriptionHistory: [],
      selectedFileName: '',
      analytics: null
    };
  },
  mounted() {
    // Load transcription history from localStorage when the app starts
    this.loadHistory();
  },
  methods: {
    handleFileSelected(file) {
      this.file = file;
      this.selectedFileName = file ? file.name : '';

      // Auto-select mode based on file size
      if (file && file.size > 25 * 1024 * 1024 && this.transcriptionMode === 'api') {
        this.transcriptionMode = 'local';
        this.errorMessage = 'File size exceeds OpenAI API limit (25MB). Mode switched to local processing automatically.';
        setTimeout(() => {
          this.errorMessage = '';
        }, 5000); // Clear message after 5 seconds
      }
    },

    // History management methods
    saveToHistory(item) {
      // Add new item to beginning of history array
      this.transcriptionHistory.unshift(item);

      // Limit history to last 10 items
      if (this.transcriptionHistory.length > 10) {
        this.transcriptionHistory = this.transcriptionHistory.slice(0, 10);
      }

      // Save to localStorage
      localStorage.setItem('transcriptionHistory', JSON.stringify(this.transcriptionHistory));
    },

    loadHistory() {
      const savedHistory = localStorage.getItem('transcriptionHistory');
      if (savedHistory) {
        try {
          this.transcriptionHistory = JSON.parse(savedHistory);
        } catch (e) {
          console.error('Error loading history:', e);
          this.transcriptionHistory = [];
        }
      }
    },

    loadHistoryItem(item) {
      this.transcription = item.transcription;
      this.translation = item.translation || '';
      this.language = item.language;
      this.targetLanguage = item.targetLanguage || '';
      this.transcriptionMode = item.mode;
      this.selectedFileName = item.fileName;
      this.analytics = item.analytics;
    },

    clearHistory() {
      this.transcriptionHistory = [];
      localStorage.removeItem('transcriptionHistory');
    },
    async upload() {
      if (!this.file) {
        alert('Please select an audio file (WAV, MP3, FLAC, M4A, or OGG).');
        return;
      }

      // Check file size if OpenAI API is selected
      if (this.transcriptionMode === 'api' && this.file.size > 25 * 1024 * 1024) {
        alert('File size exceeds the OpenAI API limit of 25MB. Please select a smaller file or use the local option.');
        return;
      }

      // Reset previous results and error messages
      this.transcription = '';
      this.translation = '';
      this.errorMessage = '';
      this.analytics = null;
      this.isLoading = true;

      const formData = new FormData();
      formData.append('file', this.file);
      formData.append('language', this.language);
      formData.append('mode', this.transcriptionMode);
      if (this.targetLanguage) {
        formData.append('target_language', this.targetLanguage);
      }

      try {
        const response = await fetch('http://localhost:5001/transcribe', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          const errorData = await response.json();
          this.errorMessage = `Transcription failed: ${errorData.error || 'Unknown error'}`;
          return;
        }

        const data = await response.json();
        this.transcription = data.transcription;
        this.translation = data.translation || '';
        this.analytics = data.analytics;

        // Save to history
        if (this.transcription && this.file) {
          this.saveToHistory({
            fileName: this.file.name,
            date: new Date().toLocaleString(),
            language: this.language,
            targetLanguage: this.targetLanguage,
            mode: this.transcriptionMode,
            transcription: this.transcription,
            translation: this.translation,
            analytics: this.analytics
          });
        }
      } catch (error) {
        console.error('Error during transcription:', error);
        this.errorMessage = 'Failed to connect to the transcription service. Please try again.';
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>

<style scoped>
.app-container {
  display: flex;
  margin: 40px auto;
  max-width: 1200px;
  background: transparent;
}

.sidebar {
  width: 300px;
  margin-right: 20px;
  flex-shrink: 0;
  background: #fff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  padding: 20px;
  overflow-y: auto;
  max-height: calc(100vh - 80px);
  position: sticky;
  top: 40px;
}

.main-content {
  flex-grow: 1;
  background: #fff;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 4px;
}

@media (max-width: 768px) {
  .app-container {
    flex-direction: column-reverse;
  }

  .sidebar {
    width: auto;
    margin-right: 0;
    margin-top: 20px;
    max-height: none;
    position: static;
  }
}
</style>
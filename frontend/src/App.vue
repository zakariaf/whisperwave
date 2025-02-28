<!-- src/App.vue -->
<template>
  <div class="container">
    <header class="header">
      <h1>Audio Transcription</h1>
    </header>

    <!-- File Uploader Component -->
    <FileUploader @file-selected="handleFileSelected" />

    <!-- Language Select Component -->
    <LanguageSelect v-model="language" />

    <!-- Transcription Mode Component -->
    <TranscriptionMode v-model="transcriptionMode" />

    <!-- Transcribe Button -->
    <button @click="upload">Transcribe</button>

    <!-- Display Transcription -->
    <div v-if="transcription" class="result">
      <h2>Transcription Result:</h2>
      <p>{{ transcription }}</p>
    </div>
  </div>
</template>

<script>
import FileUploader from './components/FileUploader.vue';
import LanguageSelect from './components/LanguageSelect.vue';
import TranscriptionMode from './components/TranscriptionMode.vue';

export default {
  name: 'App',
  components: {
    FileUploader,
    LanguageSelect,
    TranscriptionMode,
  },
  data() {
    return {
      file: null,
      language: 'en',
      transcriptionMode: 'local',
      transcription: '',
    };
  },
  methods: {
    handleFileSelected(file) {
      this.file = file;
    },
    async upload() {
      if (!this.file) {
        alert('Please select a WAV file.');
        return;
      }

      const formData = new FormData();
      formData.append('file', this.file);
      formData.append('language', this.language);
      formData.append('mode', this.transcriptionMode);

      try {
        const response = await fetch('http://localhost:5001/transcribe', {
          method: 'POST',
          body: formData,
        });
        const data = await response.json();
        this.transcription = data.transcription;
      } catch (error) {
        console.error('Error during transcription:', error);
      }
    },
  },
};
</script>
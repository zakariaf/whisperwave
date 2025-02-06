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

export default {
  name: 'App',
  components: {
    FileUploader,
    LanguageSelect,
  },
  data() {
    return {
      file: null,
      language: 'en',
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

      // Build the backend URL using environment variables
      const backendUrl = `${import.meta.env.VITE_BACKEND_URL}:${import.meta.env.VITE_BACKEND_PORT}`;

      try {
        const response = await fetch(`${backendUrl}/transcribe`, {
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

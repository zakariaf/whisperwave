<!-- src/components/FileUploader.vue -->
<template>
  <div class="uploader">
    <label for="fileInput">Upload WAV/MP3 File</label>
    <input
      id="fileInput"
      type="file"
      accept=".wav,.mp3"
      @change="onFileChange"
    />
    <div v-if="selectedFile" class="file-info">
      <span>Selected: {{ selectedFile.name }}</span>
      <span :class="{ 'size-warning': isFileTooLarge }">
        Size: {{ formatFileSize(selectedFile.size) }}
        <span v-if="isFileTooLarge" class="warning-text"> - Too large for API</span>
      </span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FileUploader',
  data() {
    return {
      selectedFile: null
    };
  },
  computed: {
    isFileTooLarge() {
      return this.selectedFile && this.selectedFile.size > 25 * 1024 * 1024;
    }
  },
  methods: {
    onFileChange(event) {
      const file = event.target.files[0];
      this.selectedFile = file;
      this.$emit('file-selected', file);
    },
    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes';

      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));

      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
  }
};
</script>

<style scoped>
.uploader {
  margin: 10px 0;
}

.file-info {
  margin-top: 8px;
  font-size: 0.9em;
  display: flex;
  flex-direction: column;
}

.size-warning {
  color: #d32f2f;
  font-weight: bold;
}

.warning-text {
  font-style: italic;
}
</style>
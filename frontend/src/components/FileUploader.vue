<!-- src/components/FileUploader.vue -->
<template>
  <div class="uploader">
    <label for="fileInput">Upload WAV File</label>
    <input
      id="fileInput"
      type="file"
      accept=".wav"
      @change="onFileChange"
    />
  </div>
</template>

<script>
export default {
  name: 'FileUploader',
  methods: {
    onFileChange(event) {
      const file = event.target.files[0];
      this.$emit('file-selected', file);
    },
  },
};
</script>

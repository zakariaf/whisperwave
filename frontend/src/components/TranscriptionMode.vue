<!-- src/components/TranscriptionMode.vue -->
<template>
  <div class="transcription-mode">
    <label class="mode-label">Transcription Mode</label>
    <div class="radio-options">
      <div class="radio-option">
        <input
          type="radio"
          id="local"
          value="local"
          v-model="selectedMode"
          name="transcriptionMode"
        />
        <label for="local">Local Whisper</label>
      </div>
      <div class="radio-option">
        <input
          type="radio"
          id="api"
          value="api"
          v-model="selectedMode"
          name="transcriptionMode"
        />
        <label for="api">OpenAI API</label>
      </div>
    </div>
    <div v-if="selectedMode === 'api'" class="api-note">
      Note: OpenAI API has a 25MB file size limit
    </div>
  </div>
</template>

<script>
export default {
  name: 'TranscriptionMode',
  props: {
    modelValue: {
      type: String,
      default: 'local',
    },
  },
  computed: {
    selectedMode: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit('update:modelValue', value);
      },
    },
  },
};
</script>

<style scoped>
.transcription-mode {
  margin: 10px 0;
}

.mode-label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.radio-options {
  display: flex;
  gap: 20px;
}

.radio-option {
  display: flex;
  align-items: center;
  gap: 5px;
}

.api-note {
  margin-top: 5px;
  font-size: 0.85em;
  color: #d32f2f;
}
</style>
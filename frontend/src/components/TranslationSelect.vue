<!-- src/components/TranslationSelect.vue -->
<template>
  <div class="translation-select">
    <label for="translationSelect">Translate to (optional)</label>
    <select id="translationSelect" v-model="selectedLanguage">
      <option value="">No Translation</option>
      <option value="en">English</option>
      <option value="es">Spanish</option>
      <option value="fr">French</option>
      <option value="de">German</option>
      <option value="it">Italian</option>
      <option value="pt">Portuguese</option>
      <option value="nl">Dutch</option>
      <option value="ru">Russian</option>
      <option value="zh">Chinese</option>
      <option value="ja">Japanese</option>
      <option value="ko">Korean</option>
      <option value="ar">Arabic</option>
      <option value="hi">Hindi</option>
      <option value="tr">Turkish</option>
      <option value="fa">Persian/Farsi</option>
    </select>
    <div v-if="selectedLanguage" class="translation-note">
      Translation will use OpenAI API regardless of transcription mode
    </div>
  </div>
</template>

<script>
export default {
  name: 'TranslationSelect',
  props: {
    modelValue: {
      type: String,
      default: '',
    },
    sourceLanguage: {
      type: String,
      default: 'en',
    }
  },
  computed: {
    selectedLanguage: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit('update:modelValue', value);
      },
    },
    isSourceLanguage() {
      return this.selectedLanguage === this.sourceLanguage;
    }
  },
  watch: {
    sourceLanguage(newVal) {
      // If the selected language is the same as the new source language,
      // reset the translation (no need to translate to the same language)
      if (this.selectedLanguage === newVal) {
        this.selectedLanguage = '';
      }
    }
  }
};
</script>

<style scoped>
.translation-select {
  margin: 10px 0;
  display: flex;
  flex-direction: column;
}

.translation-select label {
  margin-bottom: 5px;
  font-weight: bold;
}

.translation-note {
  margin-top: 5px;
  font-size: 0.85em;
  color: #6c757d;
  font-style: italic;
}
</style>
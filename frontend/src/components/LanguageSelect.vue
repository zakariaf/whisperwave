<!-- src/components/LanguageSelect.vue -->
<template>
  <div class="language-select">
    <label for="languageSelect">Select Language</label>
    <select id="languageSelect" v-model="selectedLanguage">
      <option value="en">English</option>
      <option value="de">German</option>
      <!-- Add more languages as needed -->
    </select>
  </div>
</template>

<script>
export default {
  name: 'LanguageSelect',
  props: {
    modelValue: {
      type: String,
      default: 'en',
    },
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
  },
};
</script>

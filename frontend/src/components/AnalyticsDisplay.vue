<!-- src/components/AnalyticsDisplay.vue -->
<template>
  <div v-if="analytics" class="analytics-container">
    <h3>Transcription Analytics</h3>
    <div class="analytics-info">
      <div class="analytics-item">
        <span class="analytics-label">Processing Time:</span>
        <span class="analytics-value">{{ formatTime(analytics.processing_time) }}</span>
      </div>
      <div class="analytics-item">
        <span class="analytics-label">Mode:</span>
        <span class="analytics-value" :class="'mode-' + analytics.mode">
          {{ analytics.mode === 'local' ? 'Local Whisper' : 'OpenAI API' }}
        </span>
      </div>
      <div class="analytics-item">
        <span class="analytics-label">Whisper Model:</span>
        <span class="analytics-value">{{ analytics.model }}</span>
      </div>

      <!-- Show translation details if available -->
      <template v-if="analytics.translation_time">
        <div class="analytics-item translation-stats">
          <span class="analytics-label">Translation Time:</span>
          <span class="analytics-value">{{ formatTime(analytics.translation_time) }}</span>
        </div>
        <div class="analytics-item translation-stats" v-if="analytics.translation_model">
          <span class="analytics-label">Translation Model:</span>
          <span class="analytics-value">{{ analytics.translation_model }}</span>
        </div>
      </template>
    </div>

    <div v-if="comparisonStats.length > 0" class="comparison-container">
      <h4>Mode Comparison</h4>
      <table class="comparison-table">
        <thead>
          <tr>
            <th>Mode</th>
            <th>Avg. Processing Time</th>
            <th>Usage Count</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(stat, index) in comparisonStats" :key="index">
            <td class="mode-name">{{ stat.mode === 'local' ? 'Local Whisper' : 'OpenAI API' }}</td>
            <td>{{ formatTime(stat.avgTime) }}</td>
            <td>{{ stat.count }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Model usage statistics -->
    <div v-if="modelStats.length > 0" class="model-stats-container">
      <h4>Model Usage Statistics</h4>
      <div class="model-stats">
        <div
          v-for="(stat, index) in modelStats"
          :key="index"
          class="model-stat-item"
        >
          <div class="model-name">{{ stat.model }}</div>
          <div class="model-count">{{ stat.count }} uses</div>
          <div class="model-bar-container">
            <div
              class="model-bar"
              :style="{ width: stat.percentage + '%' }"
              :class="{ 'whisper-model': !stat.isTranslation, 'translation-model': stat.isTranslation }"
            ></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AnalyticsDisplay',
  props: {
    analytics: {
      type: Object,
      default: null
    }
  },
  computed: {
    comparisonStats() {
      // Calculate comparison statistics
      const stats = this.getStoredAnalytics();
      if (!stats || Object.keys(stats).length === 0) {
        return [];
      }

      const result = [];

      if (stats.local && stats.local.times.length > 0) {
        const avgTime = stats.local.times.reduce((sum, time) => sum + time, 0) / stats.local.times.length;
        result.push({
          mode: 'local',
          avgTime,
          count: stats.local.times.length
        });
      }

      if (stats.api && stats.api.times.length > 0) {
        const avgTime = stats.api.times.reduce((sum, time) => sum + time, 0) / stats.api.times.length;
        result.push({
          mode: 'api',
          avgTime,
          count: stats.api.times.length
        });
      }

      return result;
    },
    modelStats() {
      // Calculate model usage statistics
      const stats = this.getStoredAnalytics();
      if (!stats || Object.keys(stats).length === 0) {
        return [];
      }

      // Collect all models and their usage counts
      const models = {};
      let totalCount = 0;

      // Process Whisper models
      Object.keys(stats).forEach(mode => {
        if (stats[mode].models) {
          Object.keys(stats[mode].models).forEach(model => {
            const count = stats[mode].models[model];
            if (!models[model]) {
              models[model] = { count: 0, isTranslation: false };
            }
            models[model].count += count;
            totalCount += count;
          });
        }
      });

      // Process translation models
      if (stats.translation && stats.translation.models) {
        Object.keys(stats.translation.models).forEach(model => {
          const count = stats.translation.models[model];
          if (!models[model]) {
            models[model] = { count: 0, isTranslation: true };
          } else {
            // If model exists but is used for both, mark as translation too
            models[model].isTranslation = true;
          }
          models[model].count += count;
          totalCount += count;
        });
      }

      // Convert to array and calculate percentages
      return Object.keys(models).map(model => ({
        model,
        count: models[model].count,
        isTranslation: models[model].isTranslation,
        percentage: totalCount > 0 ? (models[model].count / totalCount) * 100 : 0
      })).sort((a, b) => b.count - a.count);
    }
  },
  mounted() {
    // If we have new analytics data, store it
    if (this.analytics) {
      this.storeAnalyticsData(this.analytics);
    }
  },
  watch: {
    analytics(newAnalytics) {
      if (newAnalytics) {
        this.storeAnalyticsData(newAnalytics);
      }
    }
  },
  methods: {
    formatTime(seconds) {
      return seconds.toFixed(2) + ' seconds';
    },
    getStoredAnalytics() {
      try {
        const stored = localStorage.getItem('transcriptionAnalytics');
        return stored ? JSON.parse(stored) : {};
      } catch (e) {
        console.error('Error parsing stored analytics:', e);
        return {};
      }
    },
    storeAnalyticsData(analytics) {
      try {
        // Get existing data
        const existingData = this.getStoredAnalytics();

        // Initialize if needed
        if (!existingData[analytics.mode]) {
          existingData[analytics.mode] = {
            times: [],
            models: {}
          };
        }

        // Add new timing data
        existingData[analytics.mode].times.push(analytics.processing_time);

        // Track model usage
        if (!existingData[analytics.mode].models[analytics.model]) {
          existingData[analytics.mode].models[analytics.model] = 0;
        }
        existingData[analytics.mode].models[analytics.model]++;

        // Track translation model if present
        if (analytics.translation_model) {
          if (!existingData.translation) {
            existingData.translation = {
              models: {}
            };
          }

          if (!existingData.translation.models[analytics.translation_model]) {
            existingData.translation.models[analytics.translation_model] = 0;
          }
          existingData.translation.models[analytics.translation_model]++;
        }

        // Store back to localStorage
        localStorage.setItem('transcriptionAnalytics', JSON.stringify(existingData));
      } catch (e) {
        console.error('Error storing analytics data:', e);
      }
    }
  }
};
</script>

<style scoped>
.analytics-container {
  margin-top: 20px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 4px;
  border: 1px solid #e9ecef;
}

h3 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 1.2em;
  color: #343a40;
}

h4 {
  margin-top: 20px;
  margin-bottom: 10px;
  font-size: 1.1em;
  color: #495057;
}

.analytics-info {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.analytics-item {
  flex: 1;
  min-width: 150px;
  padding: 10px;
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.analytics-label {
  display: block;
  font-size: 0.8em;
  color: #6c757d;
  margin-bottom: 5px;
}

.analytics-value {
  font-weight: bold;
  color: #212529;
}

.mode-local {
  color: #0066cc;
}

.mode-api {
  color: #00994d;
}

.translation-stats {
  border-left: 3px solid #6610f2;
}

.comparison-container {
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #dee2e6;
}

.comparison-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
  font-size: 0.9em;
}

.comparison-table th,
.comparison-table td {
  padding: 8px 12px;
  text-align: left;
  border-bottom: 1px solid #dee2e6;
}

.comparison-table th {
  background-color: #e9ecef;
  font-weight: bold;
  color: #495057;
}

.mode-name {
  font-weight: bold;
}

/* Model stats styling */
.model-stats-container {
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #dee2e6;
}

.model-stats {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 10px;
}

.model-stat-item {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
}

.model-name {
  width: 150px;
  font-weight: bold;
  font-size: 0.9em;
}

.model-count {
  width: 80px;
  font-size: 0.8em;
  color: #6c757d;
}

.model-bar-container {
  flex: 1;
  height: 12px;
  background-color: #e9ecef;
  border-radius: 6px;
  overflow: hidden;
}

.model-bar {
  height: 100%;
  border-radius: 6px;
}

.whisper-model {
  background-color: #0066cc;
}

.translation-model {
  background-color: #6610f2;
}
</style>
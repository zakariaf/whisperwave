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
        <span class="analytics-label">Model:</span>
        <span class="analytics-value">{{ analytics.model }}</span>
      </div>
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
</style>
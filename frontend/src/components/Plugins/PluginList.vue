<script setup>
import PluginItem from "@/components/Plugins/PluginItem.vue";

const props = defineProps({
  plugins: {
    type: Array,
    required: true,
  }
});
</script>

<template>
  <div v-if="plugins.length > 0" class="plugins-list">
    <PluginItem
      v-for="plugin in plugins"
      :key="plugin.plugin_id"
      :plugin="plugin"
    />
  </div>
</template>

<style scoped>
.plugins-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
}
</style>
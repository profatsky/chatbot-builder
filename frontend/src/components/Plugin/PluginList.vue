<script setup>
import PluginItem from "@/components/Plugin/PluginItem.vue";

const props = defineProps({
  plugins: {
    type: Array,
    required: true,
  }
});

const emits = defineEmits(['add-plugin']);
const addPluginEvent = (plugin) => {
  emits('add-plugin', plugin)
};
</script>

<template>
  <div v-if="plugins.length > 0" class="plugins-list">
    <PluginItem
      v-for="plugin in plugins"
      :key="plugin.plugin_id"
      :plugin="plugin"
      @add-plugin="addPluginEvent"
    />
  </div>
</template>

<style scoped>
.plugins-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
}

@media (min-width: 768px) and (max-width: 1169px) {
  .plugins-list {
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
  }
}
</style>
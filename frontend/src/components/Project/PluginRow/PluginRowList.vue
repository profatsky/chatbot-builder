<script setup>
import PluginRowItem from '@/components/Project/PluginRow/PluginRowItem.vue';

const props = defineProps({
  plugins: {
    type: Array,
    required: true,
  }
});

const emits = defineEmits(['remove-plugin']);
const removePluginEvent = (plugin) => {
  emits('remove-plugin', plugin)
};
</script>

<template>
  <div v-if="plugins.length > 0" class="plugin-list">
    <PluginRowItem
      v-for="plugin in plugins"
      :key="plugin.plugin_id"
      :plugin="plugin"
      @remove-plugin="removePluginEvent"
    />
  </div>
</template>

<style scoped>
.plugin-list {
  margin: 24px 0;
}

@media (min-width: 768px) and (max-width: 1169px) { 
  .plugin-list {
    margin: 16px 0;
  }
}

</style>
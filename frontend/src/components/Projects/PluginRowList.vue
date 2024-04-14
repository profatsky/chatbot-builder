<script setup>
import PluginRowItem from '@/components/Projects/PluginRowItem.vue';

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
  <div v-if="plugins.length > 0">
    <PluginRowItem
      v-for="plugin in plugins"
      :key="plugin.plugin_id"
      :plugin="plugin"
      @remove-plugin="removePluginEvent"
    />
  </div>
</template>

<style>

</style>
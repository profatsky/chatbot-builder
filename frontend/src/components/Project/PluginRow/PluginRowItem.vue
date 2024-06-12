<script setup>
const props = defineProps({
  plugin: {
    type: Object,
    required: true,
  }
});

const emits = defineEmits(['remove-plugin']);
const removePluginEvent = () => {
  emits('remove-plugin', props.plugin)
};
</script>

<template>
  <div class="plugin-row">
    <div class="plugin-row__name">{{ plugin.name }}</div>
    <div class="plugin-row__btns">
      <AppRoundButton 
        buttonType="redirect"
        @click="$router.push(`/plugins/${plugin.plugin_id}`)"
      />
      <AppRoundButton 
        @click="removePluginEvent"
        buttonType="delete"
      />
    </div>
  </div>
</template>

<style scoped>
.plugin-row {
  display: flex;
  gap: 24px;
  align-items: center;
  margin-bottom: 12px;
}

.plugin-row__name {
  font-size: 16px;
  line-height: 34px;
  font-weight: 400;
  letter-spacing: 0.75px;

  border-radius: 16px;
  background-color: var(--main-white);
  padding: 12px 28px;
  flex-grow: 1;
}

.plugin-row__btns {
  display: flex;
  gap: 12px;
}

@media (min-width: 768px) and (max-width: 1169px) {
  .plugin-row {
    gap: 12px;
    margin-bottom: 12px;
  }

  .plugin-row__name {
    font-size: 14px;
    line-height: 28px;

    border-radius: 12px;
    padding: 6px 20px;
  }

  .plugin-row__btns {
    display: flex;
    gap: 8px;
  }
}

@media (max-width: 767px) {
  .plugin-row {
    gap: 6px;
    margin-bottom: 8px;
  }

  .plugin-row__name {
    font-size: 8px;
    line-height: 12px;

    border-radius: 8px;
    padding: 6px 8px;
  }

  .plugin-row__btns {
    display: flex;
    gap: 4px;
  }
}
</style>
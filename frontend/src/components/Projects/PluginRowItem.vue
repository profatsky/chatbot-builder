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
      <AppRoundButton buttonType="redirect"/>
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
  margin-top: 12px;
}

.plugin-row__name {
  font-size: 16px;
  line-height: 34px;
  font-weight: 400;
  letter-spacing: 0.75px;

  border-radius: 10px;
  background-color: var(--main-white);
  padding: 12px 28px;
  flex-grow: 1;
}

.plugin-row__btns {
  display: flex;
  gap: 12px;
}
</style>
<script setup>
const props = defineProps({
  project: {
    type: Object,
    required: true,
  }
});

const emits = defineEmits(['choose-project']);
const chooseProjectEvent = () => {
  emits('choose-project', props.project)
};
</script>

<template>
  <div class="project-row">
    <div class="project-row__name">{{ project.name }}</div>
    <AppRoundButton 
      buttonType="redirect"
      @click="chooseProjectEvent"
    />
  </div>
</template>

<style scoped>
.project-row {
  display: flex;
  gap: 24px;
  align-items: center;
  margin-top: 12px;
}

.project-row__name {
  font-size: 16px;
  line-height: 34px;
  font-weight: 400;
  letter-spacing: 0.75px;

  border-radius: 10px;
  background-color: var(--light-gray);
  padding: 12px 28px;
  flex-grow: 1;
}
</style>
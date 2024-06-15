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
  margin-top: 16px;
}

.project-row__name {
  font-size: 16px;
  line-height: 34px;
  font-weight: 400;
  letter-spacing: 0.75px;

  border-radius: 16px;
  background-color: var(--light-gray);
  padding: 12px 28px;
  flex-grow: 1;
}

@media (min-width: 768px) and (max-width: 1169px) { 
  .project-row {
    gap: 18px;
    margin-top: 12px;
  }

  .project-row__name {
    font-size: 14px;
    line-height: 28px;
    padding: 6px 20px;
    border-radius: 12px;
  }
}

@media (max-width: 767px) {
  .project-row {
    gap: 12px;
    margin-top: 8px;
  }

  .project-row__name {
    font-size: 8px;
    line-height: 12px;
    padding: 6px 8px;
    border-radius: 8px;
  }
}
</style>
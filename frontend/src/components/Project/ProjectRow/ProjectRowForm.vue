<script setup>
import ProjectRowList from '@/components/Project/ProjectRow/ProjectRowList.vue';

const props = defineProps({
  projects: {
    type: Array,
    required: true
  }
});

const emits = defineEmits(['choose-project']);
const chooseProjectEvent = (project) => {
  emits('choose-project', project)
};
</script>

<template>
  <div class="choose-project">
    <h2 class="choose-project__title"><slot></slot></h2>
    <ProjectRowList 
      :projects="projects"
      @choose-project="chooseProjectEvent"
    />
  </div>
</template>

<style scoped>
.choose-project {
  width: 360px;
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.choose-project__title {
  font-size: 28px;
  font-weight: 600px;
  line-height: 32px;
  margin-bottom: 8px;
  text-align: center;
}

@media (min-width: 768px) and (max-width: 1169px) {
  .choose-project {
    width: 280px;
    gap: 12px;
  }

  .choose-project__title {
    font-size: 24px;
    line-height: 28px;
    margin-bottom: 6px;
  }
}

@media (max-width: 767px) { 
  .choose-project {
    width: 200px;
    gap: 8px
  }

  .choose-project__title {
    font-size: 16px;
    line-height: 20px;
    margin-bottom: 4px;
  }
}
</style>
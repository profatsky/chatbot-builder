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
  <div class="create-dialogue">
    <h2 class="create-dialogue__title">Добавить диалог в проект</h2>
    <ProjectRowList 
      :projects="projects"
      @choose-project="chooseProjectEvent"
    />
  </div>
</template>

<style scoped>
.create-dialogue {
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  width: 500px;
  padding: 0 24px;
}

.create-dialogue__title {
  font-size: 24px;
  font-weight: 600px;
  margin-top: 0;
  margin-bottom: 28px;
}
</style>

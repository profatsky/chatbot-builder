<script setup>
import ProjectRowItem from '@/components/Plugins/ProjectRowItem.vue';

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
  <div v-if="projects.length > 0" class="project-list">
    <ProjectRowItem
      v-for="project in projects"
      :key="project.project_id"
      :project="project"
      @choose-project="chooseProjectEvent"
    />
  </div>
</template>

<style scoped>
.project-list {
  width: 100%;
}
</style>
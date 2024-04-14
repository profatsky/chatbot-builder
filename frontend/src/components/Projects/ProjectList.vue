<script setup>
import ProjectItem from "@/components/Projects/ProjectItem.vue";

const props = defineProps({
  projects: {
    type: Array,
    required: true,
  }
});

const emits = defineEmits(['update-project', 'delete-project']);

const updateProjectEvent = (editedProject) => {
  emits('update-project', editedProject)
};

const deleteProjectEvent = (projectID) => {
  emits('delete-project', projectID)
};
</script>

<template>
  <div v-if="projects.length > 0" class="project-list">
    <ProjectItem
      v-for="project in projects"
      :key="project.project_id"
      :project="project"
      @update-project="updateProjectEvent"
      @delete-project="deleteProjectEvent"
    />
  </div>
</template>

<style>
</style>
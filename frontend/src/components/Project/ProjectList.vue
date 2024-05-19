<script setup>
import ProjectItem from "@/components/Project/ProjectItem.vue";

const props = defineProps({
  projects: {
    type: Array,
    required: true,
  }
});

const emits = defineEmits(['update-project', 'delete-project', 'download-code']);

const updateProjectEvent = (editedProject) => {
  emits('update-project', editedProject)
};

const deleteProjectEvent = (projectId) => {
  emits('delete-project', projectId)
};

const downloadCodeEvent = (projectId) => {
  emits('download-code', projectId);
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
      @download-code="downloadCodeEvent"
    />
  </div>
</template>

<style>
</style>
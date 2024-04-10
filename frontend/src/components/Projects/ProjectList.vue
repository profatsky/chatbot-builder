<script setup>
import ProjectItem from "@/components/Projects/ProjectItem.vue";

const props = defineProps({
  projects: {
    type: Array,
    required: true,
  }
});

const emits = defineEmits(['update-project']);

function updateProject(updatedProject) {
  emits('update-project', updatedProject)
}

</script>

<template>
  <div v-if="projects.length > 0">
    <ProjectItem
      v-for="project in projects"
      :key="project.project_id"
      :project="project"
      @update-project="updateProject"
    />
  </div>
</template>

<style>

</style>
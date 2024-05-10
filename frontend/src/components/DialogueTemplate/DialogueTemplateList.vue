<script setup>
import DialogueTemplateItem from '@/components/DialogueTemplate/DialogueTemplateItem.vue';

const props = defineProps({
  dialogueTemplates: {
    type: Array,
    required: true,
  }
});

const emits = defineEmits(['create-dialogue']);
const createDialogueEvent = (template) => {
  emits('create-dialogue', template);
};
</script>

<template>
  <div v-if="dialogueTemplates.length > 0" class="dialogue-templates-list">
    <DialogueTemplateItem
      v-for="template in dialogueTemplates"
      :key="template.template_id"
      :dialogue-template="template"
      @create-dialogue="createDialogueEvent"
    />
  </div>
</template>

<style scoped>
.dialogue-templates-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
}
</style>
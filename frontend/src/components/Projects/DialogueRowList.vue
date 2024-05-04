<script setup>
import DialoguRowItem from '@/components/Projects/DialogueRowItem.vue';

const props = defineProps({
  dialogues: {
    type: Array,
    required: true,
  },
  projectID: {
    type: Number,
    required: true,
  },
});

const emits = defineEmits(['update-dialogue', 'delete-dialogue']);

const updateDialogueEvent = (dialogue) => {
  emits('update-dialogue', dialogue)
};

const deleteDialogueEvent = (dialogue) => {
  emits('delete-dialogue', dialogue)
};
</script>

<template>
  <div v-if="dialogues.length > 0" class="dialogue-list">
    <DialoguRowItem
      v-for="dialogue in dialogues"
      :key="dialogue.dialogue_id"
      :dialogue="dialogue"
      :projectID="projectID"
      @update-dialogue="updateDialogueEvent"
      @delete-dialogue="deleteDialogueEvent"
    />
  </div>
</template>

<style scoped>
.dialogue-list {
  margin-bottom: 24px;
}
</style>
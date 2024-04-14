<script setup>
import DialoguRowItem from '@/components/Projects/DialogueRowItem.vue';

const props = defineProps({
  dialogues: {
    type: Array,
    required: true,
  }
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
      @update-dialogue="updateDialogueEvent"
      @delete-dialogue="deleteDialogueEvent"
    />
  </div>
</template>

<style scoped>
.dialogue-list {
  margin: 24px 0;
}
</style>
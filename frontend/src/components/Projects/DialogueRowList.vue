<script setup>
import DialoguRowItem from '@/components/Projects/DialogueRowItem.vue';

const props = defineProps({
  dialogues: {
    type: Array,
    required: true,
  }
});

const emits = defineEmits(['update-dialogue', 'delete-dialogue']);

const deleteDialogueEvent = (dialogue) => {
  emits('delete-dialogue', dialogue)
};
</script>

<template>
  <div v-if="dialogues.length > 0">
    <DialoguRowItem
      v-for="dialogue in dialogues"
      :key="dialogue.dialogue_id"
      :dialogue="dialogue"
      @delete-dialogue="deleteDialogueEvent"
    />
  </div>
</template>

<style>

</style>
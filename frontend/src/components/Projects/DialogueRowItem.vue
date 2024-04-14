<script setup>
import { ref, reactive } from 'vue';
import { debounce } from 'lodash';

const props = defineProps({
  dialogue: {
    type: Object,
    required: true,
  }
});

const editedDialogue = reactive({ ...props.dialogue });

const emits = defineEmits(['update-dialogue', 'delete-dialogue']);

const updateDialogueTriggerTypeEvent = () => {
  emits('update-dialogue', editedDialogue)
};

const updateDialogueTriggerValueEvent = debounce(() => {
  emits('update-dialogue', editedDialogue)
}, 3000);

const deleteDialogueEvent = () => {
  emits('delete-dialogue', props.dialogue)
};

const dialogueTrigerTypes = ref([
  { label: 'Текст', value: 'text' },
  { label: 'Команда', value: 'command' },
  { label: 'Кнопка', value: 'button' }
]);
</script>

<template>
  <div class="dialogue-row">
    <div class="dialogue-row__trigger">
      <AppSelect
        v-model="editedDialogue.trigger.event_type"
        :options="dialogueTrigerTypes"
        size="medium"
        required
        @change="updateDialogueTriggerTypeEvent"
        class="trigger__select"
      />
      <AppInput
        v-model="editedDialogue.trigger.value"
        required 
        placeholder="Ввидите текст"
        @input="updateDialogueTriggerValueEvent"
        class="trigger__input"
      />
    </div>
    <div class="dialogue-row__btns">
      <AppRoundButton buttonType="redirect"/>
      <AppRoundButton 
        @click="deleteDialogueEvent"
        buttonType="delete"
      />
    </div>
  </div>
</template>

<style scoped>
.dialogue-row {
  display: flex;
  gap: 24px;
  align-items: center;
  margin-top: 20px;
}

.dialogue-row__trigger {
  display: flex;
  gap: 24px;
  flex-grow: 1;
}

.trigger__input {
  flex-grow: 1;
}

.dialogue-row__btns {
  display: flex;
  gap: 12px;
}
</style>
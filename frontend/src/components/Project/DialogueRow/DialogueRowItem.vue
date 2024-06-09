<script setup>
import { ref, reactive } from 'vue';
import { debounce } from 'lodash';

const props = defineProps({
  dialogue: {
    type: Object,
    required: true,
  },
  projectID: {
    type: Number,
    required: true,
  },
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
        placeholder="Введите текст"
        @input="updateDialogueTriggerValueEvent"
        class="trigger__input"
        maxlength="64"
      />
    </div>
    <div class="dialogue-row__btns">
      <AppRoundButton 
        buttonType="redirect"
        @click="$router.push(`/projects/${projectID}/dialogues/${dialogue.dialogue_id}`)"
      />
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
  gap: 20px;
  align-items: center;
  margin-bottom: 20px;
}

.dialogue-row__trigger {
  display: flex;
  gap: 20px;
  flex-grow: 1;
}

.trigger__input {
  flex-grow: 1;
}

.dialogue-row__btns {
  display: flex;
  gap: 12px;
}

@media (min-width: 768px) and (max-width: 1169px) {
  .dialogue-row {
    gap: 12px;
    margin-bottom: 12px;
  }

  .dialogue-row__trigger {
    gap: 12px;
  }

  .dialogue-row__btns {
    gap: 8px;
  }
}
</style>
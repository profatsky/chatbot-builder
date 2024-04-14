<script setup>
import { ref, reactive } from 'vue';
import { debounce } from 'lodash';
import {useToast} from 'vue-toast-notification';
import ChangeNameForm from '@/components/Projects/ChangeNameForm.vue';
import PluginRowList from '@/components/Projects/PluginRowList.vue';
import { removePluginFromProject } from '@/api/projects';
import { updateDialogueTrigger, deleteDialogue } from '@/api/dialogues';
import DialogueRowList from '@/components/Projects/DialogueRowList.vue';
import { createDialogue } from '@/api/dialogues';

const toast = useToast();

const keyboardTypes = ref([
  { label: 'Inline Keyboard', value: 'inline_keyboard' },
  { label: 'Reply Keyboard', value: 'reply_keyboard' },
]);

const showChangeNameForm = ref(false);

const openChangeNameForm = () => {
  showChangeNameForm.value = true;
}
const closeChangeNameForm = () => {
  showChangeNameForm.value = false;
}

const props = defineProps({
  project: {
    type: Object,
    required: true
  }
});

const editedProject = reactive({ ...props.project });

const emits = defineEmits(['update-project', 'delete-project', 'create-dialogue']);

const updateProjectStartMessageEvent = debounce(() => {
  emits('update-project', editedProject)
}, 3000);

const updateProjectKeyboardTypeEvent = () => {
  emits('update-project', editedProject)
};

const updateProjectNameEvent = (name) => {
  editedProject.name = name;
  emits('update-project', editedProject)
  closeChangeNameForm();
};

const deleteProjectEvent = () => {
  emits('delete-project', editedProject.project_id)
};

const handleRemovePluginEvent = async (plugin) => {
  const { response, error } = await removePluginFromProject(editedProject.project_id, plugin.plugin_id);
  if (error.value) {
    if (error.value.response) {
      toast.error(error.value.response.data.detail)
    } else {
      toast.error('Что-то пошло не так...')
    }
  } else {
    editedProject.plugins = editedProject.plugins.filter(p => p.plugin_id !== plugin.plugin_id);
    toast.success('Плагин успешно удален');
  }
};

const handleUpdateDialogueEvent = async (dialogue) => {
  const { response, error } = await updateDialogueTrigger(
    editedProject.project_id,
    dialogue.dialogue_id,
    dialogue.trigger.event_type,
    dialogue.trigger.value
  );
  if (error.value) {
    if (error.value.response) {
      console.log(error.value.response)
      toast.error(error.value.response.data.detail)
    } else {
      toast.error('Что-то пошло не так...')
    }
  } else {
    const index = editedProject.dialogues.findIndex(
      d => d.dialogue_id === dialogue.dialogue_id
    )
    const responseData = response.value.data;
    editedProject.dialogues[index] = responseData;
    toast.success('Данные о диалоге обновлены');
  }
};

const handleDeleteDialogueEvent = async (dialogue) => {
  const { response, error } = await deleteDialogue(editedProject.project_id, dialogue.dialogue_id);
  if (error.value) {
    if (error.value.response) {
      toast.error(error.value.response.data.detail)
    } else {
      toast.error('Что-то пошло не так...')
    }
  } else {
    editedProject.dialogues = editedProject.dialogues.filter(d => d.dialogue_id !== dialogue.dialogue_id);
    toast.success('Диалог успешно удален');
  }
};

const handleCreateDialogueEvent = async () => {
  const dialogue = {
    triggerEventType: 'text',
    triggerValue: '',
  };

  const { response, error } = await createDialogue(
    editedProject.project_id, 
    dialogue.triggerEventType, 
    dialogue.triggerValue
  );
  if (error.value) {
    if (error.value.response) {
      toast.error(error.value.response.data.detail)
    } else {
      toast.error('Что-то пошло не так...')
    }
  } else {
    const responseData = response.value.data;
    editedProject.dialogues.push(responseData);
    toast.success('Диалог успешно создан');
  }
}

</script>

<template>
  <AppModal
    v-if="showChangeNameForm"
    @closeModal="closeChangeNameForm"
  >
    <ChangeNameForm
      :projectName="project.name"
      @update-project="updateProjectNameEvent"
    />
  </AppModal>

  <div class="project">
    <div class="project__management">
      <div class="project__name">
        <img src="@/assets/icons/telegram-purple.svg">
        <h2 class="name__text">{{ project.name }}</h2>
      </div>
      <div class="project__actions">
        <div class="action">
          <img src="@/assets/icons/export-gray.svg">
          <div>Получить код</div>
        </div>
        <div @click="openChangeNameForm" class="action">
          <img src="@/assets/icons/pencil-gray.svg">
          <div>Изменить название</div>
        </div>
        <div @click="deleteProjectEvent" class="action">
          <img src="@/assets/icons/remove-gray.svg">
          <div>Удалить чат-бота</div>
        </div>
      </div>
      <AppTextarea 
        v-model="editedProject.start_message"
        placeholder="Введите текст приветственного сообщения"
        class="textarea" 
        required
        @input="updateProjectStartMessageEvent"
      />
      <div class="project__keyboard">
        <p class="clue">Выберите тип кнопок для главного меню</p>
        <AppSelect 
          v-model="editedProject.start_keyboard_type"
          :options="keyboardTypes"
          required
          @change="updateProjectKeyboardTypeEvent"
        />
      </div>
    </div>
    <div class="dialogues">
        <h3 class="dialogues__title">Диалоги ({{ editedProject.dialogues.length }}/15)</h3>
        <DialogueRowList
          :dialogues="editedProject.dialogues"
          @update-dialogue="handleUpdateDialogueEvent"
          @delete-dialogue="handleDeleteDialogueEvent"
        />
        <AppButton 
          size="large" 
          importance="secondary"
          class="dialogue__add-btn"
          @click="handleCreateDialogueEvent"
        >
          Добавить диалог
        </AppButton>
      </div>
      <div class="plugins">
        <h3 class="plugins__title">Плагины ({{ editedProject.plugins.length }}/15)</h3>
        <PluginRowList 
          :plugins="editedProject.plugins"
          @remove-plugin="handleRemovePluginEvent"
        />
        <AppButton 
          size="large" 
          importance="secondary"
          class="plugin__add-btn"
        >
          Добавить плагин
        </AppButton>
      </div>
  </div>
</template>

<style scoped>
.textarea {
  box-sizing: border-box;
  width: 100%;
  height: 112px;
  resize: none;
}

.project {
  background-color: var(--light-gray);
  padding: 44px 48px;
  margin-bottom: 48px;
  border-radius: 16px;
  box-shadow: 0 0 16px 0 rgba(17, 17, 17, 0.04);
}

.project__management {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.project__name {
  display: flex;
  align-items: center;
  gap: 12px;

  text-wrap: nowrap;
}

.name__text {
  font-size: 20px;
  font-weight: 500px;
  letter-spacing: 1px;
}

.project__actions {
  display: flex;
  gap: 60px;

  color: var(--body-text);
  font-size: 16px;
  letter-spacing: 0.75px;
  line-height: 34px;
}

.action {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.clue {
  font-size: 16px;
  font-weight: 500;
  color: var(--body-text);
  letter-spacing: 0.75px;
  line-height: 28px;
  margin-bottom: 12px;
}

.dialogues,
.plugins {
  margin-top: 40px;
}

.dialogues__title,
.plugins__title {
  font-size: 16px;
  font-weight: 500;
  letter-spacing: 3px;
  line-height: 32px;
  color: var(--primary);
  text-transform: uppercase;
  margin-bottom: 24px;
}
</style>
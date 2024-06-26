<script setup>
import { ref, reactive } from 'vue';
import { debounce } from 'lodash';
import {useToast} from 'vue-toast-notification';

import { removePluginFromProject } from '@/api/projects';
import { updateDialogueTrigger, deleteDialogue } from '@/api/dialogues';
import { createDialogue } from '@/api/dialogues';

import DialogueRowList from '@/components/Project/DialogueRow/DialogueRowList.vue';
import PluginRowList from '@/components/Project/PluginRow/PluginRowList.vue';
import ChangeNameForm from '@/components/Project/ChangeNameForm.vue';

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

const emits = defineEmits(['update-project', 'delete-project', 'create-dialogue', 'download-code']);

const updateProjectStartMessageEvent = debounce(() => {
  emits('update-project', editedProject)
}, 500);

const updateProjectKeyboardTypeEvent = () => {
  emits('update-project', editedProject)
};

const downloadCodeEvent = () => {
  emits('download-code', editedProject.project_id);
};

const updateProjectNameEvent = (name) => {
  editedProject.name = name;
  emits('update-project', editedProject);
  closeChangeNameForm();
  toast.success('Название чат-бота изменено')
};

const deleteProjectEvent = () => {
  emits('delete-project', editedProject.project_id);
};

const handleRemovePluginEvent = async (plugin) => {
  editedProject.plugins = editedProject.plugins.filter(p => p.plugin_id !== plugin.plugin_id);
  const { response, error } = await removePluginFromProject(editedProject.project_id, plugin.plugin_id);
  if (error.value) {
    toast.error('Что-то пошло не так...');
  } else {
    toast.success('Плагин успешно удален');
  }
};

const handleUpdateDialogueEvent = async (dialogue) => {
  if (dialogue.trigger.event_type == 'command') {
    if (dialogue.trigger.value.startsWith('/')) {
      toast.warning('Cимвол "/" в Команде будет подставлен автоматически');
      dialogue.trigger.value = dialogue.trigger.value.substring(1);
    };
    
    if (dialogue.trigger.value.includes(' ')) {
      toast.warning('Команда не должна содержать пробелов');
      dialogue.trigger.value = dialogue.trigger.value.replace(/\s/g, '');
    };
  };

  const { response, error } = await updateDialogueTrigger(
    editedProject.project_id,
    dialogue.dialogue_id,
    dialogue.trigger.event_type,
    dialogue.trigger.value
  );
  if (error.value) {
    toast.error('Что-то пошло не так...');
  } else {
    const index = editedProject.dialogues.findIndex(
      d => d.dialogue_id === dialogue.dialogue_id
    )
    const responseData = response.value.data;
    editedProject.dialogues[index] = responseData;
  }
};

const handleDeleteDialogueEvent = async (dialogue) => {
  editedProject.dialogues = editedProject.dialogues.filter(d => d.dialogue_id !== dialogue.dialogue_id);
  const { response, error } = await deleteDialogue(editedProject.project_id, dialogue.dialogue_id);
  if (error.value) {
    toast.error('Что-то пошло не так...');
  } else {
    toast.success('Диалог успешно удален');
  }
};

const handleCreateDialogueEvent = async () => {
  if (editedProject.dialogues.length >= 10) {
    toast.error('В этом чат-боте максимальное количество диалогов!');
    return;
  };

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
    toast.error('Что-то пошло не так...');
  } else {
    const responseData = response.value.data;
    editedProject.dialogues.push(responseData);
    toast.success('Диалог успешно создан');
  }
};
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

    <div class="project__header">
      <img src="@/assets/icons/telegram-purple.svg" class="header__img">
      <p class="header__text">{{ project.name }}</p>
    </div>

    <div class="project__actions">
      <div @click="downloadCodeEvent" class="action">
        <img src="@/assets/icons/export-gray.svg" class="action__img">
        <div>Получить код</div>
      </div>
      <div @click="openChangeNameForm" class="action">
        <img src="@/assets/icons/pencil-gray.svg" class="action__img">
        <div>Изменить название</div>
      </div>
      <div @click="deleteProjectEvent" class="action">
        <img src="@/assets/icons/remove-gray.svg" class="action__img">
        <div>Удалить чат-бота</div>
      </div>
    </div>

    <div class="menu-message">
      <p class="hint">
        Введите текст, который чат-бот будет отправлять пользователям в главном меню. Советуем описать возможности чат-бота и доступные пользователям текстовые команды.
      </p>
      <AppTextarea 
        v-model="editedProject.start_message"
        placeholder="Введите текст сообщения"
        class="textarea" 
        required
        @input="updateProjectStartMessageEvent"
        maxlength="4000"
      />
    </div>
    
    <div class="project__keyboard">
      <p class="hint">Выберите тип кнопок для диалогов</p>
      <AppSelect 
        v-model="editedProject.start_keyboard_type"
        :options="keyboardTypes"
        required
        @change="updateProjectKeyboardTypeEvent"
      />
    </div>

    <div class="dialogues">
      <h3 class="dialogues__title">Диалоги ({{ editedProject.dialogues.length }}/10)</h3>
      
      <p class="hint">
        При добавлении диалога необходимо указать на какое сообщение будет реагировать ваш чат-бот, чтобы запустить этот диалог. На выбор представлены 3 типа событий: текстовое сообщение, команда, нажатие кнопки.
      </p>
      <DialogueRowList
        :dialogues="editedProject.dialogues"
        :projectID="project.project_id"
        @update-dialogue="handleUpdateDialogueEvent"
        @delete-dialogue="handleDeleteDialogueEvent"
      />
      <AppButton 
        size="medium" 
        importance="secondary"
        class="dialogue__add-btn"
        @click="handleCreateDialogueEvent"
      >
        Добавить диалог
      </AppButton>
    </div>

    <div class="plugins">
      <h3 class="plugins__title">Плагины ({{ editedProject.plugins.length }}/3)</h3>
      <PluginRowList 
        :plugins="editedProject.plugins"
        @remove-plugin="handleRemovePluginEvent"
      />
      <AppButton 
        size="medium" 
        importance="secondary"
        class="plugin__add-btn"
        @click="$router.push(`/plugins`)"
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

.project__header {
  display: flex;
  align-items: center;
  gap: 12px;

  text-wrap: nowrap;

  margin-bottom: 24px;
}

.header__img {
  width: 32px;
  height: 32px;
}

.header__text {
  font-size: 20px;
  font-weight: 500;
  letter-spacing: 1px;
}

.project__actions {
  display: flex;
  gap: 60px;

  color: var(--body-text);
  font-size: 16px;
  letter-spacing: 0.75px;
  line-height: 34px;

  margin-bottom: 28px;
}

.action {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.action__img {
  width: 24px;
  height: 24px;;
}

.hint {
  font-size: 14px;
  font-weight: 400;
  color: var(--body-text);
  letter-spacing: 0.75px;
  line-height: 28px;
  margin-bottom: 12px;
}

.menu-message {
  margin-bottom: 24px;
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
  margin-bottom: 12px;
}

.dialogue__add-btn,
.plugin__add-btn {
  width: 220px;
}

@media (min-width: 768px) and (max-width: 1169px) { 
  .project {
    padding: 20px 24px;
    margin-bottom: 28px;
    border-radius: 12px;
  }

  .project__header {
    gap: 12px;
    margin-bottom: 16px;
  }

  .header__img {
    width: 28px;
    height: 28px;
  }

  .header__text {
    font-size: 18px;
  }

  .project__actions {
    gap: 48px;
    font-size: 14px;
    line-height: 20px;
    margin-bottom: 20px;
  }

  .action__img {
    width: 20px;
    height: 20px;;
  }

  .hint {
    font-size: 12px;
    line-height: 20px;
    margin-bottom: 8px;
  }

  .textarea {
    height: 84px;
  }

  .menu-message {
    margin-bottom: 20px;
  }

  .dialogues,
  .plugins {
    margin-top: 32px;
  }

  .dialogues__title,
  .plugins__title {
    font-size: 14px;
    line-height: 24px;
    margin-bottom: 8px;
  }

  .dialogue__add-btn,
  .plugin__add-btn {
    width: 180px;
  }
}

@media (max-width: 767px) {
  .project {
    padding: 12px 16px;
    margin-bottom: 20px;
    border-radius: 8px;
  }

  .project__header {
    gap: 4px;
    margin-bottom: 12px;
  }

  .header__img {
    width: 20px;
    height: 20px;
  }

  .header__text {
    font-size: 12px;
  }

  .project__actions {
    flex-direction: column;
    gap: 8px;
    font-size: 8px;
    line-height: 16px;
    margin-bottom: 16px;
  }

  .action__img {
    width: 16px;
    height: 16px;;
  }

  .hint {
    font-size: 8px;
    line-height: 12px;
    margin-bottom: 8px;
  }

  .textarea {
    height: 64px;
  }

  .menu-message {
    margin-bottom: 16px;
  }

  .dialogues,
  .plugins {
    margin-top: 20px;
  }

  .dialogues__title,
  .plugins__title {
    font-size: 10px;
    line-height: 16px;
    margin-bottom: 8px;
  }

  .dialogue__add-btn,
  .plugin__add-btn {
    width: 130px;
  }
}
</style>
<script setup>
import { ref, reactive } from 'vue';
import { debounce } from 'lodash';
import {useToast} from 'vue-toast-notification';
import ChangeNameForm from '@/components/Projects/ChangeNameForm.vue';
import PluginRowList from '@/components/Projects/PluginRowList.vue';
import { removePluginFromProject } from '@/api/projects';
import { deleteDialogue } from '@/api/dialogues';
import DialogueRowList from '@/components/Projects/DialogueRowList.vue';

const toast = useToast();

const keyboardTypes = ref([
  { label: 'Inline Keyboard', value: 'inline_keyboard' },
  { label: 'Reply Keyboard', value: 'reply_keyboard' },
]);

const props = defineProps({
  project: {
    type: Object,
    required: true
  }
});

const editedProject = reactive({ ...props.project });

const showChangeNameForm = ref(false);

const openChangeNameForm = () => {
  showChangeNameForm.value = true;
}
const closeChangeNameForm = () => {
  showChangeNameForm.value = false;
}

const emits = defineEmits(['update-project', 'delete-project']);

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
    const index = editedProject.plugins.findIndex(
      p => p.plugin_id === plugin.plugin_id
    );
    if (index !== -1) {
      editedProject.plugins = editedProject.plugins.filter(p => p.plugin_id !== plugin.plugin_id);
      toast.success('Плагин успешно удален');
    } else {
      toast.success('Что-то пошло не так');
    }
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

  console.log('Диалог должен быть удален!', dialogue)
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
        <h3 class="dialogues__title">Диалоги (0/15)</h3>
        <DialogueRowList
          :dialogues="editedProject.dialogues"
          @delete-dialogue="handleDeleteDialogueEvent"
        />
        <AppButton 
          size="large" 
          importance="secondary"
          class="dialogue__add-btn"
        >
          Добавить диалог
        </AppButton>
      </div>
      <div class="plugins">
        <h3 class="plugins__title">Плагины (0/15)</h3>
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
  margin-top: 48px;
  border-radius: 16px;
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

.dialogue__add-btn,
.plugin__add-btn {
  margin-top: 24px;
}

</style>
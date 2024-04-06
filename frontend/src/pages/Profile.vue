<script setup>
import { ref, onMounted } from 'vue';
import SidebarNavigation from '@/components/SidebarNavigation.vue';
import Footer from '@/components/Footer.vue';
import { getUserProfile } from '@/api/users';
import {useToast} from 'vue-toast-notification';
import AppNotification from '@/components/UI/AppNotification.vue';

const email = ref('');
const registeredAt = ref('');
const userData = ref({});

const toast = useToast();

function formatDate(dateObject) {
  const day = dateObject.getDate();
  const month = dateObject.getMonth() + 1;
  const year = dateObject.getFullYear()
  const formattedDate = `${day < 10 ? '0' + day : day}.${month < 10 ? '0' + month : month}.${year}`
  return formattedDate;
};

onMounted(async () => {
  const { response, error } = await getUserProfile();
  if (error.value) {
    if (error.value.response) {
      toast.error(error.value.response.data.detail)
    } else {
      toast.error('Что-то пошло не так...')
    }
  } else {
    const responseData = response.value.data;
    userData.value = response.value.data;

    const dateObject = new Date(responseData.registered_at);
    userData.value.registered_at = formatDate(dateObject)
  }
});
</script>

<template>
  <SidebarNavigation/>
  <main>
    <div class="container">
      <div class="profile">
        <h1 class="profile__title">Профиль</h1>
        <div class="profile__info">
          <div class="column">
            <div class="info-item">
              <img src="@/assets/icons/mail-purple.svg">
              <div class="info-item_text">
                <div class="info-item__name">Почта</div>
                <div class="info-item__value">{{ userData.email }}</div>
              </div>
            </div>
            <div class="info-item">
              <img src="@/assets/icons/calendar-purple.svg">
              <div class="info-item_text">
                <div class="info-item__name">Дата регистрации</div>
                <div class="info-item__value">{{ userData.registered_at }}</div>
              </div>
            </div>
            <div class="info-item">
              <img src="@/assets/icons/robot-face-purple.svg">
              <div class="info-item_text">
                <div class="info-item__name">Количество чат-ботов</div>
                <div class="info-item__value">5</div>
              </div>
            </div>
          </div>

          <div class="column">
            <AppNotification status="success" v-if="userData.is_verified">
              <template v-slot:title>Email подтвержден</template>
              <template v-slot:description>
                Вам доступны все функции конструктора чат-ботов. Если вы захотите изменить электронную почту, вам снова потребуется подтверждение.
              </template>
            </AppNotification>
            <AppNotification status="error" v-else>
              <template v-slot:title>Email не подтвержден</template>
              <template v-slot:description>
                У вас нет доступа к основным функциям конструктора чат-ботов.<br>
                Требуется подтверждение Email.
              </template>
            </AppNotification>
            <div class="buttons">
              <AppButton size="small" importance="secondary">Подтвердить Email</AppButton>
              <AppButton size="small" importance="secondary">Изменить Email</AppButton>
              <AppButton size="small" importance="secondary">Изменить пароль</AppButton>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
  <Footer/>
</template>

<style scoped>

.profile__title {
  margin: 48px 0;
}

.profile__info {
  display: flex;
  gap: 98px;
}

.column  {
  display: flex;
  flex-direction: column;
  gap: 48px;
}

.info-item {
  display: flex;
  gap: 16px;
}

.info-item__text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-item__name {
  font-size: 20px;
  font-weight: 500;
  letter-spacing: 1px;
  color: var(--body-text);
}

.info-item__value {
  font-size: 16px;
  font-weight: 400;
  letter-spacing: 1px;
  color: var(--body-text);
}

.buttons {
  display: flex;
  flex-direction: row;
  gap: 42px
}

</style>
<script setup>
import { ref, onMounted } from 'vue';
import AppNotification from '@/components/UI/AppNotification.vue';
import SidebarNavigation from '@/components/Sidebar/SidebarNavigation.vue';
import { getUserProfile } from '@/api/users';
import { useToast } from 'vue-toast-notification';

const userData = ref({});
const toast = useToast();

function formatDate(dateObject) {
  const day = dateObject.getDate();
  const month = dateObject.getMonth() + 1;
  const year = dateObject.getFullYear();
  const formattedDate = `${day < 10 ? '0' + day : day}.${month < 10 ? '0' + month : month}.${year}`
  return formattedDate;
};

onMounted(async () => {
  const { response, error } = await getUserProfile();
  if (error.value) {
    toast.error('Что-то пошло не так...');
  } else {
    const responseData = response.value.data;
    userData.value = response.value.data;

    const dateObject = new Date(responseData.registered_at);
    userData.value.registered_at = formatDate(dateObject);
  }
});
</script>

<template>
  <SidebarNavigation/>
  <main>
    <div class="container">
      <div class="page__content">
        <div class="page__header">
          <h1 class="header__title">Профиль</h1>
        </div>
        <div class="page__body">
          <div class="profile">
            <div class="profile__img">
              <img src="@/assets/img/base-avatar.svg">
            </div>
            <div class="profile__info">
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
          </div>
          <AppNotification status="primary">
            <template v-slot:title>Вы среди первой тысячи зарегистрированных пользователей</template>
            <template v-slot:description>
              <p class="description__main">
                Вам доступен весь функционал нашего конструктора чат-ботов без ограничений! Мы будем очень признательны, если вы поделитесь обратной связью, пожеланиями и замечаниями по нашему сервису.
              </p>
              <p class="description__contacts">
                Связяться с нами в ВКонтакте: 
                <a class="social-network-link" href="https://vk.com/profatsky" target="_blank">
                  vk.com/profatsky
                </a>
              </p>
              <p class="description__contacts">
                Связаться с нами в Telegram: 
                <a class="social-network-link" href="https://t.me/profatsky" target="_blank">
                  t.me/profatsky
                </a>
              </p>
            </template>
          </AppNotification>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>

.page__content {
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.page__header {
  margin: 40px 0px 36px 0px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header__title {
  font-size: 32px;
  line-height: 40px;
}

.page__body {
  margin: 0 auto;
}

.profile {
  display: flex;
  align-items: center;
  gap: 118px;
  margin-bottom: 80px;
}

.profile__img img {
  width: 250px;
  height: 250px;
}

.profile__info {
  display: flex;
  flex-direction: column;
  gap: 48px;
}

.info-item {
  display: flex;
  gap: 16px;
}

.info__item img {
  width: 36px;
  height: 36px;
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

.description__main {
  margin-bottom: 12px;
}

.social-network-link {
  color: var(--primary);
}

@media (max-width: 768px) {
  .page__header {
    margin: 28px 0px 40px 0px;
  }

  .header__title {
    font-size: 24px;
    line-height: 28px;
  }

  .page__body {
    margin: 0;
  }

  .profile {
    gap: 60px;
    margin-bottom: 48px;
  }

  .profile__img img {
    width: 200px;
    height: 200px;
  }

  .profile__info {
    gap: 24px;
  }

  .info-item {
    gap: 12px;
  }

  .info__item img {
    width: 30px;
    height: 30px;
  }

  .info-item__name {
    font-size: 18px;
  }

  .info-item__value {
    font-size: 14px;
  }
}
</style>
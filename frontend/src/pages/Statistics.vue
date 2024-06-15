<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { getStatistics } from '@/api/statistics.js';
import SidebarNavigation from '@/components/Sidebar/SidebarNavigation.vue';

const router = useRouter();
const userCount = ref(0);
const projectCount = ref(0); 

onMounted(async () => {
  const { response, error } = await getStatistics();
  if (error.value) {
    router.push('/');
  } else {
    const responseData = response.value.data;
    userCount.value = responseData.user_count;
    projectCount.value = responseData.project_count;
  }
});
</script>

<template>
  <SidebarNavigation/>
  <main>
    <div class="container">
      <div class="page__content">
        <div class="statistics">
          <h1 class="statistics__title">Статистика конструктора</h1>
        </div>
        <div class="statistics__cards-list">
          <div class="card">
              <img src="@/assets/img/users.svg" class="card__img">
              <h3 class="card__name">Количество пользователей</h3>
              <p class="card__value">{{ userCount }}</p>
          </div>
          <div class="card">
              <img src="@/assets/img/chatbot.svg" class="card__img">
              <h3 class="card__name">Количество чат-ботов</h3>
              <p class="card__value">{{ projectCount }}</p>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>

.statistics__title {
  font-size: 32px;
  line-height: 40px;
  margin: 40px 0px 36px 0px;
}

.statistics__cards-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
}

.card {
  background-color: var(--light-gray);
  border-radius: 16px;
  padding: 28px 32px;
  margin-bottom: 10px;

  display: flex;
  flex-direction: column;
  gap: 30px;
  text-align: center;
  align-items: center;

  box-shadow: 0 0 16px 0 rgba(17, 17, 17, 0.04);
}

.card__img {
  height: 200px;
}

.card__name {
  font-size: 28px;
  font-weight: 500;
  width: 250px;
  line-height: 40px;
  letter-spacing: 1px;
}

.card__value {
  font-size: 64px;
  font-weight: 700;
  letter-spacing: 1px;
  color: var(--primary);
}

@media (min-width: 768px) and (max-width: 1169px) {
  .statistics__title {
    font-size: 24px;
    line-height: 28px;
    margin: 28px 0px 24px 0px;
  }

  .statistics__cards-list {
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
  }

  .card {
    padding: 20px 24px;
    gap: 20px;
    margin-bottom: 4px;
  }

  .card__img {
    height: 160px;
  }

  .card__name {
    font-size: 24px;
    line-height: 36px;
    width: 210px;
  }

  .card__value {
    font-size: 48px;
  }
}

@media (max-width: 767px) {
  .statistics__title {
    font-size: 16px;
    line-height: 20px;
    margin: 18px 0px 20px 0px;
  }

  .statistics__cards-list {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
  }

  .card {
    padding: 18px 12px;
    width: 160px;
    gap: 12px;
  }

  .card__img {
    height: 60px;
  }

  .card__name {
    font-size: 12px;
    line-height: 15px;
    width: 85px;
  }

  .card__value {
    font-size: 36px;
    line-height: 44px;
  }
}
</style>
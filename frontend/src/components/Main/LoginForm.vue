<script setup>
import { ref } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import { loginUser } from '@/api/auth';
import {useToast} from 'vue-toast-notification';
import 'vue-toast-notification/dist/theme-bootstrap.css';

const email = ref('');
const password = ref('');
const showPassword = ref(false);

const checkPasswordLength = () => {
  return (password.value.length >= 8 && password.value.length <= 32);
}

const store = useStore();
const router = useRouter();
const toast = useToast();

const submitForm = async () => {
  if (!checkPasswordLength()) {
    toast.error('Длина пароля должна быть от 8 до 32 символов!');
    return
  }

  const { response, error } = await loginUser(email.value, password.value)
  if (error.value) {
    if (error.value.response) {
      toast.error(error.value.response.data.detail)
    } else {
      toast.error('Что-то пошло не так...')
    }
  } else {
    store.dispatch('login');
    toast.success(response.value.data.detail)
    router.push({ path: '/profile' })
  }
}

</script>

<template>
  <div class="login">
    <h2 class="login-title">Вход</h2>
    <form @submit.prevent="submitForm" class="login-form">
      <AppInput
        type="email"
        id="email" 
        v-model="email" 
        required 
        autocomplete="username"
        placeholder="Введите Email"
      />
      <AppInput
        :type="showPassword ? 'text' : 'password'" id="password" 
        v-model="password" 
        required 
        autocomplete="new-password"
        placeholder="Введите пароль"
      />
      <div class="login-form__show-password-checkbox">
        <input 
          type="checkbox" 
          v-model="showPassword"
        >
        <label>Показать пароль</label>
      </div>

      <AppButton 
        type="submit" 
        size="medium" 
        importance="primary"
        class="login-form__btn"
      >
        Войти
      </AppButton>
    </form>
  </div>
</template>

<style scoped>
.login {
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  width: 500px;
}

.login-title {
  font-size: 36px;
  font-weight: 600px;
  margin-top: 0;
  margin-bottom: 28px;
}

.input {
  width: 325px;
  background-color: var(--light-gray);
}

.login-form {
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  width: 370px;
  gap: 16px;
}

.login-form__show-password-checkbox {
  display: flex;
  gap: 8px;

  font-family: 'Montserrat', 'sans-serif';
  font-size: 16px;
  letter-spacing: 0.75px;
  color: var(--body-text);
  margin-right: auto;
}

.login-form__btn {
  margin-top: 20px;
}
</style>
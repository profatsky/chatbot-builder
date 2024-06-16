<script setup>
import { ref } from 'vue';
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
    toast.success(response.value.data.detail)
    router.push({ path: '/profile' })
  }
}

const emits = defineEmits(['open-register-form']);
const openRegisterFormEvent = () => {
  emits('open-register-form');
};
</script>

<template>
  <form @submit.prevent="submitForm" class="login">
    <h2 class="login__title">Вход</h2>
    <AppInput
      type="email"
      id="email" 
      v-model="email" 
      required 
      autocomplete="username"
      placeholder="Введите Email"
      class="login__input"
    />
    <AppInput
      :type="showPassword ? 'text' : 'password'" id="password" 
      v-model="password" 
      required 
      autocomplete="new-password"
      placeholder="Введите пароль"
      class="login__input"
    />
    <div class="login__show-password-checkbox">
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
      class="login__btn"
    >
      Войти
    </AppButton>
    <p class="login__register-hint">
      Нет учетной записи? <span @click="openRegisterFormEvent">Зарегистрируйтесь</span>
    </p>
  </form>
</template>

<style scoped>
.login {
  width: 360px;
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.login__title {
  font-size: 28px;
  font-weight: 600px;
  line-height: 32px;
  margin-bottom: 8px;
}

.login__input {
  width: 312px;
  background-color: var(--light-gray);
}

.login__show-password-checkbox {
  display: flex;
  gap: 8px;

  font-family: 'Montserrat', 'sans-serif';
  font-size: 16px;
  line-height: 20px;
  letter-spacing: 0.75px;
  color: var(--body-text);
  
  margin-right: auto;
}

.login__btn {
  width: 100%;
}

.login__register-hint {
  font-size: 16px;
  line-height: 20px;
}

.login__register-hint span {
  color: var(--primary-dark);
  cursor: pointer;
}

@media (min-width: 768px) and (max-width: 1169px) {
  .login {
    width: 280px;
    gap: 12px;
  }

  .login__title {
    font-size: 24px;
    line-height: 28px;
    margin-bottom: 6px;
  }

  .login__input{
    width: 240px;
  }

  .login__show-password-checkbox {
    gap: 6px;
    font-size: 12px;
    line-height: 18px;
  }

  .login__register-hint {
    font-size: 12px;
    line-height: 18px;
  }
}

@media (max-width: 767px) { 
  .login {
    width: 200px;
    gap: 8px
  }

  .login__title {
    font-size: 16px;
    line-height: 20px;
    margin-bottom: 4px;
  }

  .login__input{
    width: 184px;
  }

  .login__show-password-checkbox {
    gap: 4px;
    font-size: 8px;
    line-height: 12px;
  }
  
  .login__register-hint {
    font-size: 8px;
    line-height: 12px;
  }
}
</style>
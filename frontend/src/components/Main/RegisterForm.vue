<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { registerUser } from '@/api/auth';
import {useToast} from 'vue-toast-notification';
import 'vue-toast-notification/dist/theme-bootstrap.css';

const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const showPassword = ref(false);

const checkPasswordsMatch = () => {
  return password.value === confirmPassword.value;
};

const checkPasswordLength = () => {
  return (password.value.length >= 8 && password.value.length <= 32);
};

const router = useRouter();
const toast = useToast();


const submitForm = async () => {
  if (!checkPasswordLength()) {
    toast.error('Длина пароля должна быть от 8 до 32 символов!');
    return
  }

  if (!checkPasswordsMatch()) {
    toast.error('Введенные пароли должны совпадать!');
    return
  }

  const { response, error } = await registerUser(email.value, password.value)
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
};

const emits = defineEmits(['open-login-form']);
const openLoginFormEvent = () => {
  emits('open-login-form');
};
</script>

<template>
  <form @submit.prevent="submitForm" class="register">
    <h2 class="register__title">Регистрация</h2>
    <AppInput
      type="email"
      id="email" 
      v-model="email" 
      required 
      autocomplete="username"
      placeholder="Введите Email"
      class="register__input"
    />
    <AppInput
      :type="showPassword ? 'text' : 'password'" id="password" 
      v-model="password" 
      required 
      autocomplete="new-password"
      placeholder="Введите пароль"
      class="register__input"
    />
    <AppInput
      :type="showPassword ? 'text' : 'password'" id="confirmPassword" 
      v-model="confirmPassword" 
      required 
      autocomplete="new-password"
      placeholder="Введите пароль повторно"
      class="register__input"
    />
    <div class="register__show-password-checkbox">
      <input type="checkbox" v-model="showPassword">
      <label>Показать пароль</label>
    </div>

    <div class="register__personal-data-checkbox">
      <input type="checkbox" required>
      <label>
        Я даю свое согласие на <a href="/personal-data-processing-policy" target="_blank">обработку моих персональных данных</a>
      </label>
    </div>

    <AppButton 
      type="submit" 
      size="medium" 
      importance="primary"
      class="register__btn"
    >
      Зарегистрироваться
    </AppButton>
    <p class="register__login-hint">
      Уже зарегистрированы? <span @click="openLoginFormEvent">Войдите</span>
    </p>
  </form>
</template>

<style scoped>
.register {
  width: 360px;
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.register__title {
  font-size: 28px;
  font-weight: 600px;
  line-height: 32px;
  margin-bottom: 8px;
}

.register__input {
  width: 312px;
  background-color: var(--light-gray);
}

.register__show-password-checkbox,
.register__personal-data-checkbox {
  display: flex;
  gap: 8px;

  font-family: 'Montserrat', 'sans-serif';
  font-size: 16px;
  line-height: 20px;
  letter-spacing: 0.75px;
  color: var(--body-text);
  
  margin-right: auto;
}

.register__personal-data-checkbox a {
  font-weight: 500;
  color: var(--primary-dark);
}

.register__btn {
  width: 100%;
}

.register__login-hint {
  font-size: 16px;
  line-height: 20px;
}

.register__login-hint span {
  color: var(--primary-dark);
  cursor: pointer;
}

@media (min-width: 768px) and (max-width: 1169px) {
  .register {
    width: 280px;
    gap: 12px;
  }

  .register__title {
    font-size: 24px;
    line-height: 28px;
    margin-bottom: 6px;
  }

  .register__input{
    width: 240px;
  }

  .register__show-password-checkbox,
  .register__personal-data-checkbox {
    gap: 6px;
    font-size: 12px;
    line-height: 18px;
  }

  .register__login-hint {
    font-size: 12px;
    line-height: 18px;
  }
}

@media (max-width: 767px) { 
  .register {
    width: 200px;
    gap: 8px
  }

  .register__title {
    font-size: 16px;
    line-height: 20px;
    margin-bottom: 4px;
  }

  .register__input{
    width: 184px;
  }

  .register__show-password-checkbox,
  .register__personal-data-checkbox {
    gap: 4px;
    font-size: 8px;
    line-height: 12px;
  }

  .register__login-hint {
    font-size: 8px;
    line-height: 12px;
  }
}
</style>
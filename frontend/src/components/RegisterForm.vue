<script>
import AppButton from '@/components/UI/AppButton.vue';

export default {
  data() {
    return {
      email: "",
      password: "",
      confirmPassword: "",
      showPassword: false
    }
  },
  methods: {
    submitForm() {
      if (this.password !== this.confirmPassword) {
        alert('Пароли не совпадают');
        return;
      }
      alert('Данные отправлены на сервер');
    }
  }
}

</script>

<template>
  <div class="register">
    <h2 class="register-title">Регистрация</h2>
    <form @submit.prevent="submitForm" class="register-form">
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
      <AppInput
        :type="showPassword ? 'text' : 'password'" id="confirmPassword" 
        v-model="confirmPassword" 
        required 
        autocomplete="new-password"
        placeholder="Введите пароль повторно"
      />
      <div class="register-form__show-password-checkbox">
        <input 
          type="checkbox" 
          v-model="showPassword"
        >
        <label>Показать пароль</label>
      </div>

      <div class="register-form__personal-data-confirm">
          <input type="checkbox" required>
          <label>
            Я даю свое согласие на <a href="#">обработку моих персональных данных</a>
          </label>
        </div>

      <AppButton 
        type="submit" 
        size="medium" 
        importance="primary"
        class="register-form__btn"
      >
        Зарегистрироваться
      </AppButton>
    </form>
  </div>
</template>

<style scoped>
.register {
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  width: 500px;
}

.register-title {
  font-size: 36px;
  font-weight: 600px;
  margin-top: 0;
  margin-bottom: 28px;
}

.input {
  width: 325px;
  background-color: var(--light-gray);
}

.register-form {
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  width: 370px;
  gap: 16px;
}

.register-form__show-password-checkbox,
.register-form__personal-data-confirm {
  display: flex;
  gap: 8px;

  font-family: 'Montserrat', 'sans-serif';
  font-size: 16px;
  letter-spacing: 0.75px;
  color: var(--body-text);
  margin-right: auto;
}

.register-form__personal-data-confirm a {
  font-weight: 500;
  color: var(--primary-dark);
}

.register-form__btn {
  width: 300px;
  margin-top: 20px;
}

</style>
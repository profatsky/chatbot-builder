<script>
export default {
  data() {
    return {
      email: "",
      password: "",
      showPassword: false
    }
  },
  methods: {
    submitForm() {
      alert('Данные отправлены на сервер');
    }
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
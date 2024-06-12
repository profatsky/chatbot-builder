<script setup>
import SidebarNavigation from '@/components/Sidebar/SidebarNavigation.vue';
</script>

<template>
  <SidebarNavigation/>
  <main>
    <div class="container">
      <div class="page__content">
        <div class="page__header">
          <h1 class="header__title">Руководство для пользователей</h1>
        </div>
        
        <ul class="toc">
          <li><a href="#working-with-chatbots">Как работать с чат-ботами в конструкторе</a></li>
          <li><a href="#downloading-chatbot-code">Как скачать программный код чат-бота</a></li>
          <li><a href="#configuring-settings">Настройки конфигурации</a></li>
          <li><a href="#setting-up-environment">Настройка виртуального окружения, установка пакетов и запуск</a></li>
        </ul>

        <section id="working-with-chatbots">
          <h2>Как работать с чат-ботами в конструкторе</h2>
          <p>
            Чат-боты для Telegram – это автоматизированные собеседники, которые выполняют различные задачи: отвечают на вопросы, продают товары, предоставляют информацию и т.д.
          </p>
          <p>
            На странице <a href="/projects">Чат-боты</a> вы можете работать с вашими создаваемыми чат-ботами. Каждый чат-бот включает в себя диалоги и плагины.
          </p>
          <p>
            Диалоги – это сценарии общения с чат-ботом. Чтобы чат-бот понимал, когда запускать тот или иной диалог, необходимо явно указать тип и текст сообщения, на которое будет реагировать чат-бот. На выбор доступно 3 типа сообщений:
          </p>
          <ul>
            <li>отправка текста (чат-бот реагирует на отправленный текст)</li>
            <li>отправка команды (чат-бот реагирует на отправленную команду, начинающуюся с символа "/")</li>
            <li>нажатие кнопки (чат-бот реагирует на отправку сообщения с помощью кнопки в меню)</li>
          </ul>
          <p>
            Каждый диалог состоит из блоков, а каждый блок – это действие, которое совершает чат-бот. У чат-ботов есть 6 типов блоков.
          </p>
          <p>
            Плагины – это готовые программные модули, которые легко добавляются в чат-ботов. Плагины содержат новый функционал, который невозможно создать самостоятельно без навыков программирования.
          </p>
        </section>
        
        <section id="downloading-chatbot-code">
          <h2>Как скачать программный код чат-бота</h2>
          <p>
            На странице <a href="/projects">Чат-боты</a> выбрать одного из чат-ботов и нажать кнопку "Получить код". Начнется скачивание ZIP-архива со всеми необходимыми для запуска файлами.
          </p>
        </section>

        <section id="configuring-settings">
          <h2>Настройки конфигурации</h2>
          <p>
            Выполните следующие действия для успешной настройки конфигурации:
          </p>
          <ul>
            <li>создайте отдельную папку для чат-бота и перенесите в нее все файлы из ZIP-архива</li>
            <li>в файле .env укажите токен чат-бота (получите его в чат-боте <a href="https://t.me/BotFather">@BotFather</a>) и ваш идентификатор в Telegram (получите его в чат-боте <a href="https://t.me/getmyid_bot">@getmyid_bot</a>)</li>
            <li>если вы используете отправку писем на электронную почту, необходимо указать вашу Gmail почту и пароль в файле .env, а также пароль приложения Google (как получить пароль приложения Google читайте по <a href="https://support.google.com/mail/answer/185833?hl=ru">ссылке</a></li>
          </ul>
        </section>
        
        <section id="setting-up-environment">
          <h2>Настройка виртуального окружения, установка пакетов и запуск</h2>
          <p>
            Выполните следующие действия для успешной настройки виртуального окружения, установки пакетов и запуска:
          </p>
          <p>
            Установите Python версии 3.10 или выше с <a href="https://www.python.org/downloads/release/python-3124/">официального сайта</a> (при установке ставьте галочки на все пункты).
          </p>
          <p>
            В папке с чат-ботом откройте командную строку и в зависимости от ОС выполните необходимые команды.
          </p>
          <h3>Команды для Windows:</h3>
          <ul>
            <li>создайте виртуальное окружение с помощью команды <code>python -m venv venv</code></li>
            <li>активируйте виртуальное окружение с помощью команды <code>venv\Scripts\activate</code></li>
            <li>установите пакеты с помощью команды <code>pip install -r requirements.txt</code></li>
            <li>запустите чат-бота с помощью команды <code>python main.py</code></li>
          </ul>
          <h3>Команды для Linux и macOS:</h3>
          <ul>
            <li>создайте виртуальное окружение с помощью команды <code>python3 -m venv venv</code></li>
            <li>активируйте виртуальное окружение с помощью команды <code>source venv/bin/activate</code></li>
            <li>установите пакеты с помощью команды <code>pip install -r requirements.txt</code></li>
            <li>запустите чат-бота с помощью команды <code>python3 main.py</code></li>
          </ul>
          <p>
            Если вы закрыли командную строку и хотите снова запустить чат-бота, вам понадобиться активировать виртуальное окружение в той папке, где вы его создали, но создавать его снова и скачивать пакеты больше не нужно.
          </p>
        </section>
      </div>
    </div>
  </main>
</template>

<style scoped>
.page__header {
  margin: 32px 0px 20px 0px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header__title {
  font-size: 32px;
  line-height: 40px;
}

.toc {
  margin-bottom: 24px;
}

section {
  margin-bottom: 24px;
}

h2 {
  margin-bottom: 16px;
}

h3 {
  margin-bottom: 12px;
}

p {
  margin-bottom: 12px;
  line-height: 24px;
}

ul {
	margin-bottom: 12px;
  line-height: 24px;
}

li {
  margin: 0px 0px 8px 20px;
  line-height: 24px;
}

a {
  color: var(--primary);
}

code {
  background-color: var(--light-gray);
}
</style>
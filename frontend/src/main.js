import { createApp } from 'vue'
import App from '@/App.vue'
import router from '@/router/router';
import components from '@/components/UI';
import store from '@/store/index';
import ToastPlugin from 'vue-toast-notification';
import 'vue-toast-notification/dist/theme-bootstrap.css';

const app = createApp(App)

for (const componentName in components) {
  app.component(componentName, components[componentName])
}

app
  .use(router)
  .use(store)
  .use(ToastPlugin)
  .mount('#app')

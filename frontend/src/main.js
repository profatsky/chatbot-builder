import { createApp } from 'vue'
import App from '@/App.vue'
import router from '@/router/router';
import components from '@/components/UI';
import store from '@/store/index';

const app = createApp(App)

for (const componentName in components) {
  app.component(componentName, components[componentName])
}

app
  .use(router)
  .use(store)
  .mount('#app')

import { createApp } from 'vue'
import App from '@/App.vue'
import router from '@/router/router';
import components from '@/components/UI';

const app = createApp(App)

for (const componentName in components) {
  app.component(componentName, components[componentName])
}

app
  .use(router)
  .mount('#app')

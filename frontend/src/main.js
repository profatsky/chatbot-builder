import { createApp } from 'vue'
import App from '@/App.vue'
import router from '@/router/router';
import components from '@/components/UI';

const app = createApp(App)

components.forEach(component => {
  app.component(component.name, component)
})

app
  .use(router)
  .mount('#app')

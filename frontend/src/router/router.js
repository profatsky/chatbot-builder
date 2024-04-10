import {createRouter, createWebHistory} from 'vue-router';
import Main from '@/pages/Main.vue';
import Projects from '@/pages/Projects.vue';
import Profile from '@/pages/Profile.vue';

const routes = [
  {
    path: '/',
    component: Main
  },
  {
    path: '/projects',
    component: Projects
  },
  {
    path: '/profile',
    component: Profile
  },
]

const router = createRouter({
  routes,
  history: createWebHistory()
})

export default router;
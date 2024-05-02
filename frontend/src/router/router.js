import {createRouter, createWebHistory} from 'vue-router';
import Main from '@/pages/Main.vue';
import Projects from '@/pages/Projects.vue';
import Profile from '@/pages/Profile.vue';
import Dialogue from '@/pages/Dialogue.vue';
import PersonalDataProcessingPolicy from '@/pages/PersonalDataProcessingPolicy.vue';

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
  {
    path: '/projects/:projectId/dialogues/:dialogueId',
    component: Dialogue
  },
  {
    path: '/personal-data-processing-policy',
    component: PersonalDataProcessingPolicy
  }
]

const router = createRouter({
  routes,
  history: createWebHistory()
})

export default router;
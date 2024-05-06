import {createRouter, createWebHistory} from 'vue-router';
import Main from '@/pages/Main.vue';
import PersonalDataProcessingPolicy from '@/pages/PersonalDataProcessingPolicy.vue';
import Projects from '@/pages/Projects.vue';
import Profile from '@/pages/Profile.vue';
import Dialogue from '@/pages/Dialogue.vue';
import Plugins from '@/pages/Plugins.vue';
import PluginDetail from '@/pages/PluginDetail.vue';

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
    path: '/plugins',
    component: Plugins
  },
  {
    path: '/plugins/:pluginId',
    component: PluginDetail
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
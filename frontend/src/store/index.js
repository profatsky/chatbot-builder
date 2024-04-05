import { createStore } from 'vuex';
import authModule from './authModule';

export default createStore({
  modules: {
    auth: authModule,
  }
})
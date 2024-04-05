const state = {
  isAuth: false,
};

const mutations = {
  setAuth(state, { isAuth }) {
    state.isAuth = isAuth;
  }
};

const actions = {
  login({ commit }) {
    commit('setAuth', { isAuth: true});
  },
  logout({ commit }) {
    commit('setAuth', { isAuth: false})
  }
};

const getters = {
  isAuth: state => state.isAuth
};

export default {
  state,
  getters,
  actions,
  mutations
}
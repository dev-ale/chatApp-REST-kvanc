import Vue from 'vue'
import Vuex from 'vuex'
import VuexPersist from 'vuex-persist'

Vue.use(Vuex)

const vuexPersist = new VuexPersist({
  key: 'chat-app',
  storage: window.localStorage
})

export default new Vuex.Store({

  state: {
    loggedIn: false,
    userName: '',

  },
  mutations: {
    setLoggedInStatus (state, payload){
      state.loggedIn = payload
    },
    setUserName (state, payload){
      state.userName = payload
      localStorage.setItem('chat-app',{loggedIn: false, userName: payload})
    },
  },
  actions: {
  },
  modules: {
  },
  getters: {
    getLoggedInStatus (state){
      return state.loggedIn
    },
    getUserName (state){
      return state.userName
    },
  },
  plugins: [vuexPersist.plugin]
})

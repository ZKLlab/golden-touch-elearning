import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    userInfo: null
  },
  mutations: {
    UPDATE_USER_INFO(state, user_info) {
      state.userInfo = user_info
    }
  },
  actions: {
    updateUserInfo(context) {
      context.commit('UPDATE_USER_INFO', null)
      axios.get('/info').then((response) => {
        context.commit('UPDATE_USER_INFO', response.data)
      })
    }
  },
})

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
      axios.get('/api/info').then((response) => {
        context.commit('UPDATE_USER_INFO', response.data)
      }).catch((error) => {
        if (error.response.status === 401 || error.response.status === 403) {
          context.commit('UPDATE_USER_INFO', null)
        }
      })
    }
  },
})

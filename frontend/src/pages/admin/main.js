import Vue from 'vue'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'
import '../../plugins/element'

import App from './App'
import axios from './http'
import store from '../../store'
import router from './router'

Vue.config.productionTip = false
// noinspection JSUnusedGlobalSymbols
Vue.prototype.$axios = axios

router.beforeEach((to, from, next) => {
  NProgress.start()
  if (store.state.userInfo === null) {
    const loading = Vue.prototype.$loading({
      lock: true,
    })
    const unwatch = store.watch((state) => state.userInfo, () => {
      loading.close()
      if (store.state.userInfo['is_logged_in'] === true && store.state.userInfo['is_volunteer']) {
        next()
      } else {
        next()
        // window.location.href = '/'
      }
      unwatch()
    })
  } else {
    if (store.state.userInfo['is_logged_in'] === true && store.state.userInfo['is_volunteer']) {
      next()
    } else {
      next(false)
      // window.location.href = '/'
    }
  }
})

router.afterEach(() => {
  NProgress.done()
})

// noinspection JSUnusedGlobalSymbols
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

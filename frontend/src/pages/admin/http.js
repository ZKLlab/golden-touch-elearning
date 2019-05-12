import axios from 'axios'
import Cookies from 'js-cookie'

axios.interceptors.request.use(function (config) {
  return new Promise((resolve) => {
    if (config.method !== 'get') {
      if (!Cookies.get('csrftoken')) {
        axios.get('/api/csrf_token').then(() => {
          config.headers['X-CSRFToken'] = Cookies.get('csrftoken')
          resolve(config)
        }).catch(() => {
          resolve(config)
        })
      } else {
        config.headers['X-CSRFToken'] = Cookies.get('csrftoken')
        resolve(config)
      }
    } else {
      resolve(config)
    }
  })
}, function (error) {
  return Promise.reject(error)
})

export default axios
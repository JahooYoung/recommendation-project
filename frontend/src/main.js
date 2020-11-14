import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import i18n from './plugins/i18n'
import './plugins/axios.js'
import UserStatus from './plugins/userStatus.js'

import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)

Vue.use(UserStatus)

Vue.config.productionTip = false

window.appRoot = new Vue({
  router,
  store,
  i18n,
  render: h => h(App)
}).$mount('#app')

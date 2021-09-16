import '@babel/polyfill'
import 'mutationobserver-shim'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faChevronCircleRight, faSearch } from '@fortawesome/free-solid-svg-icons'
import { faCalendarAlt } from '@fortawesome/free-regular-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

import Vue from 'vue'

import './plugins/bootstrap-vue'
import router from './router'
import store from './store'
import App from './App.vue'

Vue.component('font-awesome-icon', FontAwesomeIcon)
library.add(faChevronCircleRight, faSearch)
library.add(faCalendarAlt)

Vue.config.productionTip = false


new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

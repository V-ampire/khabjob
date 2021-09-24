import Vue from 'vue'
import Vuex from 'vuex'

import vacancies from '@/store/vacancies.js'
import auth from '@/store/auth.js'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    vacancies,
    auth,
  }
})

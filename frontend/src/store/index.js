import Vue from 'vue'
import Vuex from 'vuex'

import vacancies from '@/store/vacancies.js'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    vacancies,
  }
})

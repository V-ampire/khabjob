import Vue from 'vue'
import VueRouter from 'vue-router'

import VacancyList from '@/views/public/VacancyList.vue'

import config from '@/config'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'PublicVacancyList',
    component: VacancyList
  },
  {
    path: '/vacancies/:vacancyId',
    name: 'PublicVacancyDetail',
    component: VacancyList
  },
]

const router = new VueRouter({
  mode: 'history',
  base: config.baseUrl,
  routes
})

export default router

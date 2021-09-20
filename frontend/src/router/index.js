import Vue from 'vue'
import VueRouter from 'vue-router'

import VacancyList from '@/views/public/VacancyList.vue'
import VacancyDetail from '@/views/public/VacancyDetail.vue'
import VacancySearch from '@/views/public/VacancySearch.vue'

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
    component: VacancyDetail
  },
  {
    path: '/search',
    name: 'PublicVacancySearch',
    component: VacancySearch
  },
]

const router = new VueRouter({
  mode: 'history',
  base: config.baseUrl,
  routes
})

export default router

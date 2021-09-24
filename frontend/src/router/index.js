import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '@/store'

import VacancyList from '@/views/public/VacancyList.vue'
import VacancyDetail from '@/views/public/VacancyDetail.vue'
import VacancySearch from '@/views/public/VacancySearch.vue'
import AdminVacancyDetail from '@/views/admin/VacancyDetail.vue'

import Login from '@/views/admin/Login.vue'
import Dashboard from '@/views/admin/Dashboard.vue'

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
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/admin',
    name: 'Dashboard',
    component: Dashboard,
    meta: {
      requiresAuth: true
    },
  },
  {
    path: '/admin/vacancies/:vacancyId',
    name: 'AdminVacancyDetail',
    component: AdminVacancyDetail,
    meta: {
      requiresAuth: true
    },
  },
]


const router = new VueRouter({
  mode: 'history',
  base: config.baseUrl,
  routes
})


router.beforeEach((to, from, next) => {
  if(to.matched.some(record => record.meta.requiresAuth)) {

    let isAuthenticated = store.getters['auth/isAuthenticated']

    if (isAuthenticated) {
      next()
      return
    }
    next({name: 'Login'})
  } else {
    next()
  }
})


export default router

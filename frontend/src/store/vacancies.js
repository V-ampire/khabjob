import { publicVacanciesApi, privateVacanciesApi, searchVacanciesApi } from '@/http/clients'
import { ResponseFormatError } from '@/http/errors'


export default {
  namespaced: true,
  state: () => ({
    vacancyList: [],
    vacancy: null,
    count: null,
    searchParams: {
      date_from: null,
      date_to: null,
      search_query: null
    },
  }),

  mutations: {
    SET_VACANCIES(state, vacancies) {
      state.vacancyList = vacancies
    },
    SET_COUNT(state, count) {
      state.count = count
    },
    SET_VACANCY(state, vacancyData) {
      state.vacancy = vacancyData
    },
    CLEAR_VACANCY(state) {
      state.vacancy = null
    },
    SET_SEARCH_PARAMS(state, params) {
      Object.assign(state.searchParams, params)
    }
  },
  
  actions: {
    async GET_VACANCIES({ commit, rootState }, { params, fromPrivate }) {
      /**
       * Load vacancyList using API search.
       * @params - Query string params
       * @fromPrivate - If true, make requests to private API.
       */
      const api = (fromPrivate) ? privateVacanciesApi(rootState.auth.token) : publicVacanciesApi()

      let response = await api.list(params)
      if (response.data.results) {
        commit('SET_VACANCIES', response.data.results)
        commit('SET_COUNT', response.data.count)
      }
      else {
        throw ResponseFormatError()
      }
    },
    async GET_VACANCY({ commit, rootState }, { vacancyId, fromPrivate }) {
      /**
       * Load vacancy info using detail endpoint
       */
      const api = (fromPrivate) ? privateVacanciesApi(rootState.auth.token) : publicVacanciesApi()

      const response = await api.detail(vacancyId)

      commit('SET_VACANCY', response.data)
    },
    async SEARCH_VACANCIES({ state, commit, rootState }, params) {
      const requestParams = state.searchParams
      if (params) {
        Object.assign(requestParams, params)
      }
      const response = await searchVacanciesApi(rootState.auth.token).search(requestParams)
      if (response.data.results) {
        commit('SET_VACANCIES', response.data.results)
        commit('SET_COUNT', response.data.count)
      }
      else {
        throw ResponseFormatError()
      }
    },
    async CREATE_VACANCY({ rootState }, createData) {
      const response = await privateVacanciesApi(rootState.auth.token).create(createData)
      return response.data
    },
    async UPDATE_VACANCY({ commit, rootState }, { vacancyId, updateData }) {
      const response = await privateVacanciesApi(rootState.auth.token).update(vacancyId, updateData)

      commit('SET_VACANCY', response.data)
    },
    async DELETE_VACANCIES({ rootState }, deleteIds) {
      const params = new URLSearchParams(deleteIds.map(s => ['id', s]))
      const response = await privateVacanciesApi(rootState.auth.token).delete_batch(params)
      return response.data
    },
    async DELETE_VACANCY({ rootState }, vacancyId) {
      const response = await privateVacanciesApi(rootState.auth.token).delete(vacancyId)
      return response.data
    }
  }
}
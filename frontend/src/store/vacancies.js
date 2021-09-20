import { publicVacanciesApi, searchVacanciesApi } from '@/http/clients'
import { ResponseFormatError } from '@/http/errors'

const api = publicVacanciesApi()
const searchApi = searchVacanciesApi()

export default {
  namespaced: true,
  state: () => ({
    vacancyList: [],
    vacancy: null,
    totalCount: null,
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
    SET_TOTAL_COUNT(state, count) {
      state.totalCount = count
    },
    SET_VACANCY(state, vacancyData) {
      state.vacancy = vacancyData
    },
    SET_SEARCH_PARAMS(state, params) {
      Object.assign(state.searchParams, params)
    }
  },
  
  actions: {
    async GET_VACANCIES({ commit }, params) {
      /**
       * Load vacancyList using API search.
       */
      let response = await api.list(params)
      if (response.data.results) {
        commit('SET_VACANCIES', response.data.results)
        commit('SET_TOTAL_COUNT', response.data.count)
      }
      else {
        throw ResponseFormatError()
      }
    },
    async GET_VACANCY({ commit }, vacancyId) {
      /**
       * Load vacancy info using detail endpoint
       */
      const response = await api.detail(vacancyId)

      commit('SET_VACANCY', response.data);
    },
    async SEARCH_VACANCIES({ state, commit }, params=null) {
      const requestParams = state.searchParams
      if (params) {
        Object.assign(requestParams, params)
      }
      const response = await searchApi.search(requestParams)
      if (response.data.results) {
        commit('SET_VACANCIES', response.data.results)
        commit('SET_TOTAL_COUNT', response.data.count)
      }
      else {
        throw ResponseFormatError()
      }
    },
  }
}
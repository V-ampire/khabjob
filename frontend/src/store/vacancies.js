import { publicVacanciesApi } from '@/http/clients'

const api = publicVacanciesApi()

export default {
  namespaced: true,
  state: () => ({
    vacancyList: [],
    vacancy: null,
    totalCount: null,
    searchOptions: {
      date_from: null,
      date_to: null,
      search_query: null
    },
  }),

  mutations: {
    SET_SEARCH_OPTS(state, options) {
      Object.assign(state.searchOptions, options)
    },
    SET_VACANCIES(state, vacancies) {
      state.vacancyList = vacancies
    },
    SET_TOTAL_COUNT(state, count) {
      state.totalCount = count
    },
  },
  
  actions: {
    async SEARCH_VACANCIES({ commit, state }, params) {
      let requestParams = {...state.searchOptions, ...params};
      
      let response = await api.list(requestParams)
      
      commit('SET_VACANCIES', response.data.results);
      commit('SET_TOTAL_COUNT', response.data.count);
    },
    // async FILTER_VACANCIES({ commit }) {

    // }
  }
}
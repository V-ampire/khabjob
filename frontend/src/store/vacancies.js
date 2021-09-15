import { publicVacanciesApi } from '@/http/clients'

const api = publicVacanciesApi()

export default {
  state: () => ({
    vacancies: [],
    vacancy: null,
    totalCount: null,
  }),
  actions: {
    async GET_VACANCIES({ commit }) {

    }
  }
}
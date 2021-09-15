<template>
  <div class="vacancies">
    <b-container fluid>
      <b-row>
        <b-col class="mb-3" cols="12">
          <VacanciesSearch />
        </b-col>
      </b-row>
      <b-row class="mb-3">
        <b-col cols="12">
          <div class="errors" v-if="errorState">{{ errorMessage }}</div>
          <div class="loading d-flex justify-content-center" v-else-if="loadingState">
            <b-spinner class="spinner" variant="primary" type="grow" label="Loading..."></b-spinner>
          </div>
          <b-list-group flush v-else>
            <b-list-group-item v-for="vacancy in vacancies" :key="vacancy.id">
              <VacancyItem :vacancyData="vacancy"/>
            </b-list-group-item>
          </b-list-group>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12">
          <Pagination 
            :count="pagination.count"
            :perPage="pagination.limit"
            v-on:onPaginate="paginate"
          />
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import { publicVacanciesApi } from '@/http/clients'
import VacancyItem from '@/components/vacancies/VacancyItem.vue'
import VacanciesSearch from '@/components/vacancies/VacanciesSearch.vue'
import Pagination from '@/components/common/Pagination.vue'
import { ON_SEARCH } from '@/events/types'
import eventBus from '@/events/eventBus'

export default {
  components: {
    VacancyItem,
    Pagination,
    VacanciesSearch
  },
  data() {
    return {
      loadingState: true,
      errorState: false,
      errorMessage: '',
      pagination: {
        count: null,
        limit: 10,
        offset: 0,
      },
    }
  },
  computed: {
    api() {
      return publicVacanciesApi()
    },
    isPaginated() {
      return !!this.pagination.count && this.pagination.count > this.pagination.limit
    }
  },
  async mounted () {
    eventBus.$on(ON_SEARCH, this.search)
    const vacanciesParams = {
      date_from: this.getTodayDate(),
      date_to: this.getTodayDate(),
    }
    await this.loadVacanciesData(vacanciesParams)
  },
  methods: {
    getTodayDate() {
      const today = new Date()
      return today.toISOString().split("T")[0]
    },
    async getVacancies(params) {
      let response;
      try {
        response = await this.api.list(params);
      } catch (err) {
        const message = 'Не удалось загрузить список вакансий. ' +
                        'Проверьте соединение с интернетом или повторите попытку позже...'
        this.showErrorMessage(message)
        throw err
      }
      return response.data
    },
    showErrorMessage(message) {
      this.errorState = true
      this.errorMessage = message
    },
    async loadVacanciesData(params={}) {
      this.loadingState = true

      const requestParams = {
        limit: this.pagination.limit,
        offset: this.pagination.offset
      }
        
      Object.assign(requestParams, params)

      console.log(requestParams)

      const paginatedData = await this.getVacancies(requestParams)
      this.vacancies = paginatedData.results
      this.pagination.count = paginatedData.count

      this.loadingState = false
    },
    async paginate(page) {
      this.pagination.offset = (page - 1) * this.pagination.limit
      await this.loadVacanciesData()
    },
    async search(params) {
      console.log(params)
      await this.loadVacanciesData(params)
    }
  }
}
</script>

<style>
  .loading {
    margin-top: 40vh;
  }
  .spinner {
    width: 10vh;
    height: 10vh;
  }
</style>
<template>
  <div class="wrapper h-100 d-flex flex-column justify-content-between">
    <div class="vacancies">
      <b-container fluid class="justify-content-between">
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
              <b-list-group-item v-for="vacancy in vacancyList" :key="vacancy.id">
                <VacancyItem :vacancyData="vacancy"/>
              </b-list-group-item>
            </b-list-group>
          </b-col>
        </b-row>
      </b-container>
    </div>
    <div class="pagination mx-auto" v-if="isPaginated">
      <Pagination
        :count="totalCount"
        :perPage="limit"
        v-on:onPaginate="paginate"
      />
    </div>
  </div>
</template>

<script>
import { mapGetters, mapState } from 'vuex';
import { mapMutations, mapActions } from 'vuex';
import VacancyItem from '@/components/vacancies/VacancyItem.vue'
import VacanciesSearch from '@/components/vacancies/VacanciesSearch.vue'
import Pagination from '@/components/common/Pagination.vue'
import { ON_SEARCH_VACANCIES } from '@/events/types'
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
      limit: 40,
      offset: 0,
    }
  },
  computed: {
    ...mapState('vacancies', [
      'totalCount',
      'vacancyList',
    ]),
    ...mapGetters('vacancies', [
      'isPaginated',
    ]),
    isPaginated() {
      return !!this.totalCount && this.totalCount > this.limit
    }
  },
  async mounted() {
    eventBus.$on(ON_SEARCH_VACANCIES, this.searchVacancies)
    const initialSearchOpts = {
      date_from: this.getTodayDate(),
      date_to: this.getTodayDate(),
      search_query: null
    }
    this.SET_SEARCH_OPTS(initialSearchOpts)
    await this.searchVacancies()
  },
  methods: {
    ...mapActions('vacancies', [
      'SEARCH_VACANCIES'
    ]),
    ...mapMutations('vacancies', [
      'SET_SEARCH_OPTS',
      'SET_PAGINATION',
    ]),
    getTodayDate() {
      const today = new Date()
      return today.toISOString().split("T")[0]
    },
    showErrorMessage(message) {
      this.errorState = true
      this.errorMessage = message
    },
    async searchVacancies() {
      this.loadingState = true
      const params = {
        limit: this.limit,
        offset: this.offset
      }
      try {
        await this.SEARCH_VACANCIES(params);
      } catch (err) {
        const message = 'Не удалось загрузить список вакансий. ' +
                        'Проверьте соединение с интернетом или повторите попытку позже...'
        this.showErrorMessage(message)
        throw err
      } finally {
        this.loadingState = false
        console.log(this.totalCount)
      }
    },
    async paginate(page) {
      this.offset = this.limit * (page - 1)
      await this.searchVacancies()
    }
  }
}
</script>

<style>
  .loading {
    margin-top: 20vh;
  }
  .spinner {
    width: 10vh;
    height: 10vh;
  }
</style>
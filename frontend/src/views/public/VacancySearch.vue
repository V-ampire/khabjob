<template>
  <div class="wrapper h-100 d-flex flex-column justify-content-between">
    <div class="vacancies">
      <b-container fluid="xl" class="justify-content-between">
        <b-row>
          <b-col cols="12">
            <div class="vacancies-search-data mb-3">
              <div class="vacancies-search-data-query mr-2" v-if="searchParams.search_query">
                Вакансии по запросу <strong>{{ searchParams.search_query }}</strong>
              </div>
              <span class="mr-1" v-if="searchParams.date_from">
                от <strong>{{ dateFromLocal }}</strong>
              </span>
              <span v-if="searchParams.date_to">
                до <strong>{{ dateToLocal }}</strong>
              </span>
              <div class="vacancies-search-incorrect" v-if="!vacancyList.length">
                <p>
                  Некорректный поисковой запрос, пожалуйста проверьте данные.
                </p>
                <p>
                  Вы можете вернуться на <router-link to="/"><span class="text-underline">главную</span></router-link>
                  или продолжить поиск.
                </p>
              </div>
            </div>
          </b-col>
        </b-row>
        <b-row v-if="vacancyList.length">
          <b-col cols="12">
            Найдено вакансий: {{ count }}
          </b-col>
        </b-row>
        <b-row class="mb-3">
          <b-col cols="12">
            <VacancyItems :vacancyList="vacancyList" />
          </b-col>
        </b-row>
      </b-container>
    </div>
    <div class="pagination mx-auto" v-if="isPaginated">
      <Pagination
        :count="count"
        :perPage="limit"
        v-on:onPaginate="fetch"
      />
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import VacancyItems from '@/components/vacancies/VacancyItems.vue'
import Pagination from '@/components/common/Pagination.vue'

export default {
  components: {
    VacancyItems,
    Pagination,
  },
  data() {
    return {
      limit: 40,
      offset: 0,
    }
  },
  computed: {
    ...mapState('vacancies', [
      'count',
      'vacancyList',
      'searchParams',
    ]),
    isPaginated() {
      return !!this.count && this.count > this.limit
    },
    dateFromLocal() {
      return new Date(this.searchParams.date_from).toLocaleDateString()
    },
    dateToLocal() {
      return new Date(this.searchParams.date_to).toLocaleDateString()
    }
  },
  async mounted() {
    await this.fetch()
  },
  methods: {
    ...mapActions('vacancies', [
      'SEARCH_VACANCIES',
    ]),
    async fetch(page=1) {
      this.offset = this.limit * (page - 1)
      await this.SEARCH_VACANCIES({
        limit: this.limit,
        offset: this.offset
      })
      window.scrollTo(0,0);
    }
  }
}
</script>
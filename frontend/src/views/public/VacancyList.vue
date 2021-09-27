<template>
  <div class="wrapper h-100 d-flex flex-column justify-content-between">
    <div class="vacancies">
      <b-container fluid="xl" class="justify-content-between">
        <b-row>
          <b-col class="mb-2" cols="12">
            <div class="vacancies-search d-flex flex-column flex-sm-row">
              <b-form ref="form">
                <div class="vacancyDate-field mb-2">
                  <span class="mr-2">
                    Вакансии на <strong class="current-date-text">{{ currentDateStr }} г.</strong>
                  </span>
                  <span class="vacancyDate-field-value">
                    <b-form-datepicker
                      v-model="vacanciesDate"
                      button-only
                      button-variant="dateBtn"
                      right
                      value-as-date
                    >
                      <template v-slot:button-content>
                        <font-awesome-icon :icon="['far', 'calendar-alt']" />
                      </template>
                    </b-form-datepicker>
                  </span>
                </div>
              </b-form>
            </div>
          </b-col>
        </b-row>
        <b-row>
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
import { convertToISODateString } from '@/utils.js'

export default {
  components: {
    VacancyItems,
    Pagination,
  },
  data() {
    return {
      limit: 40,
      offset: 0,
      vacanciesDate: new Date(),
    }
  },
  computed: {
    ...mapState('vacancies', [
      'count',
      'vacancyList',
    ]),
    isPaginated() {
      return !!this.count && this.count > this.limit
    },
    currentDateStr() {
      return this.vacanciesDate.toLocaleDateString()
    },
  },
  watch: {
    vacanciesDate: async function() {
      await this.fetch()
    }
  },
  async mounted() {
    await this.fetch()
  },
  methods: {
    ...mapActions('vacancies', [
      'GET_VACANCIES',
    ]),
    async fetch(page=1) {
      this.offset = this.limit * (page - 1)
      await this.GET_VACANCIES({
        params: {
          modified_at: convertToISODateString(this.vacanciesDate),
          limit: this.limit,
          offset: this.offset
        }
      })
      window.scrollTo(0,0)
    }
  }
}
</script>
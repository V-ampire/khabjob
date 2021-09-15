<template>
  <b-modal :title="title" ref="modal" hide-footer>
    <b-form ref="form">
      <div class="searchBar-dates mb-2">
        <h5>Поиск по датам:</h5>
        <div class="searchBar-dates-inputs">
          <div class="searchBar-dates-dateFrom mb-2">
            <b-form-datepicker
              v-model="dateFrom"
              button-variant="dateBtn"
              right
              value-as-date
            >
              <template v-slot:button-content>
                <font-awesome-icon :icon="['far', 'calendar-alt']" />
              </template>
            </b-form-datepicker>
          </div>
          <div class="searchBar-dates-dateTo">
            <b-form-datepicker
              v-model="dateTo"
              button-variant="dateBtn"
              right
              value-as-date
            >
              <template v-slot:button-content>
                <font-awesome-icon :icon="['far', 'calendar-alt']" />
              </template>
            </b-form-datepicker>
          </div>
        </div>
      </div>
      <div class="searchBar-query mb-3">
        <h5>Поиск по названию вакансии:</h5>
        <div class="searchbar-query-input">
          <b-form-input
            class="py-0"
            v-model="searchQuery" 
            placeholder="Фраза для поиска..."
            trim
          ></b-form-input>
        </div>
      </div>
      <div class="searchBar-btn">
        <b-button 
          variant="primary" 
          block
          @click="search"
        >Искать</b-button>
      </div>
    </b-form>
  </b-modal>
</template>

<script>
import eventBus from '@/events/eventBus'
import { ON_SEARCH } from '@/events/types'
import { convertToISODateString } from '@/utils.js'

export default {
  props: {
    title: {
      type: String,
      default: 'Расширенный поиск'
    }
  },
  data() {
    return {
      dateFrom: null,
      dateTo: null,
      searchQuery: ''
    }
  },
  computed: {
    searchOptions() {
      const search = {}
      if (this.dateFrom) {
        search.date_from = convertToISODateString(this.dateFrom)
      }
      if (this.dateTo) {
        search.date_to = convertToISODateString(this.dateTo)
      }
      if (this.searchQuery) {
        search.search_query = this.searchQuery
      }
      return search
    }
  },
  methods: {
    open() {
      this.$refs.modal.show()
    },
    search() {
      eventBus.$emit(ON_SEARCH, this.searchOptions)
      this.$refs.modal.hide()
    }
  },
}
</script>
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
import { mapMutations } from 'vuex';
import { convertToISODateString } from '@/utils.js'
import { ON_SEARCH_VACANCIES } from '@/events/types'
import eventBus from '@/events/eventBus'

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
  methods: {
    ...mapMutations('vacancies', [
      'SET_SEARCH_OPTS',
    ]),
    open() {
      this.$refs.modal.show()
    },
    search() {
      // Мутировать store.searchOptions
      this.SET_SEARCH_OPTS({
        date_from: (this.dateFrom) ? convertToISODateString(this.dateFrom) : null,
        date_to: (this.dateTo) ? convertToISODateString(this.dateTo) : null,
        search_query: (this.searchQuery) ? this.searchQuery : null
      })
      // Вызвать событие поиска вакансий
      eventBus.$emit(ON_SEARCH_VACANCIES)
      this.$refs.modal.hide()
    }
  },
}
</script>
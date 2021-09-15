<template>
  <div class="vacancies-search d-flex flex-column flex-sm-row">
    <b-form ref="form">
      <div class="vacancyDate-field mb-2">
        <span class="mr-2">
          Вакансии на <strong class="current-date-text">{{ currentDateStr }} г.</strong>
        </span>
        <span class="vacancyDate-field-value">
          <b-form-datepicker
            v-model="vacancyDate"
            v-on:input="search"
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
      <div class="searchQuery-field d-flex">
        <div class="searchQuery-field-input mr-2">
          <b-form-input
            class="py-0"
            v-model="searchQuery" 
            placeholder="Поиск по должности"
            trim
          ></b-form-input>
        </div>
        <div class="searchQuery-field-btn">
          <b-button 
            variant="primary" 
            class="py-1 px-2"
            v-on:click="search"
          >
            <font-awesome-icon icon="search" />
          </b-button>
        </div>
      </div>
    </b-form>
  </div>
</template>

<script>
import { ON_CHANGE } from '@/events/types'
import eventBus from '@/events/eventBus'
import { convertToISODateString } from '@/utils.js'

export default {
  data() {
    return {
      vacancyDate: new Date(),
      searchQuery: ''
    }
  },
  computed: {
    currentDateStr() {
      return this.vacancyDate.toLocaleDateString()
    },
  },
  methods: {
    search() {
      const searchOptions = {
        date_from: convertToISODateString(this.vacancyDate),
        date_to: convertToISODateString(this.vacancyDate),
      }
      if (this.searchQuery) {
        Object.assign(searchOptions, {search_query: this.searchQuery})
      }
      eventBus.$emit(ON_SEARCH, searchOptions)
    }
  },
}
</script>
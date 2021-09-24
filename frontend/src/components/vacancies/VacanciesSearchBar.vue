<template>
  <b-modal :title="title" ref="modal" hide-footer>
    <b-form ref="form" v-on:submit.prevent="search">
      <div class="searchBar-dates mb-2">
        <h5>Поиск по датам:</h5>
        <div class="searchBar-dates-inputs">
          <div class="searchBar-dates-dateFrom mb-2">
            <b-form-datepicker
              v-model="date_from"
              label-no-date-selected="Опубликованные после"
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
              v-model="date_to"
              label-no-date-selected="Опубликованные до"
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
            v-model="search_query" 
            placeholder="Фраза для поиска..."
            trim
          ></b-form-input>
        </div>
      </div>
      <div class="searchBar-status mb-3" v-if="isAuthenticated">
        <b-form-checkbox
          id="checkbox-1"
          v-model="published_only"
          name="checkbox-1"
        >
          Показывать только опубликованные вакансии
        </b-form-checkbox>
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
import { convertToISODateString } from '@/utils.js'
import { mapMutations, mapGetters, mapActions } from 'vuex';

export default {
  props: {
    title: {
      type: String,
      default: 'Расширенный поиск'
    }
  },
  data() {
    return {
      date_from: null,
      date_to: null,
      search_query: null,
      published_only: true,
      limit: 20,
    }
  },
  computed: {
    ...mapGetters('auth', [
      'isAuthenticated'
    ]),
  },
  methods: {
    ...mapMutations('vacancies', [
      'SET_SEARCH_PARAMS',
    ]),
    ...mapActions('vacancies', [
      'SEARCH_VACANCIES',
    ]),
    open() {
      this.$refs.modal.show()
    },
    search() {
      this.SET_SEARCH_PARAMS({
        date_from: (this.date_from) ? convertToISODateString(this.date_from) : null,
        date_to: (this.date_to) ? convertToISODateString(this.date_to) : null,
        search_query: this.search_query,
        published_only: this.published_only,
      })
      // Go to search page
      this.$router.push({ name: 'PublicVacancySearch' }).catch( async (error) => {
        if (error.name !== 'NavigationDuplicated') {
          throw error
        }
        // We are already on search page
        await this.SEARCH_VACANCIES({
          limit: this.limit
        })
      })
    this.$refs.modal.hide()
    }
  },
}
</script>
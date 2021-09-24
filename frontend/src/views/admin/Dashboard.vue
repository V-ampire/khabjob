<template>
  <div class="dashboard">
    <b-modal 
      class="dashboard-create-modal" 
      id="createVacancyModal" 
      title="Добавить вакансию"
      v-on:ok="create"
    >
      <div class="create-form">
        <VacancyForm ref="createVacancyForm" />
      </div>
      <div class="create-result" v-if="createdVacancy">
        Вакансия 
        <router-link :to="{ name: 'AdminVacancyDetail', params: { vacancyId: createdVacancy.id }}">
          {{ createdVacancy.name }}
        </router-link> 
        добавлена.
      </div>
    </b-modal>
    <b-container fluid>
      <b-row class="mb-3">
        <b-col cols="12">
          <h3>Фильтр вакансий</h3>
          <VacanciesFilterBar ref="filterBar" />
        </b-col>
      </b-row>
      <b-row class="mb-3">
        <b-col cols="12">
          <div class="dashboard-controls d-flex">
            <b-button @click="fetch()" variant="primary" class="mr-2">Применить фильтры</b-button>
            <b-button v-b-modal.createVacancyModal variant="primary" class="mr-2">Добавить вакансию</b-button>
            <b-button @click="remove()" variant="danger">Удалить выбранные</b-button>
          </div>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12">
          <h3>Список вакансий</h3>
          <div class="dashboard-vacancies">
            <VacancyTable ref="vacancyTable" v-on:onPaginate="fetch" :perPage="limit" />
          </div>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import { showErrorAlert, showSuccessEvent, onConfirmAction } from '@/events/utils.js'
import { ServerError } from '@/http/errors.js'
import VacancyTable from '@/components/vacancies/VacancyTable'
import VacanciesFilterBar from '@/components/vacancies/VacanciesFilterBar'
import VacancyForm from '@/components/vacancies/VacancyForm'

export default {
  components: {
    VacancyTable,
    VacanciesFilterBar,
    VacancyForm,
  },
  data() {
    return {
      limit: 20,
      offset: 0,
      createdVacancy: null
    }
  },
  computed: {
    ...mapState('vacancies', [
      'searchParams',
    ]),
  },
  async mounted() {
    await this.fetch()
  },
  methods: {
    ...mapActions('vacancies', [
      'GET_VACANCIES',
      'CREATE_VACANCY',
      'DELETE_VACANCIES',
    ]),
    async fetch(page=1) {
      const params = this.$refs.filterBar.getAsObject()
      this.offset = this.limit * (page - 1)

      const filterParams = {
        limit: this.limit,
        offset: this.offset,
        ...params
      }
      try {
        await this.GET_VACANCIES({
          params: filterParams,
          fromPrivate: true
        })
        window.scrollTo(0,0)
      } catch (error) {
        showErrorAlert(error.message)
        throw error
      }
    },
    async remove() {
      const selectedIds = this.$refs.vacancyTable.getSelectedIds()
      const confirmMessage = `Удалить выбранные вакансии (${selectedIds.length} шт.)?`
      onConfirmAction({message: confirmMessage}, async (confirm) => {
        if (confirm) {
          try {
            const response = await this.DELETE_VACANCIES(selectedIds)
            showSuccessEvent(`Удалено ${response.delete} вакансий`)
          } catch (error) {
            showErrorAlert(error.message)
            throw error
          }
          await this.fetch()
          this.$refs.vacancyTable.clearSelected()
        }
      })
    },
    async create() {
      if (this.$refs.createVacancyForm.validate()) {
        const createData = this.$refs.createVacancyForm.getAsFormData()
        try {
          const vacancy = await this.CREATE_VACANCY(createData)
          this.createdVacancy = vacancy
        } catch (error) {
          if (error instanceof ServerError && error.status === 400) {
            for (let field in error.data) {
              this.$refs.createVacancyForm.setError(field, error.data[field])
            }
          }
          else {
            showErrorAlert(error.message)
            throw error
          }
        }
      }
    }
  }
}
</script>
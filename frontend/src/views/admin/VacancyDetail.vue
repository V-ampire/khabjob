<template>
  <div class="vacancy-detail">
    <b-container fluid>
      <div class="vacancy-detail-form mb-3">
        <VacancyForm ref="updateVacancyForm" />
      </div>
      <div class="vacancy-detail-controls d-flex">
        <b-button @click="update()" variant="primary" class="mr-2">Применить изменения</b-button>
        <b-button @click="remove()" variant="danger">Удалить</b-button>
      </div>
    </b-container>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import { ServerError } from '@/http/errors.js'
import { showErrorAlert, showSuccessEvent, onConfirmAction } from '@/events/utils.js'
import VacancyForm from '@/components/vacancies/VacancyForm'

export default {
  components: {
    VacancyForm,
  },
  async mounted() {
    await this.GET_VACANCY({ vacancyId: this.vacancyId, fromPrivate: true })
    this.$refs.updateVacancyForm.setInitial(this.vacancy)
  },
  computed: {
    vacancyId() {
      return this.$route.params.vacancyId;
    },
    ...mapState('vacancies', [
      'vacancy',
    ]),
    vacancyFormData() {
      return this.$refs.updateVacancyForm.getAsFormData()
    }
  },
  methods: {
    ...mapActions('vacancies', [
      'GET_VACANCY',
      'UPDATE_VACANCY',
      'DELETE_VACANCY',
    ]),
    async update() {
      try {
        await this.UPDATE_VACANCY({
          vacancyId: this.vacancy.id,
          updateData: this.vacancyFormData
        })
        showSuccessEvent(`Вакансия ${this.vacancy.name} обновлена!`)
      } catch (error) {
        if (error instanceof ServerError) {
          if (error.status === 400) {
            for (let field in error.data) {
              this.$refs.updateVacancyForm.setError(field, error.data[field])
            }
          }
        }
        showErrorAlert(error.message)
        throw error
      }
    },
    async remove() {
      const confirmMessage = `Удалить вакансию ${this.vacancy.name}?`
      onConfirmAction({message: confirmMessage}, async (confirm) => {
        if (confirm) {
          try {
            await this.DELETE_VACANCY(this.vacancy.id)
            showSuccessEvent(`Вакансия ${this.vacancy.name} удалена!`)
          } catch (error) {
            showErrorAlert(error.message)
            throw error
          }
          this.$router.push({ name: 'Dashboard' })
        }
      })
    }
  }
}
</script>
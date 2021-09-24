<template>
  <div class="vacancy-detail">
    <b-container fluid>
      <b-row>
        <b-col sm="6">
          <div class="vacancy-detail-info">
            <h2 class="vacancy-detail-name d-block mb-2">{{ vacancy.name }}</h2>
            <div class="vacancy-detail-description mb-4">
              {{ vacancy.description }}
            </div>
          </div>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>


<script>
import { mapState, mapActions } from 'vuex'

export default {
  async mounted() {
    await this.GET_VACANCY({ vacancyId: this.vacancyId })
  },
  computed: {
    vacancyId() {
      return this.$route.params.vacancyId;
    },
    ...mapState('vacancies', [
      'vacancy',
    ]),
  },
  methods: {
    ...mapActions('vacancies', [
      'GET_VACANCY'
    ]),
  },
}
</script>
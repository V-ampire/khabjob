<template>
  <div>
    <div class="vacancy-source p-1">
      <b-badge class="mr-1" pill :variant="vacancyData.source_name">{{ vacancyData.source_name }}</b-badge>
      <b-badge pill variant="light">{{ localeModifiedAt }}</b-badge>
    </div>
      <a v-if="vacancyData.source" :href="vacancyData.source" target="_blank">
        <div class="vacancy-name p-1 d-flex justify-content-between">
          <span class="mr-1">{{ vacancyData.name }}</span>
          <span class="mr-2"><font-awesome-icon icon="chevron-circle-right" /></span>
        </div>
      </a>
      <router-link 
        v-else
        :to="{ name: 'PublicVacancyDetail', params: { vacancyId: vacancyData.id }}"
      >
        <div class="vacancy-name p-1 d-flex justify-content-between">
          <span class="mr-1">{{ vacancyData.name }}</span>
          <span class="mr-2"><font-awesome-icon icon="chevron-circle-right" /></span>
        </div>
      </router-link>
  </div>
</template>

<script>
export default {
  props: {
    vacancyData: Object
  },
  computed: {
    localeModifiedAt() {
      const d = new Date(this.vacancyData.modified_at)
      return d.toLocaleDateString()
    }
  }
}
</script>
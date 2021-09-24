<template>
  <b-list-group flush>
    <b-list-group-item v-for="vacancy in vacancyList" :key="vacancy.id">
      <div class="vacancy-source p-1">
        <b-badge class="mr-1" pill :variant="vacancy.source_name">{{ vacancy.source_name }}</b-badge>
        <b-badge pill variant="light">{{ localeModifiedAt(vacancy) }}</b-badge>
      </div>
      <a v-if="vacancy.source" :href="vacancy.source" target="_blank">
        <div class="vacancy-name p-1 d-flex justify-content-between">
          <span class="mr-1">{{ vacancy.name }}</span>
          <span class="mr-2"><font-awesome-icon icon="chevron-circle-right" /></span>
        </div>
      </a>
      <router-link 
        v-else
        :to="{ name: 'PublicVacancyDetail', params: { vacancyId: vacancy.id }}"
      >
        <div class="vacancy-name p-1 d-flex justify-content-between">
          <span class="mr-1">{{ vacancy.name }}</span>
          <span class="mr-2"><font-awesome-icon icon="chevron-circle-right" /></span>
        </div>
      </router-link>
    </b-list-group-item>
  </b-list-group>
</template>

<script>
export default {
  props: {
    vacancyList: {
      type: Array,
      default: () => [],
    }
  },
  methods: {
    localeModifiedAt(vacancy) {
      const d = new Date(vacancy.modified_at)
      return d.toLocaleDateString()
    }
  }
}
</script>

<style>
  .vacancy-name {
    text-decoration: underline;
  }
</style>
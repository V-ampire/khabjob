<template>
  <div class="filterBar">
    <b-form label-size="lg">
      <div class="filterBar-date mb-2">
        <b-form-datepicker
          v-model="fields.modified_at.value"
          button-variant="dateBtn"
          right
          value-as-date
          label-no-date-selected="Дата обновления вакансии"
        >
          <template v-slot:button-content>
            <font-awesome-icon :icon="['far', 'calendar-alt']" />
          </template>
        </b-form-datepicker>
      </div>
      <div class="filterBar-sourceName mb-2">
        <b-form-select v-model="fields.source_name.value" :options="sourceNameOpts"></b-form-select>
      </div>
      <div class="filterBar-status">
        <b-card>
          <b-form-group label="Статус публикации">
            <b-form-radio v-model="fields.is_published.value" name="isPublished" :value="true">Опубликованные</b-form-radio>
            <b-form-radio v-model="fields.is_published.value" name="isPublished" :value="false">Неопубликованные</b-form-radio>
            <b-form-radio v-model="fields.is_published.value" name="isPublished" :value="null">Все</b-form-radio>
          </b-form-group>
        </b-card>
      </div>
    </b-form>
  </div>
</template>

<script>
import formMixin from '@/components/mixins/formMixin.js'

export default {
  mixins: [formMixin],
  data() {
    return {
      fields: {
        source_name: { value: null, error: null },
        modified_at: { value: null, error: null },
        is_published: { value: null, error: null },
      },

      sourceNameOpts: [
        { value: null, text: 'Источник вакансии.' },
        { value: 'hh', text: 'Headhunter' },
        { value: 'superjob', text: 'Superjob' },
        { value: 'vk', text: 'Вконтакте' },
        { value: 'farpost', text: 'Фарпост' },
        { value: 'khabjob', text: 'Вакансии сайта' },
      ]
    }
  }
}
</script>
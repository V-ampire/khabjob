<template>
  <div class="vacancy-form">
    <b-form>
      <b-form-group
        id="vacancyNameGroup"
        label="Название вакансии"
        label-for="vacancyNameGroup"
      >
        <b-form-input
          id="vacancyNameInput"
          v-model="fields.name.value"
          type="text"
          placeholder="Название вакансии"
          required
          aria-invalid="vacancyNameGroup"
          :state="fields.name.state"
        ></b-form-input>
        <b-form-invalid-feedback id="vacancyNameGroup-error">
          {{ fields.name.error }}
        </b-form-invalid-feedback>
      </b-form-group>
      <b-form-group
        id="vacancySourceGroup"
        label="Ссылка на вакансию"
        label-for="vacancySourceGroup"
      >
        <b-form-input
          id="vacancySourceInput"
          v-model="fields.source.value"
          type="text"
          placeholder="Сслыка на вакансию"
          :state="fields.source.state"
        ></b-form-input>
        <b-form-invalid-feedback id="vacancySourceGroup-error">
          {{ fields.source.error }}
        </b-form-invalid-feedback>
      </b-form-group>
      <b-form-group
        id="vacancyDescriptionGroup"
        label="Описание вакансии"
        label-for="vacancyDescriptionGroup"
      >
        <b-form-textarea
          id="vacancyDescriptionInput"
          v-model="fields.description.value"
          placeholder="Описание вакансии)"
          :state="fields.description.state"
          rows="6"
          no-resize
        ></b-form-textarea>
        <b-form-invalid-feedback id="vacancyDescriptionGroup-error">
          {{ fields.description.error }}
        </b-form-invalid-feedback>
      </b-form-group>
      <b-form-checkbox
        id="is_published"
        v-model="fields.is_published.value"
        name="is_published"
      >
        Опубликовать вакансию
      </b-form-checkbox>
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
        name: {value: null, error: null, state: null},
        source: {value: null, error: null, state: null},
        source_name: {value: null, error: null, state: null},
        description: {value: null, error: null, state: null},
        is_published: {value: true, error: null, state: null},
      }
    }
  },
  methods: {
    validateName() {
      this.fields.name.error = null
      this.fields.name.state = null
      if (!this.fields.name.value) {
        this.fields.name.error = 'Обязательное поле.'
        this.fields.name.state = false
        return false
      }
      this.fields.name.state = true
      return true
    },
    validate() {
      return this.validateName()
    }
  },
}
</script>
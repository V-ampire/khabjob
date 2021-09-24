<template>
  <div class="suggest-form p-2">
    <b-form ref="form" v-on:submit.prevent="suggest" v-if="!showConfirm">
      <b-form-group
        id="vacancyNameGroup"
        label="Название вакансии"
        label-for="vacancyNameGroup"
      >
        <b-form-input
          id="vacancyNameInput"
          v-model="fields.name.value"
          type="text"
          placeholder="Название вашей вакансии..."
          required
          aria-invalid="vacancyNameGroup"
          :state="vacancyNameState"
        ></b-form-input>
        <b-form-invalid-feedback id="vacancyNameGroup-error">
          {{ fields.name.error }}
        </b-form-invalid-feedback>
      </b-form-group>
      <b-form-group
        id="vacancySourceGroup"
        label="Ссылка на вакансию"
        label-for="vacancySourceGroup"
        v-show="addWithSource"
      >
        <b-form-input
          id="vacancySourceInput"
          v-model="fields.source.value"
          type="text"
          placeholder="Сслыка на вакансию"
          :state="vacancySourceState"
        ></b-form-input>
        <div class="help-text">
          Укажите ссылку на вакансию (например на вашем сайте или в соц. сетях), или заполните 
          <span @click="addWithSource=!addWithSource" class="description-toggler">описание</span>
        </div>
        <b-form-invalid-feedback id="vacancySourceGroup-error">
          {{ fields.source.error }}
        </b-form-invalid-feedback>
      </b-form-group>
      <b-form-group
        id="vacancyDescriptionGroup"
        label="Описание вакансии"
        label-for="vacancyDescriptionGroup"
        v-show="!addWithSource"
      >
        <b-form-textarea
          id="vacancyDescriptionInput"
          v-model="fields.description.value"
          placeholder="Описание вакансии (не забудьте контактные данные)"
          :state="vacancyDescriptionState"
          rows="6"
          no-resize
        ></b-form-textarea>
        <div class="help-text">
          Заполните описание вакансии или 
          <span @click="addWithSource=!addWithSource" class="description-toggler">укажите ссылку на вакансию</span> 
          (например на вашем сайте или в соц. сетях).
        </div>
        <b-form-invalid-feedback id="vacancyDescriptionGroup-error">
          {{ fields.description.error }}
        </b-form-invalid-feedback>
      </b-form-group>
      <div class="suggest-form-btn">
        <b-button 
          variant="primary" 
          block
          @click="suggest"
        >Отправить</b-button>
      </div>
    </b-form>
    <div class="suggest-form-confirm text-white bg-success rounded p-2" v-else>
      <h4>Благодарим! Вакансия будет добавлена после проверки администратором!</h4>
    </div>
  </div>
</template>

<script>
import { publicVacanciesApi } from '@/http/clients.js'
import { ServerError } from '@/http/errors.js'
import formMixin from '@/components/mixins/formMixin.js'

export default {
  mixins: [formMixin],
  data() {
    return {
      fields: {
        name: {value: null, error: ''},
        source: {value: null, error: ''},
        description: {value: null, error: ''},
      },
      addWithSource: true,
      showConfirm: false,
    }
  },
  computed: {
    vacancyNameState() {
      if (this.fields.name.error) {
        return false
      }
      if (this.fields.name.value) {
        return true
      }
      return null
    },
    vacancySourceState() {
      if (this.fields.source.error) {
        return false
      }
      if (this.fields.source.value) {
        return true
      }
      return null
    },
    vacancyDescriptionState() {
      if (this.fields.description.error) {
        return false
      }
      if (this.fields.description.value) {
        return true
      }
      return null
    }
  },
  methods: {
    validateFields() {
      if (!this.fields.name.value && !this.fields.description.value) {
        if (this.addWithSource) {
          this.fields.source.error = 'Необходимо указать ссылку или заполнить описание.'
        } else {
          this.fields.description.error = 'Необходимо указать ссылку или заполнить описание.'
        }
        return false
      }
      return true
    },
    async suggest() {
      if (this.validateFields()) {
        const formData = this.getAsFormData()
        try {
          await publicVacanciesApi().create(formData)
          this.showConfirm = true
          setTimeout(() => {
            this.resetFields()
            this.showConfirm = false
          }, 2000)
        } catch(error) {
          if (error instanceof ServerError) {
            for (let field in error.data) {
              if (field in this.fields) {
                this.fields[field].error = error.data[field]
              }
            }
          } else {
            console.log(error.data)
            throw error
          }
        }
      }
    }
  }  
}
</script>

<style>
  .description-toggler {
    cursor: pointer;
    text-decoration: underline;
  }
</style>
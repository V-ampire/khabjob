<template>
  <div class="login">
    <b-container>
      <b-row>
        <b-col cols="12">
          <h3>Введите учетные данные</h3>
          <b-form ref="form" @submit="submit">
            <b-form-group
              id="usernameInputGroup"
              label="Имя пользователя:"
              label-for="usernameInput"
            >
              <b-form-input
                id="usernameInput"
                v-model="fields.username.value"
                type="text"
                placeholder="Имя пользователя"
                required
              ></b-form-input>
            </b-form-group>
            <b-form-group
              id="passwordInputGroup"
              label="Пароль:"
              label-for="passwordInput"
            >
              <b-form-input
                id="passwordInput"
                v-model="fields.password.value"
                type="password"
                placeholder="Ваш пароль"
                required
              ></b-form-input>
            </b-form-group>
            <div class="form-errors text-danger">
              <div class="form-error" v-for="error in formErrors" :key="error">
                {{ error }}
              </div>
            </div>
            <div class="form-btn">
              <b-button 
                variant="primary"
                type="submit"
                block
              >
                Войти
              </b-button>
            </div>
          </b-form>
        </b-col>
      </b-row>
    </b-container>    
  </div>
</template>

<script>
import formMixin from '@/components/mixins/formMixin.js'
import { mapActions, mapGetters } from 'vuex'
import { ServerError } from '@/http/errors'

export default {
  mixins: [formMixin],
  data() {
    return {
      fields: {
        username: {value: null, error: null},
        password: {value: null, error: null}
      },
      formErrors: [],
    }
  },
  computed: {
    ...mapGetters('auth', [
      'isAuthenticated'
    ])
  },
  mounted() {
    if (this.isAuthenticated) {
      this.$router.push({ name: 'Dashboard' })
    }
  },
  methods: {
    ...mapActions('auth', [
      'LOGIN'
    ]),
    async submit(event) {
      event.preventDefault();
      this.formErrors = []
      const credentials = this.getAsFormData()
      try {
        await this.LOGIN(credentials)
      } catch (error) {
        if (error instanceof ServerError && error.status === 400) {
          this.formErrors.push('Неверные имя пользователя или пароль.')
        } else {
          this.formErrors.push(error.message)
          throw error
        }
      }
      this.$router.push({ name: 'Dashboard' })
    }
  },
}
</script>
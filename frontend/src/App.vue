<template>
  <div class="content" id="content">
    <div class="searchBar">
      <VacanciesSearchBar ref="searchBar" />
    </div>
    <div class="alerts">
      <ErrorAlert />
      <SuccessAlert />
      <ConfirmDialog />
    </div>
    <div class="flex-wrapper">
      <div class="wrapper d-flex flex-column">
        <header class="header mb-2" id="header">
          <b-container fluid="xl">
            <nav class="navbar justify-content-between m-auto">
              <span class="navbar-brand">
                <router-link to="/">
                  <img class="navbar-brand-logo" src="@/assets/img/khabjob_logo.png" alt="khabjob">
                </router-link>
              </span>
              <div class="navbar-controls d-flex mr-1">
                <div class="navbar-search mr-2">
                  <a 
                    class="navbar-search-toggler mr-2 mr-md-4"
                    v-on:click="openSearchBar"
                  >
                    <font-awesome-icon size="lg" icon="search" />
                  </a>
                </div>
                <div class="navbar-user" v-if="isAuthenticated">
                  <a class="navbar-user-toggler" id="userToggler" @click="!show">
                    <font-awesome-icon size="lg" icon="user-circle" />
                  </a>
                  <b-popover :show.sync="showUserMenu" variant="primary" target="userToggler">
                    <template #title>{{ user }}</template>
                    <b-list-group>
                      <b-list-group-item>
                        <router-link :to="{name: 'Dashboard'}">Админка</router-link>
                      </b-list-group-item>
                      <b-list-group-item>
                        <a @click="logout">Выйти</a>
                      </b-list-group-item>
                    </b-list-group>
                  </b-popover>
                </div>
              </div>
            </nav>
          </b-container>
        </header>
        <main class="flex-fill">
          <router-view />
        </main>
      </div>
      <footer>
        <b-container class="my-2">
          <b-row>
            <b-col cols="12" sm="10" class="m-auto">
              <div class="add-vacancy m-auto">
                <b-dropdown
                block
                  menu-class="w-100"
                  variant="danger"
                  text="Предложить вакансию"
                >
                  <VacancySuggestForm />
                </b-dropdown>
              </div>
            </b-col>
          </b-row>
          <b-row>
            <b-col cols="6" class="mb-2 mx-auto text-white text-center">
              Разработчик сайта: <strong>
              <a class="developer-name text-white" href="https://vk.com/id152010495">
                V-ampire
              </a>
              </strong>, 2021г.
            </b-col>
          </b-row>
        </b-container>
      </footer>
    </div>
  </div>
</template>

<script>
import VacanciesSearchBar from '@/components/vacancies/VacanciesSearchBar.vue'
import VacancySuggestForm from '@/components/vacancies/VacancySuggestForm.vue'
import ErrorAlert from '@/components/common/ErrorAlert.vue'
import SuccessAlert from '@/components/common/SuccessAlert.vue'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import { mapState, mapGetters, mapActions, mapMutations } from 'vuex';
import { showErrorAlert } from '@/events/utils.js'
import { ON_APP_LOGOUT } from '@/events/types.js'
import eventBus from '@/events/eventBus.js'

export default {
  components: {
    VacanciesSearchBar,
    VacancySuggestForm,
    ErrorAlert,
    SuccessAlert,
    ConfirmDialog,
  },
  data() {
    return {
      showUserMenu: false
    }
  },
  computed: {
    ...mapState('auth', [
      'user'
    ]),
    ...mapGetters('auth', [
      'isAuthenticated'
    ])
  },
  mounted() {
    eventBus.$on(ON_APP_LOGOUT, () => {
      this.REMOVE_USER()
      this.REMOVE_TOKEN()
      console.log('TOKEN IS INVALID')
      this.$router.push({ name: 'Login' })
    })
  },
  methods: {
    ...mapActions('auth', [
      'LOGOUT',
    ]),
    ...mapMutations('auth', [
      'REMOVE_USER',
      'REMOVE_TOKEN',
    ]),
    openSearchBar() {
      this.$refs.searchBar.open()
    },
    async logout() {
      this.showUserMenu = false
      try {
        await this.LOGOUT()
      } catch (error) {
        showErrorAlert(
          'Не удалось разлогинится! Возможно нет соединения с интернетом или недоступен севрер.'
        )
        throw error
      }
      this.$router.push({ name: 'Login' })
    }
  },
}
</script>

<style>
@import './assets/css/main.css';

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
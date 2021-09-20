<template>
  <div class="content" id="content">
    <div class="searchBar">
      <VacanciesSearchBar ref="searchBar" />
    </div>
    <div class="flex-wrapper">
      <div class="wrapper d-flex flex-column">
        <header class="header mb-2" id="header">
          <nav class="navbar justify-content-between m-auto">
            <a class="navbar-brand" href="#">
              <img class="navbar-brand-logo" src="@/assets/img/khabjob_logo.png" alt="khabjob">
            </a>
            <div class="navbar-search">
              <a 
                class="navbar-search search-toggler mr-2 mr-md-4"
                v-on:click="openSearchBar"
              >
                <font-awesome-icon icon="search" />
              </a>
            </div>
          </nav>
        </header>
        <main class="flex-fill">
          <router-view />
        </main>
      </div>
      <footer class="bg-primary">
        <b-container class="my-2">
          <b-row>
            <b-col cols="12">
              <div class="add-vacancy">
                <b-dropdown
                  block
                  menu-class="w-100"
                  variant="dark"
                  text="Предложить вакансию"
                >
                  <VacancySuggestForm />
                </b-dropdown>
              </div>
            </b-col>
          </b-row>
          <b-row>
            <b-col cols="12" class="mb-2 mx-auto text-white">
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

export default {
  components: {
    VacanciesSearchBar,
    VacancySuggestForm
  },
  methods: {
    openSearchBar() {
      this.$refs.searchBar.open()
    },
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
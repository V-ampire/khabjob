<template>
  <div class="content" id="content">
    <div class="searchBar">
      <VacanciesSearchBar ref="searchBar" />
    </div>
    <div class="flex-wrapper">
      <div class="wrapper">
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
        <main>
          <router-view/>
        </main>
      </div>
      <footer></footer>
    </div>
  </div>
</template>

<script>
import VacanciesSearchBar from '@/components/vacancies/VacanciesSearchBar.vue'

export default {
  components: {
    VacanciesSearchBar
  },
  methods: {
    openSearchBar() {
      this.$refs.searchBar.open()
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

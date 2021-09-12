<template>
  <div class="content"></div>
</template>

<script>
export default {
  name: 'App',
  data: () => ({
    name: ''
  }),
  computed: {
    showAlert() {
      return this.name.length > 4 ? true : false
    }
  }
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
  margin-top: 60px;
}
</style>

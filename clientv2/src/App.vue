<template>
  <div id="app">
    <Header/>
    <router-view/>
  </div>
</template>

<script setup>
import Header from './components/Header.vue'

</script>

<style lang="scss">
  @import 'assets/style.scss';
  @import 'assets/animations.css';
  @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@500&display=swap');

  body{
    font-family: 'Roboto', sans-serif;
  }
</style>
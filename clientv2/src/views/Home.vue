<template>
  <div class="home">
    <stocks/>
  </div>
</template>

<script>
// @ is an alias to /src
//import HelloWorld from '@/components/HelloWorld.vue'
import Stocks from '../components/Stocks.vue'

export default {
  name: 'Home',
  components: {
    Stocks
  }
}
</script>

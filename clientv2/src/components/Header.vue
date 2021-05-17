<template>
    <div class="content-input" >
        <form action="" @submit.prevent="changeCurrentStock(ticker)">
            <label for="stockTicker">Ticker: </label>
            <input v-model="ticker" placeholder="Ticker" style="text-transform: uppercase;" id="stockTicker">
            <br>
            <button @click="changeCurrentStock(ticker)">Get Data</button>
        </form>
    </div>
</template>

<script>
import { useStore } from 'vuex';
import { computed } from 'vue';


export default {
    setup(){
        const store = useStore()

        return{
            stock: computed(() => store.state.stock),
            historicalPrices: computed(() => store.state.historicalPrices),
            isLoading: computed(() => store.state.isLoading),

            changeCurrentStock: (tck) => store.dispatch('changeCurrentStock', tck),
        };
    },
    created(){
        this.changeCurrentStock('msft');
    }
}
</script>

<style lang="scss" scoped>
.content-input{
    border-bottom: 1px solid black;
    align-self: center;
    margin: 0;
    padding: 1em;
    display: flex;
    flex-flow: row nowrap;
    justify-content: center;
    align-items: center;

    position: fixed;
    z-index: 999;
    width: 100%;
    margin-top: 0;
    background-color: white;

    form{
        display: flex;
        flex-flow: row nowrap;
        justify-content: center;
        align-items: center;

        input, button{
            height: 2em;
            padding: 0em;
            text-align: center;
            font-size: 1em;
            font-weight: bolder;
        }

        button{
            padding: 0 5px;
            background-color: #124559;
            color: white;
            border: 0;
            transition-duration: 0.3s;

            &:hover{
                cursor: pointer;
                background-color: #01161E;
                box-shadow: 0px 0px 8px 5px rgba(0, 0, 0, 0.137);
            }
        }

        *{
            margin: 0 10px;
        }
    }
}
</style>
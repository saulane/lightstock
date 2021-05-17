<template>
    <div class="content">
        <loading-screen/>

        
        <div v-if="!isLoading" class="data-content">
            <welcome-band/>
            <div class="second-row">
                <stock-chart class="chart-container"/>
                <div class="table-container">
                    <stock-table/>
                </div> 
                <gaps-tables/>
                <return-chart class="card-contouring"/>
            </div>
        </div>
    </div>
</template>

<script>
import { useStore } from 'vuex';
import { computed } from 'vue';

import LoadingScreen from './LoadingScreen.vue';
import StockChart from './StockChart.vue';
import StockTable from './StockTable.vue';
import ReturnChart from './ReturnChart.vue';
import GapsTables from './GapsTables.vue';
import WelcomeBand from './WelcomeBand.vue';

export default {
    name: 'Stocks',
    components:{
        LoadingScreen,
        StockChart,
        StockTable,
        ReturnChart,
        GapsTables,
        WelcomeBand,
    },
    data(){
        return {
            ticker: 'MSFT',
        };
    },
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
};
</script>

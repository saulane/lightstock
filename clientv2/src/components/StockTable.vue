<template>
    <div class="tables">
        <table>
            <thead >
                <th colspan="6">{{ stockInfo["shortName"] }}</th>
                <tr>
                    <td>Date</td>
                    <td>Open</td>
                    <td>High</td>
                    <td>Low</td>
                    <td>Close</td>
                    <td>Return</td>
                </tr>
            </thead>
            <tbody>
                <tr v-for="row in stockPrices.slice(-5)" :key="row">
                    <td>{{ new Date(row['Date']).toLocaleDateString("fr-FR") }}</td>
                    <td>{{ row['Open'] }}</td>
                    <td>{{ row['High'] }}</td>
                    <td>{{ row['Low']}}</td>
                    <td>{{ row['Close'] }}</td>
                    <td>{{ Math.round(row['return'] *10000)/100}}%</td>
                </tr>
            </tbody>
        </table>

        <table>
            <thead>
                <th colspan="2">Return Satistics</th>
            </thead>
            <tbody>
                <tr v-for="(item, index) in returnStats" :key="(item, index)">
                    <td>{{ index }}</td>
                    <td>{{ Math.round(item*10000)/100 }}%</td>
                </tr>
            </tbody>
        </table>
        
    </div>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";

export default({
    setup() {
        const store = useStore()
        
        return{
            isLoading: computed(() => store.state.isLoading)
        }
    },
    computed: {
        stockInfo(){
            return this.$store.state.stock;
        },
        stockPrices(){
            return this.$store.state.historicalPrices;
        },
        returnStats(){
            return this.$store.state.returnStats;
        }
        
    }
})
</script>

<style lang="scss" scoped>
.tables{
    font-weight: 5em;
}
</style>
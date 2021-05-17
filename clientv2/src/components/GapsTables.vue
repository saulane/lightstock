<template>
    <div class="gaps-tables-container">
        <table>
            <thead>
                <th colspan="3">Gaps Satistics</th>
                <tr>
                    <td></td>
                    <td>Up Gap</td>
                    <td>Down Gap</td>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Occurence</td>
                    <td>{{ Math.round(gapStats['upGap']['occurence']*10000)/100 }}%</td>
                    <td>{{ Math.round(gapStats['downGap']['occurence']*10000)/100 }}%</td>
                </tr>
                <tr>
                    <td>Intraday Filled</td>
                    <td>{{ Math.round(gapStats['upGap']['percentFilled']*10000)/100 }}%</td>
                    <td>{{ Math.round(gapStats['downGap']['percentFilled']*10000)/100 }}%</td>
                </tr>
            </tbody>
        </table>

        <table>
            <thead>
                <th colspan="7">Gapping Day Return Statistics</th>
                <tr>
                    <td></td>
                    <td v-for="(item, index) in gapStats['upGap']['dayReturnStats']" :key="(item, index)">{{ index }}</td>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Up Gap</td>
                    <td v-for="(item, index) in gapStats['upGap']['dayReturnStats']" :key="(item, index)">{{ Math.round(item*10000)/100 }}%</td>
                </tr>
                <tr>
                    <td>Down Gap</td>
                    <td v-for="(item, index) in gapStats['downGap']['dayReturnStats']" :key="(item, index)">{{ Math.round(item*10000)/100 }}%</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>

export default ({
    setup() {
    },
    computed: {
        gapStats(){
            return this.$store.state.gapStats;
        }
    }
})
</script>


<style>
.gaps-tables-container{
    display: flex;
    flex-flow: row wrap;
    flex: 1;
    justify-content: center;
    max-width: 100%;
}

.gaps-tables-container table{
    margin: 10px;
}
</style>
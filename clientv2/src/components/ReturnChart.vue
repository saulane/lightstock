<template>
    <div class="stats-charts-container">
        <vue-highcharts
        type="chart"
        :options="returnChartOptions"
        ref="returnChart"
        style="max-width:370px;width:90vw;"
        class="returnDistribChart"/>

        <vue-highcharts
        type="chart"
        :options="rangeChartOptions"
        ref="rangeChart"
        style="max-width:400px;width:90vw;"
        class="trueRangeDistribChart"/>
    </div>
</template>

<script>
import VueHighcharts from 'vue3-highcharts';
import {computed, ref} from 'vue';
import {useStore} from 'vuex';

import HighCharts from 'highcharts';
import HistogramBellcurve from 'highcharts/modules/histogram-bellcurve';

HistogramBellcurve(HighCharts);

export default ({
    name: 'ReturnChart',

    components: {
        VueHighcharts,
    },
    setup() {
        const store = useStore();
      
        var returnsData = ref(computed(() => store.getters.returnsList)).value
        var trueRangeData = ref(computed(() => store.getters.trueRangeList)).value

        var returnChartOptions = computed(() => ({
            title: {
                text: 'Intraday Returns Distribution',
            },
            navigation: {
                bindingsClassName: 'returnChart'
            },
            xAxis: [{
                alignTicks: false
            }, {
                title: { text: 'Daily Return' },
                alignTicks: false,
                opposite: false
            }],
            yAxis: [{
                title: { text: '' },
            }, {
                title: { text: 'Count' },
                opposite: false
            }],
            plotOptions: {
                histogram: {
                    binsNumber: 15
                },
                series: {
                    color: "#598392",
                }
            },
            stockTools: {
                gui: {
                    enabled: false,
                }
            },
            series: [{
                type: 'histogram',
                name: 'Histogram',
                xAxis: 1,
                yAxis: 1,
                baseSeries: 's1',
                showInLegend: false,
                zIndex: -1,
                },
                {
                data: returnsData,
                type: 'scatter',
                id: 's1',
                showInLegend: false,
                visible: false
                }],
        }));

        var rangeChartOptions = computed(() => ({
            title: {
                text: 'True Range Distribution',
            },
            navigation: {
                bindingsClassName: "trueRangeDistribChart"
            },
            stockTools: {
                gui: {
                    enabled: false,
                }
            },
            xAxis: [{
                alignTicks: false
            }, {
                title: { text: 'Daily True Range' },
                alignTicks: false,
                opposite: false
            }],
            yAxis: [{
                title: { text: '' },
            }, {
                title: { text: 'Count' },
                opposite: false
            }],
            plotOptions: {
                histogram: {
                    binsNumber: 15
                },
                series: {
                    color: "#598392",
                }
            },
            series: [{
                type: 'histogram',
                name: 'Histogram',
                xAxis: 1,
                yAxis: 1,
                baseSeries: 's2',
                showInLegend: false,
                zIndex: -1,
                },
                {
                data: trueRangeData,
                type: 'scatter',
                id: 's2',
                showInLegend: false,
                visible: false
                }],
        }));

        return {
            returnChartOptions,
            rangeChartOptions,
            
        }
    },
})
</script>

<style lang="scss" scoped>
.stats-charts-container{
    
    display: flex;
    flex-flow: row wrap;
    justify-content: center;
    border: 0;

    *{
        margin: 0 10px;
    }
}
</style>

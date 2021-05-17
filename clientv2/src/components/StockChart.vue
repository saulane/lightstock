<template>
    <div class="stock-chart-container">
        <vue-highcharts
        type="stockChart"
        :options="stockChartOptions"
        :redrawOnUpdate="true"
        :oneToOneUpdate="false"
        :animateOnUpdate="true"
        ref="stockChart"
        @updated="onUpdate"
        class="stockChart"
        style="max-width:1300px;width:95vw;"/>

    </div>
</template>
<script>
import VueHighcharts from 'vue3-highcharts';
import HighCharts from 'highcharts';

import StockCharts from 'highcharts/modules/stock';
import Indicators from 'highcharts/indicators/indicators-all';

import DragPanes from 'highcharts/modules/drag-panes';
import AnnotationsAdvanced from 'highcharts/modules/annotations-advanced';
import PriceIndicators from 'highcharts/modules/price-indicator';
import FullScreen from 'highcharts/modules/full-screen';

import StockTools from 'highcharts/modules/stock-tools';
import exportingInit from 'highcharts/modules/exporting';

import { ref } from 'vue'

import { useStore } from 'vuex';
import { computed } from 'vue';
//import { mapState } from 'vuex'

StockCharts(HighCharts);
Indicators(HighCharts);
DragPanes(HighCharts);
AnnotationsAdvanced(HighCharts);
PriceIndicators(HighCharts);
FullScreen(HighCharts);
exportingInit(HighCharts);

StockTools(HighCharts);

export default {
    name: 'StockChart',

    components: {
        VueHighcharts,
    },
    setup() {
        const store = useStore()

        var defaultData = ref(computed(() => store.getters.candlestick))
        var volumeData = ref(computed(() => store.getters.volumeDate))
        var stockTicker = ref(computed(() => store.state.stock['longName']))

        var stockChartOptions = computed(() => ({
            title: {
                text: stockTicker.value,
                align: "center",
            },
            navigation: {
                bindingsClassName: "stockChart"
            },
            stockTools: {
                gui: {
                    enabled: true,
                }
            },
            yAxis: [{
                labels: {
                    align: 'left'
                },
                height: '90%',
                resize: {
                    enabled: true
                }
            }, {
                labels: {
                    align: 'left'
                },
                top: '90%',
                height: '10%',
                offset: 0
            }],
            chart: {
                height: 61 + '%',
                events: {
                    load: function(){
                        var chart = this,
                        series = this.series[0],
                        xAxis = chart.xAxis[0],
                        newStart = series.xData[series.xData.length-61],
                        newEnd = series.xData[series.xData.length];
                        xAxis.setExtremes(newStart,newEnd);

                        if(window.screen.width > 600){
                            chart.stockTools.showhideBtn.click();
                        }
                        
                    }
                }
            },
            tooltip: {
                shape: 'square',
                headerShape: 'callout',
                borderWidth: 0,
                shadow: false,
                positioner: function (width, height, point) {
                    var chart = this.chart,
                        position;

                    if (point.isHeader) {
                        position = {
                            x: Math.max(
                                // Left side limit
                                chart.plotLeft,
                                Math.min(
                                    point.plotX + chart.plotLeft - width / 2,
                                    // Right side limit
                                    chart.chartWidth - width - chart.marginRight
                                )
                            ),
                            y: point.plotY
                        };
                    } else {
                        position = {
                            x: point.series.chart.plotLeft,
                            y: point.series.yAxis.top - chart.plotTop
                        };
                    }

                    return position;
                }
            },
            series: [{
                type: 'candlestick',
                id: stockTicker.value,
                name: stockTicker.value,
                data: defaultData.value,
                },{
                type: 'column',
                id: 'stock-volume',
                name: 'Volume',
                data: volumeData.value,
                yAxis: 1
            }],
            plotOptions: {
                candlestick: {
                    dataGrouping: false,
                    color: "black",
                    upColor: "white"
                },
                series: {
                    color: "#598392",
                }
            },
            responsive: {
                rules: [{
                    condition: {
                        maxWidth: 600
                    },
                    chartOptions: {
                        title: {
                            align: "center",
                        },
                        stockTools: {
                            gui: {
                                enabled: false,
                            }
                        },
                        chart: {
                            height: 161 + '%',
                        }

                    },
                }],

            },
        }));

        const onUpdate = () => {
            console.log('Chart updated');
        };

        const updateData = (data) => {
            defaultData.value = data;
        };

        return {
            stockChartOptions,
            onUpdate,
            updateData,
        };
    },
    computed: {
        graphData(){
            return this.$store.getters.candlestick;
        },
    },
    created(){
        //this.updateData(this.graphData)
        this.stockChartOptions.title.text = this.$store.state.stock["longName"]
    }
};
</script>

<style>
@import url('https://code.highcharts.com/css/stocktools/gui.css');
@import url('https://code.highcharts.com/css/annotations/popup.css');

.stock-chart-container{
    margin: 10px;
}

/* .highcharts-arrow-left{
    display: none;
} */

.highcharts-menu-wrapper{
    margin-top: 10px;
    max-height: 350px;
    overflow-y: scroll;
    direction: rtl;
    margin-left:5px;
}

.highcharts-menu-wrapper::-webkit-scrollbar{
    width: 7px;
}

/* .highcharts-menu-wrapper::-webkit-scrollbar-track {

} */

.highcharts-menu-wrapper::-webkit-scrollbar-thumb {
    background-color: #c7c7c7;
    border-radius: 20px;
}

.highcharts-menu-wrapper::-webkit-scrollbar-thumb:hover {
    background-color: #8b8b8b;
}
</style>
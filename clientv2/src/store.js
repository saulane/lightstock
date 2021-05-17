import Vuex from "vuex";
import axios from "axios";

export default new Vuex.Store({
	state: {
		ticker: "aapl",
		isLoading: false,
		stock: {},
		historicalPrices: [],
		returnStats: {},
		gapStats: {},
		cachedData: {}
	},
	getters: {
		pricesForChart(state) {
			var pricesData = [];
			state.historicalPrices.forEach((element) => {
				pricesData.push([element["ts"], element["Close"]]);
			});
			return pricesData;
		},
		candlestick(state) {
			var candles = [];
			state.historicalPrices.forEach((el) => {
				var cdl = [el["ts"], el["Open"], el["High"], el["Low"], el["Close"], el['Volume']];
				candles.push(cdl);
			});
			return candles;
		},
		volumeDate(state){
			var volumes = [];
			state.historicalPrices.forEach((el) => {
				var vol = [el["ts"], el['Volume']];
				volumes.push(vol);
			});
			return volumes;
		},
		returnsList(state){
			var returnsL = []
			state.historicalPrices.forEach((el) => {
				returnsL.push(el['return']*100)
			});
			return returnsL
		},
		trueRangeList(state){
			var trueRangeL = []
			state.historicalPrices.forEach((el) => {
				trueRangeL.push((el['High']/el['Low']-1)*100)
			});
			return trueRangeL
		}
	},
	mutations: {
		loading(state, isLoading) {
			if (isLoading) {
				state.isLoading = true;
			} else {
				state.isLoading = false;
			}
		},
		updateStock(state, data) {
			state.stock = data['info']
			state.historicalPrices = data["prices"];
			state.returnStats = data["returnStatistics"];
			state.gapStats = data["gapStatistics"];
		},
		pushCachedStock(state, data){
			state.cachedData[data[0]] = data[1]
		}
	},
	actions: {
		async getDataFromApi(context, data) {
			const path = "http://127.0.0.1:5000/stocks/";
			context.state.isLoading = true;
			console.log(context.state.cachedData)

			await axios
				.get(path + data, {
					params: {
						ticker: data,
					},
				})
				.then((res) => {
					if (res.data["info"]["symbol"]) {
						context.commit("updateStock", res.data);
						context.commit("pushCachedStock", [data, res.data]);
					} else {
						context.state.ticker = "Ticker invalide";
					}
					context.state.isLoading = false;
				})
				.catch((error) => {
					console.log(error);
				});
		},
		changeCurrentStock(context, tck){
			if (tck in context.state.cachedData){
				context.commit("updateStock", context.state.cachedData[tck]);
			}else{
				console.log(tck)
				context.dispatch('getDataFromApi', tck)
			}
		}
	},
});

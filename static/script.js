function plotSummary(id, data) {
	$("#"+id).sparkline(toint(data), {type:"bar", chartRangeMin:0, chartRangeMax:100});
}

function toint(vals) {
	return $.map(vals, function(val, i) { return Math.round(val); });
}

var chartWidth=600;
var smallChartHeight=300;
var percYAxis = 
	{
		title: { text : null },
		labels : {
			formatter: function() {
				return '' + this.value + '%';
			}
		},
		min: 0,
		max: 100
	};
var percToolFormatter = function() { return '<b>'+ Math.floor(this.y) +'%</b><br/>'; };
	
var chartPrecip, chartFlyability, chartWind, chartDir; 
function setOptions() {
	Highcharts.setOptions({
		chart: {
			type: 'spline', 
			height: smallChartHeight,
			width: chartWidth,
		},
		tooltip: {
			crosshairs : true,
			shared : true,
		},
		legend: { enabled: false },
		credits: { enabled: false },
	});
}
function plotFlyability(id, times, values) {
	chartFlyability = new Highcharts.Chart({
		chart: {
			renderTo: id,
		},
		title: { text: "Chance of Flying" },
		xAxis: { categories: times },
		yAxis: percYAxis,
		tooltip: {
			formatter : percToolFormatter,
			crosshairs : true,
			shared : true,
		},
		series: [{
			name: "Flyability",
			data: values
		}],
	});
}
function plotWindDir(id, times, dir, left, right) {
    var values = [];
    for ( d in dir ) {
        url = '/flyability/wind/dir_' + d + '_' + left + '_' + right + 
              '_40.png';
        values.push( { y: 0, marker: { symbol: 'url(' + url + ')' } } );
    }
	chartFlyability = new Highcharts.Chart({
		chart: {
			renderTo: id,
		},
		title: { text: "Wind Direction" },
		xAxis: { categories: times },
		yAxis: {},
		series: [{
			name: "Wind",
			data: values
		}],
	});
}
function plotWind(id, times, wind, gust) {
	chartWind = new Highcharts.Chart({
		chart: {
			renderTo: id,
		},
		title: { text: "Wind Speed" },
		xAxis: { categories: times },
		yAxis: {
			title: { text : null },
			labels : {
				formatter: function() {
					return '' + this.value + 'mph';
				}
			},
			min: 0,
			max: 20,
			plotBands: [
				{
					from: 12,
					to: 15,
					color: 'rgba(255,0,0, 0.2)',
					label: {
						text: 'P2 wind unsafe',
						style: {
							color: '#606060'
						}
					}
				}, 
				{
					from: 15,
					to: 18,
					color: 'rgba(255,0,0, 0.3)',
					label: {
						text: 'P3 wind / P2 gust unsafe',
						style: {
							color: '#606060'
						}
					}
				}, 
				{
					from: 18,
					to: 20,
					color: 'rgba(255,0,0, 0.4)',
					label: {
						text: 'P3 gust unsafe',
						style: {
							color: '#606060'
						}
					}
				}, 
			],
		},
		tooltip: {
			crosshairs : true,
			shared : true,
		},
		series: [
			{ name: "Wind", data: wind },
			{ name: "Gust", data: gust }
		],
	});
}
function plotPrecip(id, times, values) {
	chartPrecip = new Highcharts.Chart({
		chart: {
			renderTo: id,
			plotBackgroundColor : {
				linearGradient: [0,0,0,smallChartHeight],
				stops: [
					[0, 'rgb(255, 100, 100)'],
					[0.5, 'rgb(255, 200, 200)'],
					[0.7, 'rgb(255, 255, 255)'],
				]

			}
		},
		title: { text: "Chance of Precipitation" },
		xAxis: { categories: times },
		yAxis: percYAxis,
		tooltip: {
			formatter : percToolFormatter,
			crosshairs : true,
			shared : true,
		},
		series: [{
			name: "Chance of Precipitation",
			data: values
		}],
	});
}

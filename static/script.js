function plotSummary(id, data) {
	$("#"+id).sparkline(toint(data), {type:"bar", chartRangeMin:0, chartRangeMax:100});
}

function toint(vals) {
	return $.map(vals, function(val, i) { return Math.round(val); });
}

function drawArrow(id, dir) {
	var canvas = $("#"+id).get(0);
	var context = canvas.getContext("2d");
	// this assumes it's a square.
	w = canvas.width;
	context.clearRect(0,0,w,w);
	pad = 1;
	angle = dir * Math.PI / 180.0;
	c = w / 2;
	halflen = w / 2 - pad;
	incx = halflen * -Math.sin(angle);
	incy = halflen * Math.cos(angle);
	fromx = c - incx;
	fromy = c - incy;
	tox = c + incx;
	toy = c + incy;
	context.beginPath();
	context.lineWidth = 3;
	canvasArrow(context,fromx, fromy, tox, toy);
	context.stroke();
}

function canvasArrow(context, fromx, fromy, tox, toy){
    var headlen = 10;   // length of head in pixels
    var angle = Math.atan2(toy-fromy,tox-fromx);
    context.moveTo(fromx, fromy);
    context.lineTo(tox, toy);
    context.lineTo(tox-headlen*Math.cos(angle-Math.PI/6),toy-headlen*Math.sin(angle-Math.PI/6));
    context.moveTo(tox, toy);
    context.lineTo(tox-headlen*Math.cos(angle+Math.PI/6),toy-headlen*Math.sin(angle+Math.PI/6));
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
	
var chartPrecip, chartFlyability, chartWind; 
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
		legend: { enabled: true },
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

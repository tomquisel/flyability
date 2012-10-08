"use strict";

function Plotter() { }

Plotter.prototype.chartWidth=800;
Plotter.prototype.chartHeight=200;
Plotter.prototype.percYAxis = {
    title: { text : null },
    labels : {
        formatter: function() {
            return '' + this.value + '%';
        }
    },
    min: 0,
    max: 100
};
Plotter.prototype.percToolFormatter = function() { 
    return '<b>'+ Math.floor(this.y) +'%</b><br/>'; 
};
Plotter.prototype.setOptions = function() {
    Highcharts.setOptions({
        chart: {
            type: 'spline', 
            height: this.chartHeight,
            //width: chartWidth,
            marginLeft: 0
        },
        tooltip: {
            crosshairs : true,
            shared : true,
        },
        legend: { enabled: false },
        credits: { enabled: false },
        plotOptions : {
            series : {
                animation : false
            }
        }
    });
};
Plotter.prototype.plotFlyability = function(id, times, values) {
    this.chartFlyability = new Highcharts.Chart({
        chart: {
            renderTo: id,
        },
        title: { text: "Chance of Flying" },
        xAxis: { categories: times },
        yAxis: this.percYAxis,
        tooltip: {
            formatter : this.percToolFormatter,
            crosshairs : true,
            shared : true,
        },
        series: [{
            name: "Flyability",
            data: values
        }],
    });
};
Plotter.prototype.plotPrecip = function(id, times, values) {
    this.chartPrecip = new Highcharts.Chart({
        chart: {
            renderTo: id,
            /*plotBackgroundColor : {
                linearGradient: [0,0,0,chartHeight],
                stops: [
                    [0, 'rgb(255, 100, 100)'],
                    [0.5, 'rgb(255, 200, 200)'],
                    [0.7, 'rgb(255, 255, 255)'],
                ]

            }*/
        },
        title: { text: "Chance of Precipitation" },
        xAxis: { categories: times },
        yAxis: this.percYAxis,
        tooltip: {
            formatter : this.percToolFormatter,
            crosshairs : true,
            shared : true,
        },
        series: [{
            name: "Chance of Precipitation",
            data: values
        }],
    });
};
Plotter.prototype.plotWindDir = function (id, times, dir, left, right) {
    var values = [];
    left = Math.round(left);
    right = Math.round(right);
    for ( var i in dir ) {
        var d = Math.round(dir[i]);
        var url = '/flyability/wind/dir_' + d + '_' + left + '_' 
                  + right + '_50.png';
        values.push( { y: 0, marker: { symbol: 'url(' + url + ')' } } );
    }
    this.chartWindDir = new Highcharts.Chart({
        chart: {
            renderTo: id,
            height: 130,
            type: 'scatter',
        },
        title: { text: "Wind Direction" },
        xAxis: { 
            categories: times,
        },
        yAxis: {
            gridLineWidth: 0,
            title: { text : null },
            labels : {
                formatter: function() {
                    return '   ';
                }
            },
        },
        tooltip: { enabled: false}, 
        series: [{
            name: "Wind",
            data: values
        }],
    });
};
Plotter.prototype.plotWind = function(id, times, wind, gust) {
    var gustMax = Math.max.apply(Math, gust);
    var windMax = Math.max.apply(Math, wind);
    var chartMax = Math.max(gustMax, windMax, 20);
    this.chartWind = new Highcharts.Chart({
        chart: {
            renderTo: id,
            //height: 300,
        },
        title: { text: "Wind Speed" },
        colors: [
            '#4EA54E', 
            '#4572A7',
            ],
        xAxis: { categories: times },
        yAxis: {
            title: { text : null },
            labels : {
                formatter: function() {
                    return '' + this.value + 'mph';
                }
            },
            min: 0,
            max: chartMax,
            plotBands: [
                {
                    from: 12,
                    to: 15,
                    color: 'rgba(255,0,0, 0.2)',
                    label: {
                        text: 'P2 wind unsafe',
                        style: { color: '#606060' }
                    }
                }, {
                    from: 15,
                    to: 18,
                    color: 'rgba(255,0,0, 0.3)',
                    label: {
                        text: 'P3 wind / P2 gust unsafe',
                        style: { color: '#606060' }
                    }
                }, {
                    from: 18,
                    to: 2000,
                    color: 'rgba(255,0,0, 0.4)',
                    label: {
                        text: 'P3 gust unsafe',
                        style: { color: '#606060' }
                    }
                }, 
            ],
        },
        tooltip: {
            borderColor : '#4572A7',
            crosshairs : true,
            shared : true,
            formatter: function() {
                var s = '';
                $.each(this.points, function(i, point) {
                    var ser = point.series;
                    var y = Math.round(point.y);
                    s += '<span style="color:' + ser.color + '">' + 
                         ser.name + '</span>: <b>'+ y +'</b>mph<br/>';
                });
                
                return s;
            },
        },
        series: [
            { name: "Gust", data: gust },
            { name: "Wind", data: wind },
        ],
    });
};

function Plotter2() { }
Plotter2.prototype = new Plotter();

Plotter2.prototype.plotFlyAndPrecip = function(id, times, flyability, precip) {
    this.chartFlyability = new Highcharts.Chart({
        chart: {
            renderTo: id,
        },
        title: { text: null },
        legend: { enabled: true },
        xAxis: { categories: times },
        yAxis: this.percYAxis,
        tooltip: {
            formatter : this.percToolFormatter,
            crosshairs : true,
            shared : true,
        },
        series: [{ name: "Flyability", data: flyability },
                 { name: "Precipitation", data: precip}
                ],
    });
};

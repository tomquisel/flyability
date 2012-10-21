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
    return '<b>'+ Math.round(this.y) +'%</b><br/>'; 
};
Plotter.prototype.percFormatter = function() { 
    return Math.round(this.y) +'%'; 
};

function Plotter2() { }
Plotter2.prototype = new Plotter();

Plotter2.prototype.percYAxis = {
    title: { text : null },
    labels : {
        formatter: function() {
            return '' + this.value + '%';
        }
    },
    tickInterval : 20,
    min: 0,
    max: 100
};
Plotter2.prototype.setOptions = function() {
    Highcharts.setOptions({
        chart: {
            type: 'spline', 
            height: this.chartHeight,
            //width: chartWidth,
            marginLeft: 50
        },
        legend: { enabled: false },
        credits: { enabled: false },
        plotOptions : {
            series : {
                animation : false,
                states: {
                    hover: {
                        enabled: false
                    }
                }
            }
        }
    });
};
Plotter2.prototype.formatter = function(obj, suffix, hasColor, isBold) {
    var color = obj.series.color;
    var y = Math.round(obj.y);
    var s = y + suffix;
    if (isBold) {
        s = "<b>" + s + "</b>";
    }
    if (hasColor) {
        s = '<span style="color:' + color + '">' + s + '</span>';
    }
    return s;
}
Plotter2.prototype.listFormatter = function(obj, suffix, skip) {
    var s = '';
    for (var i in obj.points) {
        var p = obj.points[i];
        var ser = p.series;
        var y = Math.round(p.y);
        if (ser.name == skip) { continue; }
        s += '<span style="color:' + ser.color + '">' + 
             ser.name + '</span>: <b>'+ y +'</b>' + suffix + '<br/>';
    };
    
    return s;
}
Plotter2.prototype.plotFlyAndPrecip = function(id, times, flyability, precip) {
    //var flColor = '#4EA54E';
    //var prColor = '#4572A7';
    //var dataLabels = {
    //    enabled: true,
    //    formatter: function() { 
    //        return Plotter2.prototype.dataLabel(this, "%"); 
    //    },
    //    backgroundColor: '#FFF',
    //    borderRadius: 5,
    //    borderWidth: 1,
    //    shadow: true,
    //    padding: 2,
    //    y: -10
    //}
    //var flDataLabels = jQuery.extend({}, dataLabels);
    //flDataLabels.align = 'left';
    //flDataLabels.x = 2;
    //flDataLabels.borderColor = flColor;
    //var prDataLabels = jQuery.extend({}, dataLabels);
    //prDataLabels.align = 'right';
    //prDataLabels.x = -2;
    //prDataLabels.borderColor = prColor;

    this.chartFlyability = new Highcharts.Chart({
        chart: {
            renderTo: id,
        },
        title: { text: null },
        legend: { 
            enabled: true,
            verticalAlign: "top"    
        },
        colors: plotColors,
        xAxis: { categories: times },
        yAxis: this.percYAxis,
        tooltip: { 
            crosshairs: true,
            shared : true,     
            formatter: function() {
                return Plotter2.prototype.listFormatter(this, "%");
            },
        },
        series: [{ 
                name: "Flyability", 
                data: flyability, 
                lineWidth: 5,
                marker: { radius: 5 },
                //dataLabels: flDataLabels
            }, { 
                name: "Chance of Precipitation", 
                data: precip,
                //dataLabels: prDataLabels
        }],
    });
};

function makePlotBands() {
    var res = [
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
    ];
    return res;
}

function discretize(v, unit) {
    v = v / unit;
    v = Math.round(v);
    v = v * unit;
    return v;
}

function makeArrowUrl(dir, left, right, size) {
    if (size === undefined) {
        size = 30 
    }
    var unit = 5.0;
    dir = discretize(dir, unit);
    left = discretize(left, unit);
    right = discretize(right, unit);
    return 'url(/flyability/wind/dir_' + dir + '_' + left + '_' + right + 
            '_' + size + '.png)';
}

function makeWindValues(dir, left, right, lim) {
    var values = [];
    var y = lim / 5.0;
    left = Math.round(left);
    right = Math.round(right);
    for ( var i in dir ) {
        var d = Math.round(dir[i]);
        var url = makeArrowUrl(d, left, right);
        values.push( { y: y, marker: { fillColor: '#FFF', symbol: url } } );
    }
    return values;
}

Plotter2.prototype.plotWind = function(id, times, wind, gust, dir, 
                                       left, right) 
{
    var gustMax = Math.max.apply(Math, gust);
    var windMax = Math.max.apply(Math, wind);
    var chartMax = Math.max(gustMax, windMax, 20);
    dir = makeWindValues(dir, left, right, chartMax);
    var series = [];
    var myColors = plotColors;
    if (gust.length) {
        series.push({ name: "Gust", data: gust });
    } else {
        myColors = [plotColors[1]];
    }
    series.push({ name: "Wind", data: wind });
    series.push(
        { 
            name: "Direction", 
            data: dir, 
            type: 'scatter', 
            marker: { symbol: makeArrowUrl(215, 200, 300, 15) } 
        });
    this.chartWind = new Highcharts.Chart({
        chart: {
            renderTo: id,
            //height: 300,
        },
        title: { text: null },
        legend: { 
            enabled: true,
            verticalAlign: "top"    
        },
        colors: myColors,
        xAxis: { categories: times },
        yAxis: {
            title: { text : null },
            labels : {
                formatter: function() {
                    return '' + this.value + 'mph';
                }
            },
            tickInterval : 5,
            min: 0,
            max: chartMax,
            plotBands : makePlotBands(),
        },
        tooltip: {
            borderColor : '#4572A7',
            crosshairs : true,
            shared : true,
            formatter: function() {
                return Plotter2.prototype.listFormatter(this, "mph", "Direction");
            },
        },
        series: series
    });
};

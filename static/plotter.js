"use strict";

function Plotter() { }

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
             ser.name + '</span>:<b>'+ y +'</b>' + suffix + '<br/>';
    };
    
    return s;
}

Plotter2.prototype.getFlyDetails = function (time) {
    if (!this.times) {
        console.log("Plotter2 times not initialized!!");
    }
    var ind = this.times.indexOf(time);
    console.log(this.flyDetails);
    var res = {
        pop : this.pop[ind],
        popProb : this.flyDetails.pop[ind],
        wind : this.wind[ind],
        windProb : this.flyDetails.wind[ind],
        dir : this.dir[ind],
        dirProb : this.flyDetails.dir[ind]
    }
    if (this.gust.length > ind) {
        res.gust = this.gust[ind];
        res.gustProb = this.flyDetails.gust[ind];
    }
    return res;
}

Plotter2.prototype.probToSymbol = function(prob) {
    console.log(prob);
    if (prob <= 50) {
        return '<span style="color:#f00">\u2717</span>';
    } else if ( prob < 70) {
        return '\u2013';
    }
    return '<span style="color:' + window.plotColors[0] +'">\u2713</span>';
}

Plotter2.prototype.flyFormatter = function (plotter) {
   var details = plotter.getFlyDetails(this.x);
   var p = this.points[0];
   var ser = p.series;
   var s = ''; 
   var sfm = '<span style="font-size:medium">';
   var es = '</span>';
   s += '<span style="font-weight:bold; font-size:medium">';
   s += Math.round(p.y) + es + sfm + '% Flyable ' + es + '<br>';
   s += plotter.probToSymbol(details.popProb) + ' ';
   s += 'chance of precipitation:<b>' + details.pop + '</b>%<br>';
   s += plotter.probToSymbol(details.windProb) + ' ';
   s += 'wind speed:<b>' + Math.round(details.wind) + '</b>mph<br>';
   if ('gust' in details) {
       s += plotter.probToSymbol(details.gustProb) + ' ';
       s += 'gust speed:<b>' + Math.round(details.gust) + '</b>mph<br>';
   }
   s += plotter.probToSymbol(details.dirProb) + ' ';
   s += 'wind direction:<b>' + dir2str(details.dir) + '</b><br>';
   return s;
}

Plotter2.prototype.plotFly = function(id) {
    var plotter = this;

    this.chartFlyability = new Highcharts.Chart({
        chart: {
            renderTo: id,
        },
        title: { text: null },
        legend: { 
            enabled: true,
            verticalAlign: "top"    
        },
        xAxis: { categories: this.times },
        yAxis: this.percYAxis,
        tooltip: { 
            crosshairs: true,
            shared : true,     
            formatter: function() {
                return plotter.flyFormatter.call(this, plotter);
            }
        },
        series: [{ 
                name: "Flyability at " + this.site, 
                data: this.flyability
        }],
    });
};

function makePlotBands() {
    var res = [
        {
            from: 12,
            to: 15,
            color: 'rgb(255, 220, 220)',
            label: {
                text: 'P2 wind unsafe',
            }
        }, {
            from: 15,
            to: 18,
            color: 'rgb(255, 185, 185)',
            label: {
                text: 'P3 wind / P2 gust unsafe',
            }
        }, {
            from: 18,
            to: 2000,
            color: 'rgb(255, 150, 150)',
            label: {
                text: 'P3 gust unsafe',
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

function makeWindValues(dir, lim, arrowMaker) {
    var values = [];
    var y = -lim * 0.13;
    for ( var i in dir ) {
        var d = Math.round(dir[i]);
        var url = arrowMaker(d);
        values.push( { y: y, marker: { fillColor: '#FFF', symbol: url } } );
    }
    return values;
}

Plotter2.prototype.plotWind = function(id, arrowMaker)
{
    var gustMax = Math.max.apply(Math, this.gust);
    var windMax = Math.max.apply(Math, this.wind);
    var chartMax = Math.round(Math.max(gustMax + 2, windMax + 2, 20));
    var chartMin = Math.round(- 1/4 * chartMax);
    var dir = makeWindValues(this.dir, chartMax, arrowMaker);
    var series = [];
    var myColors = plotColors;
    if (this.gust.length) {
        series.push({ name: "Gust", data: this.gust });
    } else {
        myColors = [plotColors[1]];
    }
    series.push({ name: "Wind", data: this.wind });
    series.push(
        { 
            name: "Direction", 
            data: dir, 
            type: 'scatter', 
            marker: { symbol: arrowMaker(215, 15) } 
        });

    this.chartWind = new Highcharts.Chart({
        chart: {
            renderTo: id,
            height: Plotter2.prototype.chartHeight * 5 / 4,
        },
        title: { text: null },
        legend: {
            enabled: true,
            verticalAlign: "top"    
        },
        colors: myColors,
        xAxis: { categories: this.times },
        yAxis: {
            title: { text : null },
            labels : {
                formatter: function() {
                    if (this.value >= 0) {
                        return '' + this.value + 'mph';
                    } else {
                        return '';
                    }
                }
            },
            tickPositioner: function() {
                return [chartMin, 0, 5, 10, chartMax];
            },
            min: chartMin,
            max: chartMax,
            plotBands : makePlotBands(),
            plotLines : [ { value: 0, width: 2, color: '#000'} ]
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


"use strict";

window.plotColors = [
    '#4EA54E', 
    '#4572A7',
];

function plotSummary(id, data) {
    $("#"+id).sparkline(toint(data), {
        type:"bar", 
        chartRangeMin:0, 
        chartRangeMax:100, 
        tooltipSuffix: "%", 
        barColor: plotColors[0]});
}

function toint(vals) {
    return $.map(vals, function(val, i) { return Math.round(val); });
}

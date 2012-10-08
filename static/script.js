"use strict";

function plotSummary(id, data) {
    $("#"+id).sparkline(toint(data), {type:"bar", chartRangeMin:0, chartRangeMax:100, tooltipSuffix: "%"});
}

function toint(vals) {
    return $.map(vals, function(val, i) { return Math.round(val); });
}

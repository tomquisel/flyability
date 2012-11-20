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

function drawMap(div, lat, lon, sites) {
    var center = new google.maps.LatLng(lat, lon);
    var mapOptions = {
        zoom: 7,
        center: center,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    var map = new google.maps.Map(document.getElementById('mapdiv'), mapOptions);

    for (var i in sites) {
        var site = sites[i];
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(site.lat, site.lon),
            map: map,
            title: site.name
        });
    }
}

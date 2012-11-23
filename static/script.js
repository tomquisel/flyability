"use strict";

window.plotColors = [
    '#4EA54E', 
    '#4572A7',
];

function getMarker(i) {
    var urlstart = "http://maps.google.com/mapfiles/marker";
    var start = "A".charCodeAt(0);
    var ind = String.fromCharCode(Number(start) + Number(i));
    return urlstart + ind + ".png";
}

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
    $.fly.map = new google.maps.Map($('#mapdiv')[0], mapOptions);

    console.log("Markers initialized");
    $.fly.markers = {};
    for (var i in sites) {
        var site = sites[i];
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(site.lat, site.lon),
            map: $.fly.map,
            title: site.name,
        });
        $.fly.markers[site.id] = marker;
    }
    console.log("Checking for markers callback...");
    if ('markers_callback' in $.fly) {
        console.log("Running deferred callback");
        $.fly.markers_callback();
        delete $.fly.markers_callback;
    }
}

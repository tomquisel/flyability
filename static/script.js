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
        barColor: plotColors[0]
    });
}

function toint(vals) {
    return $.map(vals, function(val, i) { return Math.round(val); });
}

function Mapper(args) {
    
    this.div = args.div;
    this.spinner = args.spinner;
    this.infoURL = args.infoURL;

    this.draw = function(lat, lon, sites) {
        var me = this;
        var center = new google.maps.LatLng(lat, lon);
        var mapOptions = {
            zoom: 7,
            center: center,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        }
        this.map = new google.maps.Map(this.div, mapOptions);
        this.setCenterMarker(center);
        
        console.log("Markers initialized");
        this.sites = {};
        for (var i in sites) {
            (function() {
                var site = sites[i];
                var marker = new google.maps.Marker({
                    position: new google.maps.LatLng(site.lat, site.lon),
                    map: this.map,
                    title: site.name,
                });
                var infoWindow = new google.maps.InfoWindow({
                    content: '<img src="' + this.spinner + '"/>'
                });
                var listener = google.maps.event.addListener(marker, 'click', 
                    function() { 
                        me.drawInfo(infoWindow, marker, site.id); 
                    }
                );
                this.sites[site.id] = { 
                    marker : marker,
                    listener : listener,
                    loaded : false
                }
            }.call(this));
        }
        console.log("Checking for markers callback...");
        if ('markers_callback' in this) {
            console.log("Running deferred callback");
            this.markers_callback();
            delete this.markers_callback;
        }
    }

    this.drawInfo = function(info, marker, id) {
        var me = this;
        if (this.openInfo) {
            this.openInfo.close();
        }
        info.open(this.map, marker);
        this.openInfo = info;
        if (!this.sites[id].loaded) {
            $.get(this.infoURL, { id: id }, function (data) { 
                info.setContent(data); 
                me.sites[id].loaded = true;
            });
        }
    }

    this.update = function(lat, lon) {
        var newCenter = new google.maps.LatLng(lat, lon);
        this.map.panTo(newCenter);
        this.setCenterMarker(newCenter);
    }

    this.setCenterMarker = function(latlng) {
        if (this.centerMarker) {
            this.centerMarker.setMap(null);
            delete this.centerMarker;
        }
        this.centerMarker = new google.maps.Marker({
            position: latlng,
            map: this.map,
            icon: "http://www.google.com/mapfiles/arrow.png"
        });
    }

    this.updateMarkers = function(ids) {
        var me = this;
        $.each(this.sites, function(k, v) {
            //var m = me.markers[i];
            //m.setIcon(null);
        });
        for (var i in ids) {
            var marker = this.sites[ids[i]].marker;
            marker.setIcon(getMarker(i));
        }
    }

    this.updateMarkersWhenReady = function(ids) {
        if (!('sites' in this)) {
            console.log("Running callback later");
            this.markers_callback = function() { this.updateMarkers(ids); };
        } else {
            console.log("Running callback now");
            this.updateMarkers(ids);
        }
    }
}

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
        barColor: plotColors[0]
    });
}

function toint(vals) {
    return $.map(vals, function(val, i) { return Math.round(val); });
}

function dir2str(dir) {
    if (typeof(dir2str.mapping) == 'undefined') {
        dir2str.mapping = {
            0 : 'N',
            22.5 : 'NNE',
            45 : 'NE',
            77.5 : 'ENE',
            90 : 'E',
            112.5 : 'ESE',
            135 : 'SE',
            157.5 : 'SSE',
            180 : 'S',
            202.5 : 'SSW',
            225 : 'SW',
            247.5 : 'WSW',
            270 : 'W',
            292.5 : 'WNW',
            315 : 'NW',
            337.5 : 'NNW',
            360 : 'N'
        };
    }
    var best = 'BAD';
    var bestdist = 1000;
    for (var d in dir2str.mapping) {
        if (!dir2str.mapping.hasOwnProperty(d)) {
            continue;
        }
        var dist = Math.abs(d - dir);
        if (dist < bestdist) {
            best = dir2str.mapping[d];
            bestdist = dist;
        }
    }
    return best;
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
        
        this.sites = {};
        for (var i in sites) {
            (function() {
                // this craziness allows for local scoping so objects are 
                // created afresh and not all references to the same thing
                var site = sites[i];
                var sitePos = new google.maps.LatLng(site.lat, site.lon);
                var marker = new google.maps.Marker({
                    position: sitePos,
                    map: this.map,
                    title: site.name,
                });
                var infoWindow = new google.maps.InfoWindow({
                    content: '<img class="cimg" src="' + this.spinner + '"/>'
                });
                var listener = google.maps.event.addListener(marker, 'click', 
                    function() { 
                        me.drawInfo(infoWindow, marker, site.id); 
                    }
                );
                this.sites[site.id] = { 
                    marker : marker,
                    listener : listener,
                    loaded : false,
                }
            }.call(this));
        }
        if ('markers_callback' in this) {
            this.markers_callback();
            delete this.markers_callback;
        }
    }

    this.getMarker = function (i) {
        var urlstart = "http://maps.google.com/mapfiles/marker";
        var start = "A".charCodeAt(0);
        var ind = String.fromCharCode(Number(start) + Number(i));
        return urlstart + ind + ".png";
    }

    this.getIcon = function(which) {
        var url, anchor;
        if (which == "arrow") {
            url = "//www.google.com/mapfiles/arrow.png";
            anchor = new google.maps.Point(12, 34);
        } else if (which == "arrowshadow") {
            url = "//www.google.com/mapfiles/arrowshadow.png";
            anchor = new google.maps.Point(12, 34);
        } else if (which == "shadow") {
            url = "//www.google.com/mapfiles/shadow50.png";
            anchor = new google.maps.Point(11, 34);
        } else {
            alert("Mapper.getIcon FAIL");
        }
        return new google.maps.MarkerImage(url, undefined, undefined, anchor);
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
            delete this.centerMarker; }
        this.centerMarker = new google.maps.Marker({
            position: latlng,
            map: this.map,
            icon: this.getIcon("arrow"),
            shadow: this.getIcon("arrowshadow")
        });
    }

    this.updateMarkers = function(ids) {
        for (var i in this.sites) {
            var site = this.sites[i];
            site.marker.setIcon(null);
            if (site.line) {
                site.line.setMap(null);
                delete site.line;
            }
        }
        for (var i in ids) {
            var site = this.sites[ids[i]];
            site.marker.setIcon(this.getMarker(i));
            site.marker.setShadow(this.getIcon("shadow"));

            var line = new google.maps.Polyline({
              path: [this.map.getCenter(), site.marker.getPosition()],
              strokeColor: '#00F',
              strokeOpacity: 0.5,
              strokeWeight: 2,
              visible: false,
              map: this.map
            });
            site.line = line;
        }
    }

    this.updateMarkersWhenReady = function(ids) {
        if (!('sites' in this)) {
            this.markers_callback = function() { this.updateMarkers(ids); };
        } else {
            this.updateMarkers(ids);
        }
    }
}

<script>
    function doSearch(lat, lon) {
        $("#results").html("Fetching nearby sites...");
        $.get("/flyability/search", {lat : lat, lon : lon}, renderResults)
            .error(function () {alert("Fail!"); });
    }
    function renderResults(data) {
        $("#results").html(data);
        var ids = [];
        var regex = /site_(.+)/;
        var atags = $("#results a");
        for (var i in atags) {
            var link = atags[i];
            var match = regex.exec(link.id);
            if (match) { 
                ids.push(match[1]);
            }
        }
        var lis = $.makeArray($("#results li"));
        for ( var i in lis) {
            $(lis[i]).css('background-image', 'url(' + getMarker(i) + ')');
            console.log("I: " + i);
        }
        if (!('markers' in $.fly)) {
            console.log("Running callback later");
            $.fly.markers_callback = function() { updateMarkers(ids); };
        } else {
            console.log("Running callback now");
            updateMarkers(ids);
        }
    }
    function updateMarkers(ids) {
        console.log("Markers: " +$.fly.markers + " " + typeof($.fly.markers));
        $.each($.fly.markers, function(k, v) {
            //var m = $.fly.markers[i];
            //m.setIcon(null);
        });
        for (var i in ids) {
            var marker = $.fly.markers[ids[i]];
            marker.setIcon(getMarker(i));
        }
    }
    $(function(){
        $("#geocomplete").geocomplete()
        .bind("geocode:result", function(event, result){
            var loc = result.geometry.location;
            doSearch(loc.lat(), loc.lng());
            $.fly.map.panTo(new google.maps.LatLng(loc.lat(), loc.lng()));
        })
        .bind("geocode:error", function(event, status){
            console.log(status);
            $("#results").html("ERROR: " + status);
        })
        .bind("geocode:multiple", function(event, results){
            $("#results").html("Multiple: " + results.length + " results found");
        });

        $("#search").click(function(){
            $("#geocomplete").trigger("geocode");
            return false;
        });

        $.fly = {};
        $.fly.lat = 40;
        $.fly.lon = -80;
        $.get("http://freegeoip.net/json/{{ request.META.REMOTE_ADDR }}", 
            function (data) {
                dict = $.parseJSON(data);
                if (dict) {
                    $.fly.lat = dict.latitude;
                    $.fly.lon = dict.longitude;
                }
        }).complete ( function() {
            // draw the map
            drawMap($("#mapdiv"), $.fly.lat, $.fly.lon, {{ sitesobj|safe }} );
            doSearch($.fly.lat, $.fly.lon);
        });
    });
</script>

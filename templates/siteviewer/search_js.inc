<script>
    function doSearch(lat, lon) {
        $.fly.jsp.getContentPane().html("Fetching nearby sites...");
        $.get("/flyability/search", {lat : lat, lon : lon}, renderResults)
            .error(function () {alert("Fail!"); });
    }
    function renderResults(data) {
        $.fly.jsp.getContentPane().html(data);
        $.fly.jsp.reinitialise();
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
        $.fly.mapper.updateMarkersWhenReady(ids);
    }
    function doResize() {
        var resultsrow = $("#resultsrow");
        var desired = $(window).height() - resultsrow.offset().top;
        resultsrow.css({'height':desired+'px'});
    }
    $(function(){
        $.fly = {};

        doResize();
        $(window).resize(doResize);

        $.fly.jsp = $('.scroll-pane').jScrollPane().data('jsp');

        $(".resitem").live("mouseover", function()
        {
                $(this).css("background-color", "#F3F7FD");
        }).live("mouseout", function()
        {
                $(this).css("background-color", "white");
        });
        $("#geocomplete").geocomplete()
        .bind("geocode:result", function(event, result){
            var loc = result.geometry.location;
            doSearch(loc.lat(), loc.lng());
            $.fly.mapper.update(loc.lat(), loc.lng());
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

        $.fly.lat = 40;
        $.fly.lon = -80;
        $.get("http://freegeoip.net/json/{{ request.META.REMOTE_ADDR }}", 
            function (data) {
                dict = $.parseJSON(data);
                if (dict) {
                    $.fly.lat = dict.latitude;
                    $.fly.lon = dict.longitude;
                }
            }
        ).complete ( function() {
            $.fly.mapper = new Mapper({
                div: $("#mapdiv")[0], 
                spinner: "{{ STATIC_URL }}/spinner.gif",
                infoURL: "{% url 'summary' %}"
            });
            // draw the map
            $.fly.mapper.draw($.fly.lat, $.fly.lon, {{ sitesobj|safe }});
            doSearch($.fly.lat, $.fly.lon);
        });
    });
    </script>

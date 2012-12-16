<script>
    function doSearch(lat, lon, query) {
        $.fly.jsp.getContentPane().html(
        "{% filter escapejs %}{% include "siteviewer/search_loading.inc" %}{% endfilter %}"
        );
        $.fly.jsp.reinitialise();
        $.get("{% url 'search' %}", {lat : lat, lon : lon, query : query}, renderResults)
            .error(function () {console.log("AJAX fail."); });
    }
    
    function getId(resitem) {
        var regex = /site_(.+)/;
        var match = regex.exec(resitem.id);
        if (match) { 
            return +match[1];
        }
        console.log(resitem);
        return null;
    }

    function renderResults(data) {
        var data = "<h4>Paragliding Sites near <br/>" + $.fly.address + 
            "</h4>" + data;
        $.fly.jsp.getContentPane().html(data);
        $.fly.jsp.reinitialise();
        var ids = [];
        var items = $("#results .resitem");
        items.each(function (i, item) {
            ids.push(getId(item));
        });
        var lis = $("#results li");
        lis.each(function (i, li) {
            var marker = 'url(' + $.fly.mapper.getMarker(i) + ')';
            $(li).css('background-image', marker);
            console.log("I: " + i);
        });
        $.fly.mapper.updateMarkersWhenReady(ids);
    }

    function doResize() {
        var resultsrow = $("#resultsrow");
        var desired = $(window).height() - resultsrow.offset().top;
        resultsrow.css({'height':desired+'px'});
    }

    function drawAndSearch() {
        if (!$.fly.mapper) {
            $.fly.mapper = new Mapper({
                div: $("#mapdiv")[0], 
                spinner: "{{ STATIC_URL }}/spinner.gif",
                infoURL: "{% url 'summary' %}"
            });
            $.fly.mapper.draw($.fly.lat, $.fly.lon, {{ sitesobj|safe }});
        }
        doSearch($.fly.lat, $.fly.lon, $.fly.address);
        $.fly.mapper.update($.fly.lat, $.fly.lon);
    }
    
    function geoipLookup(cb) {
        $.get("http://freegeoip.net/json/{{ request.META.REMOTE_ADDR }}", 
            function (data) {
                if (data && data.latitude != "0" && data.longitude != "0") {
                    $.fly.lat = data.latitude;
                    $.fly.lon = data.longitude;
                    $.fly.address = data.city + ", " + data.region_code;
                }
            }
        ).complete ( function() {
            cb();
        });
    }

    $(function(){
        $.fly = {};

        doResize();
        $(window).resize(doResize);

        $.fly.jsp = $('.scroll-pane').jScrollPane( 
            { hideFocus: true } 
        ).data('jsp');

        $(".resitem").live("mouseover", function()
        {
            $.fly.mapper.sites[getId(this)].line.setVisible(true);
            $(this).css("background-color", "#F3F7FD");
        }).live("mouseout", function()
        {
            $.fly.mapper.sites[getId(this)].line.setVisible(false);
            $(this).css("background-color", "white");
        });
        $("#geocomplete").geocomplete()
        .bind("geocode:result", function(event, result){
            var loc = result.geometry.location;
            $.fly.lat = loc.lat();
            $.fly.lon = loc.lng();
            $.fly.address = result.formatted_address;
            console.log(result);
            drawAndSearch();
        })
        .bind("geocode:error", function(event, status){
            console.log(status);
            $("#results").html("ERROR: " + status);
        })
        .bind("geocode:multiple", function(event, results){
            $.fly.jsp.getContentPane().html(results.length + " results found");
        });

        $("#search").click(function(){
            $("#geocomplete").trigger("geocode");
            return false;
        });

        $.fly.lat = 40.7142;
        $.fly.lon = -74.0064;
        $.fly.address = "NYC, NY";
        if ($('#geocomplete').val() != "") {
            $('#geocomplete').trigger("geocode");
        } else {
            geoipLookup(drawAndSearch);
        }
    });
    </script>

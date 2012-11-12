<script>
  $(function(){
    $("#geocomplete").geocomplete()
      .bind("geocode:result", function(event, result){
        var loc = result.geometry.location;
        $("#searchLat").val(loc.Ya);
        $("#searchLon").val(loc.Za);
        /* $("#results").html("Fetching nearby sites...");
        $.get("/flyability/search", {'lat' : lat, 'lon' : lon},
            function(data, textStatus, jqXHR) {
                $("#results").html(data);
        }); */
      })
      .bind("geocode:error", function(event, status){
        alert(status);
        $("#results").html("ERROR: " + status);
      })
      .bind("geocode:multiple", function(event, results){
        $("#results").html("Multiple: " + results.length + " results found");
      });
    
    $("#search").click(function(){
        $("#geocomplete").trigger("geocode");
        return true;
    });
  });
</script>

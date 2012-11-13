<div class="searchrow">
    <form class="form-search" method="GET" action="search">
        <fieldset>
            <input id="geocomplete" type="text" name="query" 
                value="{{ request.GET.query }}"
                class="input-large search-query" 
                placeholder="Enter a city" />
            <input id="searchLat" type="hidden" name="lat" value="" />
            <input id="searchLon" type="hidden" name="lon" value="" />
            <button id="search" type="submit" class="btn">Search</button>
        </fieldset>
    </form>
</div>
<div id="results">
    <ul>
    {% for s in sites %}
    <li><b>{{ s.name }}</b> {{ s.dist_mi }} mi / {{ s.dist_km }} km away</li>   
    {% endfor %}
    </ul>
</div>

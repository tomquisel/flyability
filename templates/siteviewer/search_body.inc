<div class="searchrow">
    <form class="form-search" id="search-form" method="GET" action="{% url 'search' %}">
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
    <li><b><a href={% url 'site' s.country s.state s.name %}>{{ s.name }}, {{s.state}}</a></b> 
    {{ s.dist_mi }} mi / {{ s.dist_km }} km away</li>   
    {% endfor %}
    </ul>
</div>

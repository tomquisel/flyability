    <ul>
    {% for s in sites %}
        <li><b><div><a id="site_{{ s.id }}" href={% url 'site' s.country s.state s.name %}>{{ s.name }}, {{s.statecode}}</a></b> 
            {{ s.dist_mi }} mi away </div>
        {% for day in s.days %}
            <div class="prediction" id="fly_{{s.date}}">
                <strong>{{ day.flyability|floatformat:0 }}</strong>
            </div>
        {% endfor %}
        </li>   
    {% endfor %}
    </ul>

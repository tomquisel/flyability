    <ul>
    {% for s in sites %}
    <li>
        <div id="site_{{ s.id }}" class="resitem">
            <div style="width:100%">
                <b><a target="_blank"
                    href={% url 'site' s.country s.state s.name %}
                >{{ s.name }}, {{s.statecode}}</a></b> 
                <span class="right"><b>{{ s.dist_mi }}</b> mi </span>
            </div>
            {% for day in s.days %}
                <div class="prediction" id="fly_{{s.date}}"
                    style="background:{{ day.color }}">
                    <strong>{{ day.short }}</strong>
                </div>
            {% endfor %}
        </div>
    </li>   
    {% endfor %}
    </ul>

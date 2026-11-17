---
title: Media
---
<iframe class="video" src="https://www.youtube.com/embed/1oTJ6iI6saM" title="4788 Can't Control, 2026 FRC competition season" loading="lazy" allowfullscreen></iframe>

Our 2026 competition season.
{: .lead}

## Robot videos

{% assign robots = site.robots | where_exp: "r", "r.video" | sort: "year" | reverse %}
<ul class="links">
  {% for robot in robots %}<li><a href="{{ robot.url }}">{{ robot.year }}: {{ robot.title }}</a></li>
  {% endfor %}
</ul>

## Events

<ul class="links">
  <li><a href="https://www.youtube.com/watch?v=rQ4boQ2z7zk"><em>FIRST</em> Tech Challenge WA Qualifier 2026 livestream</a></li>
</ul>

## Follow us

{% include socials.html %}

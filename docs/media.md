---
title: Media
---
<iframe class="video" src="https://www.youtube.com/embed/1oTJ6iI6saM" title="4788 Can't Control, 2026 FRC competition season" loading="lazy" allowfullscreen></iframe>

Our 2026 competition season.
{: .lead}

## Photos

<div class="gallery">
  <img class="wide" src="/assets/img/photos/warp-2026-team.jpg" alt="Team 4788 in pink shirts with their two robots on the field at WARP 2026" loading="lazy">
  <img src="/assets/img/photos/warp-2026-robot-fuel.jpg" alt="The 2026 robot on the Rebuilt field, surrounded by yellow fuel balls" loading="lazy">
  <img src="/assets/img/photos/warp-2026-hopper-full.jpg" alt="Close-up of the robot's hopper full of fuel as it drives past" loading="lazy">
  <img class="wide" src="/assets/img/photos/warp-2026-robot-driving.jpg" alt="The 2026 robot driving through a spray of fuel balls at WARP" loading="lazy">
  <img src="/assets/img/photos/warp-2026-robot-red.jpg" alt="The 2026 robot in red bumpers collecting fuel" loading="lazy">
  <img src="/assets/img/photos/warp-2025-gup-x-driving.jpg" alt="Gup X, the 2025 robot, carrying coral across the field at WARP 2025" loading="lazy">
  <img src="/assets/img/photos/warp-2025-9982.jpg" alt="Robot 9982 holding an algae ball at WARP 2025" loading="lazy">
  <img src="/assets/img/photos/warp-2025-gup-x.jpg" alt="Gup X on the field at WARP 2025" loading="lazy">
</div>

Photos from WARP 2025 and WARP 2026.

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

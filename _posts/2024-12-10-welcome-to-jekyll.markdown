---
layout: post
title:  "Hollywood's Ouroboros, or the Endless Cycle of Film content"
order: 1
date:   2024-12-10 17:13:55 +0100
categories: jekyll update
permalink: /movie_evolution/
menu_title: Movie Story
---



<!-- center title of the page -->

<style>
h1 {
    text-align: center;
}
</style>

<!-- intro movie cover slideshow -->

<div class="carousel-container">
  <div class="carousel">
    <img src="{{ site.baseurl }}/assets/images/image_slide_show/avatar.jpg" alt="avatar">
    <img src="{{ site.baseurl }}/assets/images/image_slide_show/bloodshot.jpg" alt="bloodshot">
    <img src="{{ site.baseurl }}/assets/images/image_slide_show/deadpool_2.jpg" alt="deadpool_2">
    <img src="{{ site.baseurl }}/assets/images/image_slide_show/scuicide_squad.jpg" alt="scuicide_squad">
    <img src="{{ site.baseurl }}/assets/images/image_slide_show/spiderman_coming_soon.jpg" alt="spiderman_coming_soon">
    <img src="{{ site.baseurl }}/assets/images/image_slide_show/casino_royale.jpg" alt="casino_royale">
    <img src="{{ site.baseurl }}/assets/images/image_slide_show/fast-and-furious.jpg" alt="fast-and-furious">
    <img src="{{ site.baseurl }}/assets/images/image_slide_show/godzilla.jpg" alt="godzilla">
    <img src="{{ site.baseurl }}/assets/images/image_slide_show/harry_potter.jpg" alt="harry_potter">
    <img src="{{ site.baseurl }}/assets/images/image_slide_show/ice_age.jpg" alt="ice_age">
    <img src="{{ site.baseurl }}/assets/images/image_slide_show/IT_2.jpg" alt="IT_2">
    <img src="{{ site.baseurl }}/assets/images/image_slide_show/star_wars.JPG" alt="star_wars">
    <img src="{{ site.baseurl }}/assets/images/image_slide_show/black_panther.jpg" alt="black_panther">
  </div>
</div>

From the silent films of the late 19th century to today’s billion-dollar franchises, cinema has 
evolved into a rich tapestry of stories, characters, and sagas. At OnceUponATimeInData, we invite 
you on a journey through time, spanning from 1880 to 2024, where every graph, statistic, and 
visualization tells a chapter in the grand narrative of the movie industry. We will try to find 
the different motivation and trends that makes the movie industry produce non-original stories.

In this blog, we’ll combine insights from the CMU Movie Summary Corpus and with data sourced from 
TMDB. We’ll examine how classics inspired modern remakes, how books and comics found new life on 
screen, and how movie studios continuously returned to beloved worlds through sequels. By presenting 
data as a narrative, we aim to show not just the numbers, but the story behind them, revealing the 
patterns, trends, and turning points that shaped over a century of cinema. Enjoy this cinematic 
journey through data, where every chart is a stepping stone deeper into the world of film 
storytelling.

## The phenomenon of non-original movies

### More and more movies
When we look at the current landscape of current movie releases, we see that a majority of well-known
movies are not original. This trend has been accelerating over the years. Different motivations
drive the production of non-original movies. Where historcially, books where the main source of
inspiration, we see that comic adaptations are becoming more popular, especially in the last 20 years.


In the following graph, we plotted the number of movies, sequels, book adaptations, comic adaptations, and remakes released each year. We see that there is an increase in the number of movies released each year.

<p class="grey-italic-caption" style="text-align: center; margin-top: 10px; margin-bottom: 0px;">
  Choose a category to see how it evolve over years.
</p>

<iframe src="{{ site.baseurl }}/results/movie_counter_figure_1880_2024.html" width="100%" height="450" frameborder="0"></iframe>

However, the number of sequels, book adaptations, comic adaptations, and remakes has been increasing at a faster rate. It is interessant to see the different trends in the number of movies released. Book adaptation have seen a linear rise since the early 20th century. This is probably due to the will of filmmakers to adapt well-known stories to the screen, make it their own, and bring it to a new audience. We could also see it as a form of legitimization of a rising movie industry. 

Sequels however, have seen their rise in the 70s, with the rise of the blockbuster. Movies
like Star Wars, Jaws, and Indiana Jones have shown that sequels can be as successful as the original
and are the beginning of franchise movies that are still popular today. Comic adaptations have seen
a rise in the 2000s, the trend that was starting in the CMU dataset has been confirmed in the TMDB
dataset after 2010. 

### Non-original movies are accelerating
One could remark that the number of movie releases has been increasing over the years, so the
trend seen is not that surprising. That would be fairly correct for the case of book adaptations.
Indeed, they remain at a fairely constant rate. Sequels also seem to have had its peak in ratio 
around the 80s.
However, keeping only the CMU dataset would make you miss the main rise in comic adaptations and 
remakes, as well as the resurgence of sequels in the 2000s. The TMDB dataset shows that the trend
of all non-original movies is accelerating. This is worrying, as it could mean that the movie industry
is playing it safe and is using the same stories over and over again.

### Could it be about the money?

The above paragraph sounds more worring than the data. Indeed, in absolute value, the number of
non original movies is increasing, but to a percentage that is still quite low, a few percent of
the total movies released each year.














<!-- single image selector -->

<section id="single-image-section">
  <div class="image-container">
    <img id="selected-image-single" src="{{ site.baseurl }}/assets/images/fast-and-furious.jpg" alt="Selected image">
    <select id="image-selector-single"></select>
  </div>
</section>


Where `YEAR` is a four-digit number, `MONTH` and `DAY` are both two-digit numbers, and `MARKUP` is the file extension representing the format used in the file. After that, include the necessary front matter. Take a look at the source for this post to get an idea about how it works.

Jekyll also offers powerful support for code snippets:

{% highlight ruby %}
def print_hi(name)
  puts "Hi, #{name}"
end
print_hi('Tom')
#=> prints 'Hi, Tom' to STDOUT.
{% endhighlight %}

Check out the [Jekyll docs][jekyll-docs] for more info on how to get the most out of Jekyll. File all bugs/feature requests at [Jekyll’s GitHub repo][jekyll-gh]. If you have questions, you can ask them on [Jekyll Talk][jekyll-talk].

[jekyll-docs]: https://jekyllrb.com/docs/home
[jekyll-gh]:   https://github.com/jekyll/jekyll
[jekyll-talk]: https://talk.jekyllrb.com/

<!-- double image selector -->

<section id="comparison-section">
  <div class="comparison-container">
    <div class="image-container">
      <img id="selected-image-left" src="{{ site.baseurl }}/assets/images/fast-and-furious.jpg" alt="Selected image">
      <select id="image-selector-left"></select>
    </div>
    <div class="image-container">
      <img id="selected-image-right" src="{{ site.baseurl }}/assets/images/harry_potter.jpg" alt="Selected image">
      <select id="image-selector-right"></select>
    </div>
  </div>
</section>

<!-- 
<script>
  const baseurl = "{{ site.baseurl }}";
</script>
-->

<!-- Include CSS and JS 
<link rel="stylesheet" href="{{ site.baseurl }}/assets/css/image-selector.css">
<script src="{{ site.baseurl }}/assets/js/image-selector.js"></script>
-->

Check out the [Jekyll docs][jekyll-docs] for more info on how to get the most out of Jekyll. File all bugs/feature requests at [Jekyll’s GitHub repo][jekyll-gh]. If you have questions, you can ask them on [Jekyll Talk][jekyll-talk].

<div class="original-size-image">
  <img src="{{ site.baseurl }}/assets/images/indiana_jones.jpeg" alt="Indiana Jones Image">
</div>

<!-- New comparison section -->
<section id="new-comparison-section">
  <div class="comparison-container">
    <div class="image-container">
      <img id="new-selected-image-left" src="{{ site.baseurl }}/assets/images/graph_test_1.png" alt="Selected image">
      <select id="new-image-selector-left"></select>
    </div>
    <div class="image-container">
      <img id="new-selected-image-right" src="{{ site.baseurl }}/assets/images/graph_test_2.png" alt="Selected image">
      <select id="new-image-selector-right"></select>
    </div>
  </div>
</section>

<iframe src="{{ site.baseurl }}/assets/test_code/interactive_plot.html" width="100%" height="600" frameborder="0"></iframe>

<iframe src="{{ site.baseurl }}/results/time_between_sequels.html" width="100%" height="1250" frameborder="0"></iframe>
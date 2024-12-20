---
layout: post
title: "Hollywood's Ouroboros, or the Endless Cycle of Film content"
order: 1
date: 2024-12-10 17:13:55 +0100
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


- [The phenomenon of non-original movies](#phenomen-non-original-movie)
    - [More and more movies](#more-and-more-movies)
    - [Non-original movies are accelerating](#non-original-movies-are-accelerating)
    - [Could it be about the money ?](#could-it-be-about-money)
- [Do sequels live up to the hype ?](#do-sequels-live-up-to-the-hype)

From the silent films of the late 19th century to today’s billion-dollar franchises, cinema has
evolved into a rich tapestry of stories, characters, and sagas. At OnceUponATimeInData, we invite
you on a journey through time, spanning from 1880 to 2024, where every graph, statistic, and
visualization tells a chapter in the grand narrative of the movie industry. We will try to find
the different motivation and trends that makes the movie industry produce non-original stories.

In this blog, we’ll combine insights from the CMU Movie Summary Corpus and with data sourced from
TMDB (see how we preprocess data on the [dedicated page]({{ "/data_pre_processing/" | relative_url }})). We’ll examine
how classics inspired modern remakes, how books and comics found new life on
screen, and how movie studios continuously returned to beloved worlds through sequels. By presenting
data as a narrative, we aim to show not just the numbers, but the story behind them, revealing the
patterns, trends, and turning points that shaped over a century of cinema. Enjoy this cinematic
journey through data, where every chart is a stepping stone deeper into the world of film
storytelling.

## <span id="phenomen-non-original-movie">The phenomenon of non-original movies</span>

### <span id="more-and-more-movie">More and more movies</span>

When we look at the current landscape of current movie releases, we see that a majority of well-known
movies are not original. This trend has been accelerating over the years. Different motivations
drive the production of non-original movies. Where historically, books where the main source of
inspiration, we see that comic adaptations are becoming more popular, especially in the last 20 years.

Note that the dataset is not the same before 2010 and after. We will be careful when analysing the data, in
particular when analysing the evolution between before 2010 and after. In absolute value, we are not losing the
data from the CMU dataset for movies after 2010, but we are losing about half of the TMDB dataset if CMU was
updated until 2023. However, most of the movies lost seem to are old movies, so the effect is not as strong as
losing half of the movies after 2010.

TODO : graphique des films non retrouvé pas année

In the following graph, we plotted the number of movies, sequels, book adaptations, comic adaptations, and remakes
released each year. We see that there is an increase in the number of movies released each year.

<p class="grey-italic-caption" style="text-align: center; margin-top: 10px; margin-bottom: 0px;">
  Choose a category to see how it evolves over years.
</p>

<!-- Iframe selector section -->
<section id="second-iframe-section">
  <div class="iframe-container">
    <iframe id="second-selected-iframe" src="" width="100%" height="450" frameborder="0"></iframe>
    <select id="second-iframe-selector"></select>
  </div>
</section>


However, the number of sequels, book adaptations, comic adaptations, and remakes has been increasing at a faster rate.
It is interessant to see the different trends in the number of movies released. Book adaptation have seen a linear rise
since the early 20th century. This is probably due to the will of filmmakers to adapt well-known stories to the screen,
make it their own, and bring it to a new audience. We could also see it as a form of legitimization of a rising movie
industry.

Sequels however, have seen their rise in the 70s, with the rise of the blockbuster. Movies
like Star Wars, Jaws, and Indiana Jones have shown that sequels can be as successful as the original
and are the beginning of franchise movies that are still popular today. Comic adaptations have seen
a rise in the 2000s, the trend that was starting in the CMU dataset has been confirmed in the TMDB
dataset after 2010.

### <span id="non-original-movie-accelerating">Non-original movies are accelerating</span>

The number of movie releases has been increasing over the years, so the
trend seen is not that surprising. That would be fairly correct for the case of book adaptations.
Indeed, they remain at a fairly constant rate before the 2000s. Sequels also seem to have had its peak in ratio
around the 80s.
However, keeping only the CMU dataset would make you miss the main rise in comic adaptations and
remakes, as well as the resurgence of sequels in the 2000s. The TMDB dataset shows that the trend
of all non-original movies is accelerating. This is worrying, as it could mean that the movie industry
is playing it safe and is using the same stories over and over again. Studios have indeed been more and
more reticent to take risks, placing their bets on established franchises and familiar stories to ensure
box office success.

<iframe src="{{ site.baseurl }}/results/ratio_movie_figure_1880_2024.html" width="100%" height="500" frameborder="0"></iframe>

### <span id="could-it-be-about-money">Could it be about the money ?</span>

When my little brother and I looked at the number of non-original movies being released, the graph didn’t seem all that surprising. Sure, the absolute number of sequels, adaptations, and remakes is rising, but in terms of percentage? It’s still just a small slice of the total films released each year. So far, not too worrying.

But then we turned to the box office revenue, and that’s where things got interesting. My brother and I couldn’t help but notice how dramatically non-original movies, particularly sequels, have grown in financial success over the years. Starting in the 1980s, when big blockbuster franchises were just taking off—the box office revenue of sequels began climbing sharply. By the 2000s, these movies were contributing a huge portion of total box office earnings, consistently outperforming other non-original categories like book adaptations, comic adaptations, and remakes. “See?” my brother said, pointing to the graph, “That’s why we all know about superhero movies and *Harry Potter*.”

He wasn’t wrong. Book adaptations have had a steady influence on the box office for decades, with a noticeable peak in the early 2000s, thanks to major literary franchises like *Harry Potter* and *The Lord of the Rings*. “And don’t forget the *Avengers*,” he added excitedly. Comic adaptations are a more recent phenomenon, showing a sharp surge after 2000, propelled by the explosion of superhero blockbusters. As for remakes, well, they’ve had their moments, but they’ve generally played a smaller, more stable role in the industry. “Guess remakes aren’t as cool,” my brother quipped.

What we both found fascinating was the cumulative box office revenue of all non-original movies combined. The graph revealed an unmistakable trend: as sequels rose to dominance, they pulled up the entire category of non-original films with them. By 2020, these movies represented a significant share of total box office revenue. “Wow, studios must really love sequels,” my brother said. He’s right, of course. The data shows that reusing and extending existing intellectual properties isn’t just a trend—it’s a cornerstone of the industry.

<!-- Iframe selector section -->
<section id="iframe-section">
  <div class="iframe-container">
    <iframe id="selected-iframe" src="" width="100%" height="600" frameborder="0"></iframe>
    <select id="iframe-selector"></select>
  </div>
</section>

The average revenue per movie tells another compelling story. Sequels consistently earn more on average than any other type of non-original film, reflecting their reliability as financial assets. Book adaptations, with their peaks driven by beloved franchises, also perform well, while comic adaptations have shown a sharp rise, aligning with their global popularity in recent years. Remakes, on the other hand, often struggle to achieve the same level of success, suggesting that they come with higher financial risks.

My brother summed it up best: “It’s all about giving people what they already love.” He’s onto something. The rise of sequels and adaptations tells us a lot about the film industry: familiarity sells, and franchises with built-in fan bases offer a safer bet for studios. While original films still have their place, they’re no longer the driving force of box office success. For better or worse, the age of non-original movies is here to stay.  

<iframe src="{{ site.baseurl }}/results/box_office_ratio" width="100%" height="500" frameborder="0"></iframe>

## <span id="do-sequels-live-up-to-the-hype">Do sequels live up to the hype ?</span>

Who knew that *Bambi* has sequels? Maybe my little brother… but if we don’t know it, it’s probably due to the lackluster success of the collection. The first movie significantly outshines its sequels. *Bambi*’s original release achieved a staggering $5 billion in box office revenue, while its sequels grossed only around $50 million, highlighting the rare case of a classic film that remains iconic, with its sequels barely remembered by most audiences.

But one thing is clear: my little brother and I both know the legendary spy and the fascinating young wizard with the lightning scar on his forehead. Unlike *Bambi*, mega-franchises like *James Bond* and *Harry Potter* tell a completely different story. The *James Bond* series boasts an incredible $17.2 billion total, with sequels consistently delivering strong box office results, proving the enduring appeal of the iconic spy. Similarly, the *Harry Potter* franchise earned $10 billion collectively, with all installments maintaining high audience appreciation and impressive revenue. These franchises showcase how a beloved universe and consistent quality can elevate every movie in the series.

<iframe src="{{ site.baseurl }}/results/compare_first_sequel_total.html" width="100%" height="600" frameborder="0"></iframe>

Fortunately, my little brother will (hopefully) never discover the *Human Centipede* sequels—better yet, he’s too young to even know about the first movie! Perhaps it’s for the best… as the collection didn’t perform well anyway.


### <span id="how-long-is-to-long-the-wait-between-sequels">Could it be about the money ?</span>















<p class="grey-italic-caption" style="text-align: center; margin-top: 10px; margin-bottom: 0px;">
  Click and drag the map to view data from other countries. You can also zoom in on any area for a closer look.
</p>
<iframe src="{{ site.baseurl }}/results/map_sequels.html" width="100%" height="500" frameborder="0"></iframe>










<!-- single image selector -->

<section id="single-image-section">
  <div class="image-container">
    <img id="selected-image-single" src="{{ site.baseurl }}/assets/images/fast-and-furious.jpg" alt="Selected image">
    <select id="image-selector-single"></select>
  </div>
</section>


Where `YEAR` is a four-digit number, `MONTH` and `DAY` are both two-digit numbers, and `MARKUP` is the file extension
representing the format used in the file. After that, include the necessary front matter. Take a look at the source for
this post to get an idea about how it works.

Jekyll also offers powerful support for code snippets:

{% highlight ruby %}
def print_hi(name)
puts "Hi, #{name}"
end
print_hi('Tom')
#=> prints 'Hi, Tom' to STDOUT.
{% endhighlight %}

Check out the [Jekyll docs][jekyll-docs] for more info on how to get the most out of Jekyll. File all bugs/feature
requests at [Jekyll’s GitHub repo][jekyll-gh]. If you have questions, you can ask them on [Jekyll Talk][jekyll-talk].

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

Check out the [Jekyll docs][jekyll-docs] for more info on how to get the most out of Jekyll. File all bugs/feature
requests at [Jekyll’s GitHub repo][jekyll-gh]. If you have questions, you can ask them on [Jekyll Talk][jekyll-talk].

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
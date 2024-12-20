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
    - [How long is too long ?](#how-long-is-too-long)
- [The cost of success](#cost-of-success)
  - [Standalone or first movie in sequels ?](#standalone-vs-first-movie-collection)
  - [Collection investments](#collection-investments)
  - [Genres and adaptations](#genres-and-adapations)
- [What audience think ?](#what-audience-think)
  - [Does the first movie set the standard ?](#does-the-first-movie-standard)
  - [Does spending buy approval ?](#does-spending-buy-approval)


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

But then we turned to the box office revenue, and that’s where things got interesting. My brother and I couldn’t help but notice how dramatically non-original movies, particularly sequels, have grown in financial success over the years. Starting in the 1980s, when big blockbuster franchises were just taking off, the box office revenue of sequels began climbing sharply. By the 2000s, these movies were contributing a huge portion of total box office earnings, consistently outperforming other non-original categories like book adaptations, comic adaptations, and remakes. “Look ! That’s why we all know about superhero movies and *Harry Potter*.” He wasn’t wrong. Book adaptations have had a steady influence on the box office for decades, with a noticeable peak in the early 2000s, thanks to major literary franchises like *Harry Potter* and *The Lord of the Rings*. “And don’t forget the *Avengers*,” he added excitedly. Comic adaptations are a more recent phenomenon, showing a sharp surge after 2000, propelled by the explosion of superhero blockbusters. As for remakes, well, they’ve had their moments, but they’ve generally played a smaller, more stable role in the industry. “Guess remakes aren’t as cool,” my brother quipped.

What we both found fascinating was the cumulative box office revenue of all non-original movies combined. The graph revealed an unmistakable trend: as sequels rose to dominance, they pulled up the entire category of non-original films with them. By 2020, these movies represented a significant share of total box office revenue. “Wow, studios must really love sequels,” my brother said. He’s right, of course. The data shows that reusing and extending existing intellectual properties isn’t just a trend, it’s a cornerstone of the industry.

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


### <span id="how-long-is-too-long">How long is too long ?</span>

<iframe src="{{ site.baseurl }}/results/time_between_sequels.html" width="100%" height="1225" frameborder="0"></iframe>


This graph highlights the diverse release patterns of movie franchises and the varying impacts of time gaps between sequels.

Some classics like 101 Dalmatians (released in 1961) remain widely known and loved, but their sequels, such as the follow-up released decades later, have struggled to gain the same recognition. When I asked my little brother if he knew *101 Dalmatians* he said: "Of cours, everyone knows that movies !" But when I mentionned there was sequels, he looked puzzled. Similarly, *Cinderella*, first released in 1950, is a timeless story still celebrated today, yet its sequels (*Cinderella II* and *Cinderella III*) are far less memorable.

On the other hand, franchises like *Harry Potter* demonstrate the power of consistent and efficient releases. With all movies released between 2001 and 2011, the series maintained a steady momentum, keeping audiences engaged without long waits between installments. The *Hunger Games* franchise initially followed a similar pattern, with four movies released annually from 2012 to 2015. However, the graph shows a significant gap before the release of its 2023 prequel: *The Ballad of Songbirds and Snakes*, showcasing how studios often return to successful universes to revive audience interest.

As we scanned further, my little brother spotted *Star Wars*. “Oh, I love Star Wars! But why does it start at number five?” I laughed. “Actually, it starts at number four, and then they went back later to make the first three movies. The release order was very original!” We marveled at how *Star Wars* began with *The Empire Strikes Back* (1980) and became one of the most beloved franchises, despite its unconventional order.

Some franchises, such as *Bambi*, illustrate extreme gaps between installments. The original Bambi was released in 1942, but its sequel didn’t appear until 2006—a remarkable 64-year gap, highlighting the challenges of building upon a classic decades later. "That's probably why nobody knows about the *Bambi* sequel" my little brother added.

Interestingly, horror movies like *The Exorcist* show exceptional longevity. Spanning from pre-1980 to beyond 2020, this franchise demonstrates the enduring appeal of horror films, which often continue to attract audiences across generations. When I saw my little brother’s surprised face, I reassured him: “Don’t worry, we’ll explore it later, no need to be impatient.”

we can see how timing of sequels can make or break a franchise. While some benefit from efficient releases to sustain audience momentum, others rely on nostalgia or genre appeal to remain relevant over decades.



## <span id="cost-of-sucess">The cost of success</span>

### <span id="standalone-vs-first-movie-collection">Standalone or first movie in sequels ?</span>

An intriguing aspect of the film industry is understanding the factors that influence studios to produce sequels to original movies. Since studios often prioritize maximizing profits, it becomes essential to investigate whether certain attributes of the first movie in a series significantly impact the likelihood of a sequel being made. 
“But how can we know that ?” my little brother asked. “Just watch, we’ll find out right now”. 
To explore this, we analyzed two key metrics: the box office revenue and the average audience vote for standalone movies versus the first movies in a collection, specifically focusing on films released between 2010 and 2024.
Our analysis involved taking a random sample of 100 movies from both categories. Plotting the data on a graph revealed a striking trend. Movies that served as the starting point for a collection tended to cluster in the upper-right corner of the plot, exhibiting both higher box office revenues and slightly better average audience votes compared to standalone films. This pattern strongly suggests that financial success plays a critical role in a studio's decision to greenlight a sequel. The rationale here is straightforward: a movie that performs exceptionally well at the box office provides a promising foundation for a sequel, as it has already demonstrated its ability to attract a large audience.
Interestingly, movies that later spawned sequels also displayed a tendency to receive higher average audience votes. This could indicate that critical and audience reception also plays a role in the decision-making process. After all, when audiences enjoy the first opus, they are more likely to return for a sequel. Sequels often maintain a consistent storyline, featuring familiar characters and themes that resonate with fans of the original film. Studios likely recognize that audience attachment to these elements increases the likelihood of a sequel's success, making it a relatively safer investment compared to standalone projects.
To validate the trends observed in our graph, we performed statistical tests to determine whether the differences in revenue and average vote between the two groups were statistically significant. For the average vote, we applied a t-test since the data followed a normal distribution. For box office revenue, which did not meet the normality criteria, we used a Mann-Whitney U Test, a non-parametric alternative suited for skewed data distributions.

"But how can we validate this ? Are we sure about it ?", "I’m not sure you’ll understand the math behind this, but let me explain it to you, little brother". 

The results of these tests confirmed our initial observations. The *t-test* for average vote showed a significant difference, indicating that movies leading to sequels indeed tend to have higher audience ratings. Similarly, the *Mann-Whitney U Test* for revenue reinforced the conclusion that higher box office revenue is a strong predictor for sequels. 

"Oh, so if a movie is really liked by people and makes a lot of money, it tends to get a sequel. That makes sense.", "Haha, yes indeed. Remember when you watched your first Shrek? You were so impatient to see the next one." 

<iframe src="{{ site.baseurl }}/results/Revenue_vs_vote.html" width="100%" height="500" frameborder="0"></iframe>

|                  | Test Result   | p-value       |
|:----------------:|:-------------:|:-------------:|
|Revenue (U_stat)  | 328073.5      | 7.6e-108      |
|Vote (t_stat)     | -7.9952       | 1.5e-15       |

### <span id="collection-investments">Collection Investments</span>

The *Harry Potter* collection towers above most, with a staggering box office revenue exceeding $10 billion. But it’s no mystery why—this collection is also among the highest-budgeted, with each movie requiring over $100 million to bring its magical world to life. “Well, it’s probably hard to make all those special effects, even if we know that Hogwarts Castle is just a miniature!” Despite the high cost, *Harry Potter* consistently sits far above the return on investment curve, proving that investing big can also mean earning big.

Interestingly, we noticed that most collections, hover above the return on investment line. This means that, in general, collections are profitable ventures for studios. Only a few collections fall below the curve, representing those rare cases where large budgets didn’t translate into financial success.

<iframe src="{{ site.baseurl }}/results/budget_vs_revenue.html" width="100%" height="500" frameborder="0"></iframe>

Then came a shocker: *The Amityville Horror*. “What? Almost $1 billion in revenue with barely a $1 million budget?” my little brother exclaimed. It’s true, *Amityville* is one of the standout examples of incredible return on investment. Horror collections, as it turns out, often follow this pattern. *The Exorcist* also caught my little brother eye eye. “Oh, that one again! It’s one of the biggest earners too!” he said, noticing its approximately $5 billion revenue. “Guess I’ll start watching horror movies soon.” I quickly reminded him, “Maybe wait a few years before diving into those…”

However, not every high-budget collection follows the typical financial story. The *Spider-Man* collection, for instance, claims the top spot for the highest budgets, soaring well above $100 million per movie. “Do you think Spider-Man’s webs cost that much to make?” he joked. Still, its impressive box office revenue proves that even the priciest collections can be worth the investment.

Overall, the graph reveals a fascinating trend: while some collections achieve incredible returns with tiny budgets, like *Amityville*, others, like *Spider-Man* and *Harry Potter*, show that massive budgets can still pay off handsomely. Most importantly, it highlights the diversity of financial strategies in the film industry, some opt for high-budget blockbusters, while others succeed by turning small investments into big hits.

### <span id="genres-and-adaptations">Genres and adapations</span>

<iframe src="{{ site.baseurl }}/results/genre_heatmap_box_office.html" width="100%" height="500" frameborder="0"></iframe>

Unsurprisingly, adventure is the standout genre, particularly for comic adaptations and sequels. “That makes sense,” I thought to myself as I looked at the data. *Indiana Jones*, for example, shines as a classic comics adventure. Sequels in the adventure genre are once again consistently major earners, reflecting the audience’s appetite for continued exploration of familiar, thrilling worlds.

Science fiction also proves to be a strong performer for comic adaptations. It’s hard not to think of *Marvel and DC* movies here, franchises that blend superheroes and futuristic themes into blockbusters that rake in massive revenues.

On the other hand, remakes continue to struggle. For family films, in particular, remakes fall behind standalone movies in revenue. It seems audiences may prefer the charm of original family stories to reimagined classics, "I don’t really like family films,” my little brother added. “Mum always wants us all to watch a Christmas family movie on Christmas Eve", "I understand you" I said, laughing. And in general, remakes only rarely manage to surpass the revenues of their standalone counterparts, which aligns with the trend we’ve seen throughout the analysis: remakes face significant challenges in replicating the success of their originals.

Finally, sequels are the champions across the board. Their ability to build on established worlds and fan bases makes them a reliable choice for studios looking to maximize box office returns.

Overall, the data reveals the complex dynamics between genre and type, showing how certain combinations, like adventure sequels or science fiction comic adaptations, can drive incredible financial success, while others, like family remakes, face a difficult battle to resonate with audiences.

## <span id="what-audience-think">What audience think ?</span>

### <span id="does-the-first-movie-standard">Does the first movie set the standard ?</span>

"Tell me, big brother, we’ve compared standalone movies and the first movie in a series, but are the following sequels just as loved ?", "Haha, let’s take a closer look at the sequels to find out!"

Sequels often come with a great deal of anticipation. When we head to the theaters to watch the latest installment of a well-loved franchise, it’s typically because we thoroughly enjoyed the previous movies and are eager to see the continuation of the story. However, this raises an intriguing question: does this high level of expectation influence how we perceive sequels? Or are we so invested in the franchise that our opinions about sequels become less objective? To delve into this, we analyzed the overall appreciation of sequels compared to the first movie in a series.

The following graph compares the rating of the first movie in a collection to the average rating of the rest of the sequels combined. The movies are ranked based on the score of the first installment, allowing for a clear visual representation of trends.
The results are striking. It quickly becomes evident that the majority of sequels receive lower ratings than the first movie. Only a small number of franchises manage to achieve higher average ratings for the rest of the collection. Interestingly, after a certain threshold of first-movie rating, it becomes exceedingly rare for a collection’s average score to surpass that of the original.

“Oh, that could explain why I was a bit disappointed when I saw *Shrek II*.” “Yes, probably,” I said to my little brother, laughing.


<iframe src="{{ site.baseurl }}/results/average_rating_first_vs_rest.html" width="100%" height="630" frameborder="0"></iframe>


“But look at this one, it’s interesting. That’s not always the case…”

One notable outlier is the *Lord of the Rings* trilogy. Not only does the first movie boast one of the highest ratings, but the franchise remarkably managed to surpass this score with its sequels, a truly exceptional feat in the world of cinema. This example highlights how rare it is for sequels to outperform their predecessors, especially when the bar is already set exceptionally high.

On the other end of the spectrum, some studios have made the curious decision to produce sequels for movies with ratings below the average for standalone films. At first glance, this seems counterintuitive, as one might expect studios to focus their resources on expanding stories with strong audience and critical reception. 

However, there could be several explanations for this phenomenon. In some cases, sequels may have been pre-planned and already in production when the first movie was released.


### <span id="does-spending-buy-approval">Does spending buy approval ?</span>


<!-- Graph Carousel Section -->
<div id="graph-carousel" class="graph-carousel">
  <iframe id="graph-frame" src="{{ site.baseurl }}/results/revenu/revenu1.html" frameborder="0"></iframe>

  <!-- Navigation controls -->
  <button id="prev-button" class="carousel-control prev">←</button>
  <button id="next-button" class="carousel-control next">→</button>

  <!-- Play/Pause button -->
  <button id="play-pause-button" class="play-pause">Play</button>
</div>

This graph takes us into the ups and downs of movie franchises! It shows, for the 5 firts movies, revenue versus ratings, with blue dots for movies that outscore their predecessors and red for those that fall short. 

What stands out? Well, second films often struggle, with many dropping in both ratings and revenue. But it’s not all downhill. Some franchises, like *Harry Potter*, buck the trend and show major improvements in later films. 

We can also spot a tendency for first films to shine brightest, often leading in both revenue and ratings. Still, the graph reminds us: franchises don’t follow a fixed formula, some truly find their magic over time!

Once we adjusted for inflation, the results changed dramatically! The rankings shifted, with new winners emerging, and some of today’s biggest blockbusters no longer claiming the title of the greatest franchises in history. Context truly reshapes the narrative!





<p class="grey-italic-caption" style="text-align: center; margin-top: 10px; margin-bottom: 0px;">
  Click and drag the map to view data from other countries. You can also zoom in on any area for a closer look.
</p>
<iframe src="{{ site.baseurl }}/results/map_sequels.html" width="100%" height="500" frameborder="0"></iframe>


<iframe src="{{ site.baseurl }}/results/violin_chart_studio.html" width="100%" height="630" frameborder="0"></iframe>




























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
---
layout: post
title:  "Once upon a time...in movie's data"
date:   2024-12-10 17:13:55 +0100
categories: jekyll update
---

<!-- center title of the page -->

<style>
h1 {
    text-align: center;
}
</style>

<!-- intro image -->

<div class="classic-image">
  <img src="{{ site.baseurl }}/assets/images/reddit.jpg" alt="Reddit Image">
</div>


<div class="carousel-container">
  <div class="carousel">
    <img src="{{ site.baseurl }}/assets/images/image_slide_show/black_panther.jpg" alt="black_panther">
    <img src="{{ site.baseurl }}/assets/images/image_slide_show/bloodshit.jpg" alt="bloodshit">
    <img src="{{ site.baseurl }}/assets/images/image_slide_show/deadpool_2.jpg" alt="deadpool_2">
    <img src="{{ site.baseurl }}/assets/images/image_slide_show/scuicide_squad.jpg" alt="scuicide_squad">
    <img src="{{ site.baseurl }}/assets/images/image_slide_show/spiderman_actor.jpg" alt="spiderman_actor">
    <img src="{{ site.baseurl }}/assets/images/image_slide_show/spiderman.jpg" alt="spiderman">
    <img src="{{ site.baseurl }}/assets/images/image_slide_show/the_predator.jpg" alt="the_predator">
  </div>
</div>



You’ll find this post in your `_posts` directory. Go ahead and edit it and re-build the site to see your changes. You can rebuild the site in many different ways, but the most common way is to run `jekyll serve`, which launches a web server and auto-regenerates your site when a file is updated.

Jekyll requires blog post files to be named according to the following format:

`YEAR-MONTH-DAY-title.MARKUP`

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
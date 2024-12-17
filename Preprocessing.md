---
layout: page
title: Data pre-processing
order: 2
permalink: /data_pre_processing/
---

We began our analysis with the [CMU Movie Summary Corpus](http://www.cs.cmu.edu/~ark/personas/) as our foundational dataset. To incorporate additional films, such as sequel collections, sequels, book adaptations, comic adaptations, and remakes, we utilized the [TMDB dataset](https://www.themoviedb.org). Since the TMDB data lacked direct Wikipedia IDs, we scraped Wikipedia to obtain them for each TMDB movie. Armed with these IDs, we merged the TMDB data into the CMU dataset, linking existing entries and adding new films to expand our analysis. The following graph illustrates the varying sizes of the TMDB dataset, the CMU dataset, and the final filtered dataset after these integrations.

<iframe src="{{ site.baseurl }}/results/data_cleaning_graph.html" width="100%" height="520" frameborder="0"></iframe>


We see that the [TMDB dataset](https://www.themoviedb.org) is much more exhaustive than our database. We lose quite a lot of data 
points, but we were still able to recover a lot of movies. However, in the rest of the analysis,
we will have to be careful when looking at data before 2010, which will be the data coming from the 
CMU dataset, and the data after, which comes from TMDB. In absolute value, we should be losing about
half of the TMDB dataset if CMU was updated until 2023.

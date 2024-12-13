---
layout: page
title: Data pre-processing
permalink: /data_pre_processing/
---

We began our analysis with the [CMU Movie Summary Corpus](http://www.cs.cmu.edu/~ark/personas/) as our foundational dataset. To incorporate additional films, such as sequel collections, sequels, book adaptations, comic adaptations, and remakes, we utilized the [TMDB dataset](https://www.themoviedb.org). Since the TMDB data lacked direct Wikipedia IDs, we scraped Wikipedia to obtain them for each TMDB movie. Armed with these IDs, we merged the TMDB data into the CMU dataset, linking existing entries and adding new films to expand our analysis. The following graph illustrates the varying sizes of the TMDB dataset, the CMU dataset, and the final filtered dataset after these integrations.

ADD PLOT

ADD PLOT DESCRIPTION

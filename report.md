# Main Post
## 1. Intro:

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


## 2. Data pre-processing

We began our analysis with the CMU Movie Summary Corpus as our foundational dataset. To incorporate 
additional films—such as sequel collections, sequels, book adaptations, comic adaptations, and 
remakes we utilized the TMDB dataset. This dataset is very useful, because the movies in that 
database have tags based on if they are sequels, book adaptations, comic adaptations, and remakes.
We also used further data to add data such as the missing box office entries, the movie budget and 
the user ratings. Since the TMDB data lacked direct Wikipedia IDs, we scraped Wikipedia to obtain 
them for each TMDB movie. Unfortunately, some movies were still missing. That is why we also added 
movies if the had the same title and release year. Armed with these IDs, we merged the TMDB data 
into the CMU dataset, linking existing entries and adding new films to expand our analysis. 
The following graph illustrates the varying sizes of the TMDB dataset, the CMU dataset, and the 
final filtered dataset after these integrations.


We see that the TMDB dataset is much more exhaustive than our database. We lose quite a lot of data 
points, but we were still able to recover a lot of movies. However, in the rest of the analysis,
we will have to be careful when looking at data before 2010, which will be the data coming from the 
CMU dataset, and the data after, which comes from TMDB. In absolute value, we should be losing about
half of the TMDB dataset if CMU was updated until 2023.

## The phenomenon of non-original movies

### More and more movies
When we look at the current landscape of current movie releases, we see that a majority of well-known
movies are not original. This trend has been accelerating over the years. Different motivations
drive the production of non-original movies. Where historcially, books where the main source of
inspiration, we see that comic adaptations are becoming more popular, especially in the last 20 years.


In the following graph, we plotted the number of movies, sequels, book adaptations, comic adaptations, and remakes  
released each year. We see that there is an increase in the number of movies released each year.
However, the number of sequels, book adaptations, comic adaptations, and remakes has been increasing
at a faster rate. It is interessant to see the different trends in the number of movies released.
Book adaptation have seen a linear rise since the early 20th century. This is probably due to the 
will of filmmakers to adapt well-known stories to the screen, make it their own, and bring it to a
new audience. We could also see it as a form of legitimization of a rising movie industry. 

Sequels however, have seen their rise in the 70s, with the rise of the blockbuster. Movies
like Star Wars, Jaws, and Indiana Jones have shown that sequels can be as successful as the original
and are the beginning of franchise movies that are still popular today. Comic adaptations have seen
a rise in the 2000s, the trend that was starting in the CMU dataset has been confirmed in the TMDB
dataset after 2010. 

### Non-original movies are accelarating
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




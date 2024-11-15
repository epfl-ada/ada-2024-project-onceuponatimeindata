# Why your favorite movie does/doesn't have a sequel

## Abstract
Our project, explores the patterns and factors that influence the retelling of stories instead of brand new creations. We looked at movies that are sequels, book adaptaions, comics adaptations and remakes. By analyzing a movie dataset, we aim to uncover what are the genres that most often lead to non-original stories, the financial incentives needed, 
and viewer engagement that drive sequels the be produced. We’ll investigate questions like: 
What is the average box office revenue for movies with sequels? How do ratings compare between
original movies and their sequels? And do certain genres, like action or comedy, have a higher
likelihood of spawning a series? Do sequels have a longer or shorter playing time then the 
originals? Through this analysis, we aim to highlight the economic and creative motivations 
behind sequels, and examine whether sequels generally succeed in meeting or surpassing the 
popularity and quality of the original or if some of them are made to maximize profit. 
Ultimately, our project offers insights into why the movie industry likes to reuse stories,
and which ones are most likely to be retold, while others remain single installments
It will helping movie enthusiasts understand the trends shaping the industry.

## Research Questions

What genres are most likely to have sequels?

What is the average box office revenue for movies with sequels compared to standalone movies?

Will the new blockbusters of 2024 have sequels based on audience ratings?

Does the presence of a sequel correlate with specific cast, director, or studio attributes?

What role does time between releases play in a sequel’s success?

What are the trends in sequel production over time?

What is the influence of initial audience ratings or critic reviews on the decision to produce a sequel?

Can we see a trend in the evolution of castings in sequels?


## Additional Dataset
we gathered aditional datasets about book that have film adaptation and their sequels which opens new questions like for example: What genre of story is most likely to have a movie adaptation.
## Organization within the team
- **Clara**: In charge of global clarity and homogenize et qualité des graphique, création de graph interactif
- **Yann**: Character evolution in sequels  
- **Jules**: Prediction of the existence of a sequel based on ratings, particularly using IMDb data from 2024 films
- **Quentin**: Analyse des sequels en fonction des notes. (Rating of movies of a same collection and of the general collection) Trends of sequels as a function of time
- **Yuansheng**: Analysis with the quality of the cast, realisator
## Timeline
Here is the corrected version of your text:
- **Week 9**: First graphs and repartition of the work, loading of the new datasets
- **Week 10**: Cleaning of the new dataset and merging of the information with the other datasets
- **Week 11**: First graphs with the new datasets
- **Week 12**: In-depth analysis of the most relevant data
- **Week 13**: Creating interactive graphs and improving the homogeneity of the project, writing of the report
- **Week 14**: Final details
## Methods

Data Exploration and Cleaning

To begin our analysis, we utilized basic functions from the pandas library to explore the initial dataset. This step allowed us to gain a comprehensive understanding of the structure, contents, and potential limitations of the data. We carefully filtered out irrelevant or incomplete entries, ensuring that only data relevant to our objectives remained for further analysis. Additionally, we cleaned the dataset by removing unnecessary columns, standardizing formats, and addressing missing values to create a robust foundation for our work.
Integration with TMDB Dataset

Next, we enriched our dataset by incorporating supplementary data from the TMDB (The Movie Database) website. Using an API key, we performed web scraping to retrieve detailed information about movie sequels, including release dates, box office performance, and production details. This additional data provided a deeper context to our analysis and was pivotal for understanding the dynamics of movie sequels.
Linking Data Sources

To connect the TMDB data to our original dataset, we used a cross-referencing method with Wikipedia. By sending targeted requests to the Wikipedia API, we were able to identify and match sequels from the TMDB dataset with their corresponding entries in our original data. This linking process created a unified dataset that paired sequels with their related metadata, enabling a cohesive analysis across all sources.
Visualization and Preliminary Analysis

With the cleaned and integrated dataset, we proceeded to visualize the data using the matplotlib library. A variety of graphs were generated to address key questions and explore the relationships within the data. These visualizations provided an initial glimpse into trends and patterns, such as the performance of sequels compared to their predecessors, release timing, and audience reception.

This structured approach ensured that our analysis was thorough and that our results were grounded in high-quality data, allowing us to derive meaningful insights from the linked datasets. 




### How to use the library

The first step that is done in results.ipynb is to load the initial movie database contained in the folder data/MovieSummaries. This allows us to assess the available data and understand the scope of movies to work with. After examining the size and quality of this data, we proceed to load additional information from a secondary database (TMDB), which contains a list of movies and their sequels. From there we combine both datasets using wikipedia id and combining both datasets. 
All the data must, however, be preprocessed beforehand using the code in ‘data_preprocessing.ipynb’; afterward, the analysis can begin with the file ‘results.ipynb



    Load the Primary Database:
        We begin by loading the primary movie database to get an initial overview of the dataset. This helps to assess the volume of data available and identify any potential gaps or areas that need further information.

    Load Sequel Metadata:
        Next, we load data from a secondary database focused on sequels. This step helps us identify which movies from the primary dataset are sequels, enabling us to analyze or filter the data accordingly.

    Combine Both Datasets:
        Finally, we merge the sequel metadata with the primary movie database, creating a comprehensive dataset that includes both general movie information and sequel identifiers. This combined dataset is ready for further analysis or processing steps.


## Project Structure

The directory structure of new project looks like this:

```
├── data                                                <- Project data files
│   │                                  
│   ├── MovieSummaries
│   │        ├─character.metadata.tsv
│   │        ├─movie.metadata.csv
│   │        ├─name.clusters.txt
│   │        ├─plot_summaries.txt
│   │        ├─README.txt
│   │        └── tvtropes.clusters.txt   
│   ├── Book
│   │        ├─book_extended_1880_2010.csv
│   │        ├─book_extended_2010_2024.csv
│   │        ├─book_metadata_1880-2010.csv
│   │        ├─book_metadata_2010_2024.csv
│   │        ├─book_with_wiki_id_1880_2010.csv
│   │        ├─book_with_wiki_id_2010_2024.csv
│   │        ├─movie_with_book_1880_2010.csv   
│   │        └─movie_with_book_2010_2024.csv 
│   ├── collections
│   │       ├─collectiion_ids.json
│   │       ├─sequels_and_original_with_wiki_id.csv
│   │       └──sequels.csv  
│   ├── comics
│   │        ├─comics_extended_1880_2010.csv
│   │        ├─comics_extended_2010_2024.csv
│   │        ├─comics_metadata_1880-2010.csv
│   │        ├─comics_metadata_2010_2024.csv
│   │        ├─comics_with_wiki_id_1880_2010.csv
│   │        ├─comics_with_wiki_id_2010_2024.csv
│   │        ├─movie_with_comics_1880_2010.csv   
│   │        └─movie_with_comics_2010_2024.csv 
│   ├── random_sample
│   │        ├─random_sample.csv
│   │        ├─random_sample_2010_2024.csv
│   │        ├─random_sample_2010_2024.csv
│   │        ├─random_sample_210_2024_extended.csv   
│   │        └─random_sample_metadata_2010_2024.csv
│   ├── remake
│   │        ├─movie_with_remake_1880_2010.csv
│   │        ├─movie_with_remake_2010_2024.csv
│   │        ├─remake_extended_1880-2010.csv
│   │        ├─remake_extened_2010_2024.csv
│   │        ├─remake_with_wiki_id_1880_2010.csv
│   │        ├─remake_with_wiki_id_2010_2024.csv
│   │        ├─remake_metatdata_1880_2010.csv   
│   │        └─remake_metadata_2010_2024.csv 
│   ├── sequels
│   │        ├─collection_ids_1880_2010.csv
│   │        ├─collection_ids_2010_2024.csv
│   │        ├─movie_with_sequels_1880-2010.csv
│   │        ├─movie_with_sequels_2010_2024.csv
│   │        ├─sequels_1880_2010.csv
│   │        ├─sequels_2010_2024.csv
│   │        ├─sequels_extended_1880_2010.csv   
│   │        ├─sequels_extended_2010_2024.csv
│   │        ├─sequels_metatdat_1880_2010.csv
│   │        ├─sequels_metadata_2010_2024.csv
│   │        └─sequels_with_wiki_id_1880_2010.csv     
│   ├── movie_sequel_tmbd.csv
│   ├── movie_with_keyword_sequel.csv
│   └── sequel_film.csv
│
├── src                                               <- Source code
│   ├── data                                          <- Data directory
│   │     ├── __pyache__
│   │     │        └──TMDB_Movies.cpython-39.pyc 
│   │     │   
│   │     └── TMBD_Movies.py                          <- Additonnal dataset                                
│   │     
│   │
│   ├── models                                        <- Model directory
│   │     ├─box_office_revenue.py                     <- all function associated to the box office revenue
│   │     ├─collection_analysis.py                    <- all function associated to the collection analysis
│   │     ├─movie_counter.py                          <- all function associated to the counting of movie
│   │     ├─movie_data_cleaner.py                     <- all function associated to display of preprocessing data
│   │     └─movie_frames.py                           <- class for movies
│   ├── utils                                         <- Utility directory
│   │     ├── __pyache__
│   │     │        └──geenral_utils.cpython-39.pyc 
│   │     ├─data_utils.py
│   │     ├─evaluation_utils.py  
│   │     └── general_utils.py                           
│   └──  scripts                                       <- Shell scripts
│
├── tests                                              <- Tests of any kind
│    ├── main.py                                       <- test about functions
│    └── test_dataloader.py                            <- Tests about load datas
│
├── data_preprocessing.ipynb                            <- preprocessing of the data
├── results.ipynb                                      <- notebook showing the results
├── .gitignore                                         <- List of files ignored by git
├── pip_requirements.txt                               <- File for installing python dependencies
└── README.md
```


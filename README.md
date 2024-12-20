
# Hollywood’s Ouroboros, or the Endless Cycle of Film Content

Website URL: [https://epfl-ada.github.io/ada-2024-project-onceuponatimeindata/](https://epfl-ada.github.io/ada-2024-project-onceuponatimeindata/)

Final notebook viewer: [insert link]

In order to create fully interactive plots, we used the [plotly.express](https://plotly.com/python/plotly-express/) library. Unfortunately, interactive plot viewing isn’t supported on GitHub. [NbViewer](https://nbviewer.org/) provides an alternative solution to view interactive plots. You can copy and paste the **permalink of the results.ipynb** or simply click on the link above.


## Abstract
Our project, explores the patterns and factors that influence the retelling of stories instead of brand new creations. We looked at movies that are sequels, book adaptations, comics adaptations and remakes. By analyzing a movie dataset, we aim to uncover what are the genres that most often lead to non-original stories, the financial incentives needed, and viewer engagement that drive sequels the be produced. We’ll investigate questions like: What is the average box office revenue for movies with sequels? How do ratings compare between original movies and their sequels? And do certain genres, like action or comedy, have a higher likelihood of spawning a series? Do sequels have a longer or shorter playing time then the originals? Through this analysis, we aim to highlight the economic and creative motivations behind sequels, and examine whether sequels generally succeed in meeting or surpassing the popularity and quality of the original or if some of them are made to maximize profit. Ultimately, our project offers insights into why the movie industry likes to reuse stories,
and which ones are most likely to be retold, while others remain single installments. It will helping movie enthusiasts understand the trends shaping the industry.


## Research Questions

- How has the prevalence of sequels, adaptations, and remakes evolved over time ?

- Do sequels and adaptations tend to generate higher average box office revenues than standalone, original films, indicating a financial incentive for producing non-original content?

- Which films, originals, sequels, or adaptations, dominate the top box office earnings, and what patterns emerge among these highest-grossing productions?

- Do later installments in a film series generally surpass the original movie in terms of box office revenue, or does the first film typically remain the most financially successful?

- Does a longer gap between installments in a franchise affect audience interest and box office performance, or do certain sequel patterns yield more sustained success over time?

- Do sequels generally improve upon or diminish the critical reception of the original film, and what factors might contribute to shifts in audience ratings across a franchise?

- How does the source of a film’s story, original, literary, comic, or previously produced, interact with its genre to influence box office revenue, and are certain adaptation types more successful in specific genres?

- What Studios produce the most sequels, remakes and adaptations and what studios are getting the best rating on those movies.


## Additional Dataset

To complete the given dataset: [CMU Movie Summary Corpus](http://www.cs.cmu.edu/~ark/personas/), we used the [TMDB dataset](https://www.themoviedb.org/). Combined with additional Wikipedia research, this allowed us to find the Wikipedia IDs of the new movies and merge all of our movie data.

## Organization within the team

- **Clara**: Analyzing the financial aspects of the movies, generating interactive plots
- **Yann**:  Generating various interactive plots, managing data structure, cleaning notebook
- **Jules**: Analyzing the global distribution of movies, managing storytelling of the datastory
- **Quentin**: Coding website structure and design
- **Yuansheng**: Cleaning notebook and coming up with plot ideas

## Timeline

- **Week 9**: First graphs and repartition of the work, loading of the new datasets
- **Week 10**: Cleaning of the new dataset and merging of the information with the other datasets
- **Week 11**: First graphs with the new datasets
- **Week 12**: In-depth analysis of the most relevant data
- **Week 13**: Creating interactive graphs and improving the homogeneity of the project, creation of the website
- **Week 14**: Final details in the notebook and designing the website while adding the results and telling the story


## Methods

Data Exploration and Cleaning

To begin our analysis, we utilized basic functions from the pandas library to explore the initial dataset. This step allowed us to gain a comprehensive understanding of the structure, contents, and potential limitations of the data. We carefully filtered out irrelevant or incomplete entries, ensuring that only data relevant to our objectives remained for further analysis. Additionally, we cleaned the dataset by removing unnecessary columns, standardizing formats, and addressing missing values to create a robust foundation for our work.

Integration with TMDB Dataset

Next, we enriched our dataset by incorporating supplementary data from the TMDB (The Movie Database) website. Using an API key, we performed web scraping to retrieve detailed information about movie sequels, including release dates, box office performance, and production details. This additional data provided a deeper context to our analysis and was pivotal for understanding the dynamics of movie sequels.

Linking Data Sources

To connect the TMDB data to our original dataset, we used a cross-referencing method with Wikipedia. By sending targeted requests to the Wikipedia API, we were able to identify and match sequels from the TMDB dataset with their corresponding entries in our original data. This linking process created a unified dataset that paired sequels with their related metadata, enabling a cohesive analysis across all sources.

Visualization and Preliminary Analysis

With the cleaned and integrated dataset, we proceeded to visualize the data using the matplotlib library. A variety of graphs were generated to address key questions and explore the relationships within the data. These visualizations provided an initial glimpse into trends and patterns, such as the performance of sequels compared to their predecessors, release timing, and audience reception.
All functions responsible for mathematical computations and subsequent plotting are centralized in the src > models directory. From there, we can simply call these functions in the final notebook.

Interactive Visualization and Deeper Analysis

Having established a solid foundation with our cleaned and integrated dataset, we now turn to interactive visualizations using the Plotly Express library. By creating dynamic, hover-enabled plots, we can dive deeper into the details of our data and uncover more nuanced insights. This approach enables a richer exploration of trends, providing a more immersive and data-driven understanding of the cinematic landscape. This will be especially useful for website users, who can see all the graph’s data in detail.


### How to use the library

The first step that is done in results.ipynb is to load the initial movie database contained in the folder data/MovieSummaries. This allows us to assess the available data and understand the scope of movies to work with. After examining the size and quality of this data, we proceed to load additional information from a secondary database (TMDB), which contains a list of movies and their sequels. From there we combine both datasets using wikipedia id and combining both datasets. 



Load the Primary Database:
We begin by loading the primary movie database to get an initial overview of the dataset. This helps to assess the volume of data available and identify any potential gaps or areas that need further information.

Load Sequel Metadata:
Next, we load data from a secondary database focused on sequels. This step helps us identify which movies from the primary dataset are sequels, enabling us to analyze or filter the data accordingly.

Combine Both Datasets:
Finally, we merge the sequel metadata with the primary movie database, creating a comprehensive dataset that includes both general movie information and sequel identifiers. This combined dataset is ready for further analysis or processing steps.




### Code structure:

├── data                                                <- Project data files
│   │                                  
│   ├── MovieSummaries			← given dataset
│   │        ├─character.metadata.tsv
│   │        ├─movie.metadata.csv
│   │        ├─name.clusters.txt
│   │        ├─plot_summaries.txt
│   │        ├─README.txt
│   │        └─ tvtropes.clusters.txt   
│   ├── MovieSummaries_filtered		← given dataset filtered by categories
│   │        ├─movie_df.csv
│   │        ├─movie_df_book.csv
│   │        ├─movie_df_comics.csv
│   │        ├─movie_df_remakes.csv
│   │        ├─movie_def_sequel_original.csv
│   │        └─movie_df_sequels.csv 
│   ├── all_sample		
│   │        ├─all_sample_2010_2024.csv
│   │        ├─all_sample_2010_2024_extended.csv
│   │        └─all_sample_2010_2024_metadata.csv 
│   ├── book
│   │        ├─book_1880_2010.csv
│   │        ├─book_1880_2010_extended.csv
│   │        ├─book_1880_2010_metadata.csv
│   │        ├─book_1880_2010_with_wiki_id.csv
│   │        ├─book_2010_2024.csv
│   │        ├─book_2010_2024_extended.csv   
│   │        └─book_2010_2024_metadata.csv 
│   ├── collections
│   │       ├─collection_ids_1880_2010.json
│   │       ├─collection_ids_2010_2024.json
│   │       ├─sequels_and_original_1880_2010.csv
│   │       ├─sequels_and_original_1880_2010_extended.csv
│   │       ├─sequels_and_original_1880_2010_with_wiki_id.csv
│   │       ├─sequel_and_original_2010_2024.csv
│   │       ├─sequels_and_original_2010_2024_extended.csv
│   │       ├─sequels_and_original_2010_2024_metadata.csv
│   │       └─sequels_and_original_2010_2024_with_wiki_id.csv
│   ├── comics
│   │        ├─comics_1880_2010.csv
│   │        ├─comics_1880_2010_extended.csv
│   │        ├─comics_1880_2010_metadata.csv
│   │        ├─comics_1880_2010_with_wiki_id.csv
│   │        ├─comics_2010_2024.csv
│   │        ├─comics_2010_2024_extended.csv  
│   │        └─comics_2010_2024_metadata.csv 
│   ├── random_sample
│   │        ├─random_sample_2010_2024.csv
│   │        ├─random_sample_210_2024_extended.csv   
│   │        └─random_sample_2010_2024_metadata.csv
│   ├── remake
│   │        ├─movie_1880_2010.csv
│   │        ├─remake_1880_2010_extended.csv
│   │        ├─remake_1880_2010_metadata.csv
│   │        ├─remake_1880_2010_with_wiki_id.csv
│   │        ├─remake_2010_2024.csv
│   │        ├─remake_2010_2024_extended.csv   
│   │        └─remake_2010_2024_metadata.csv 
│   ├── sequels
│   │        ├─sequels_1880_2010.csv
│   │        ├─sequels_1880_2010.csv
│   │        ├─sequels_1880_2010_metadata.csv
│   │        ├─sequels_1880_2010_with_wiki_id.csv
│   │        ├─sequels_2010_2024.csv
│   │        ├─sequels_2010_2024_extended.csv   
│   │        └─sequels_2010_2024_metadata.csv.csv     
│   └── inflation.csv
├── results                                                <- graphs in html                                
│   ├─average_box_office_revenue.html
│   ├─average_rating_first_vs_rest.html			
│   ├─box_office_absolute.html
│   ├─box_office_ratio.html
│   ├─budget_vs_revnue.html
│   ├─compare_first_sequel_average.html
│   ├─compare_first_sequel_total.html
│   ├─data_cleaning_graph_lost.html
│   ├─data_cleaning_graph.html
│   ├─figure_revenue_1.html
│   ├─figure_revenue_2.html
│   ├─figure_revenue_3.html
│   ├─figure_revenue_4.html
│   ├─figure_revenue_5.html
│   ├─figure_vote_1.html
│   ├─figure_vote_2.html
│   ├─figure_vote_3.html
│   ├─figure_vote_4.html
│   ├─figure_vote_5.html
│   ├─genre_heatmap_box_office.html
│   ├─genre_heatmap_rating.html
│   ├─movie_counter_figure_1880_2010.html
│   ├─movie_counter_figure_1880_2024.html
│   ├─probability_of_success.html
│   ├─race_chart.html
│   ├─ratio_movie_figure_1880_2010.html
│   ├─ratio_movie_figure_1880_2024.html
│   ├─time_between_sequels.html  
│   └─violin_chart_studio.html
│
├── src                                               <- Source code
│   ├── data                                          <- Data directory
│   │        ├── __pyache__
│   │        │            ├─TMDB_Movies.cpython-39.pyc
│   │        │            └──dataset_enhancer.cpython-39.pyc
│   │        │                           
│   │        ├─TMBD_Movies.py   			<- Additonnal dataset
│   │        └─dataset_enhancer.py                                
│   │     
│   │
│   ├── models                                        <- Model directory (all functions useful for analysis)
│   │        ├── __pyache__
│   │        │            ├─movie_data_cleaner.cpython-39.pyc
│   │        │            └─movie_frame.cpython-39.pyc
│   │        ├─box_office_revenue.py        
│   │        ├─collection_analysis.py          
│   │        ├─genre_analysis.py
│   │        ├─Models_ROI.py                
│   │        ├─movie_counter.py                
│   │        ├─movie_data_cleaner.py	      
│   │        ├─movie_frame.py  		<- class for movies
│   │        └─ratings_analysis.py
│   ├──scripts
│   │     ├──load_some_dataset_and_save_it_in_data_directory.py      <- Shell scripts
│   │
│   │                     
│   ├── utils                                         <- Utility directory
│   │     ├── __pyache__
│   │     │               ├─data_utils.cpython-39.pyc
│   │     │               ├─evaluation_utils-cpython-39.pyc
│   │     │               └─genral_utils.cpython-39.pyc 
│   │     ├─data_utils.py
│   │     ├─evaluation_utils.py  
│   │     └─general_utils.py                           
│
├── tests                                              <- Tests of any kind
│    ├── main.py                                       <- test about functions
│    └── test_dataloader.py                            <- Tests about load datas
│
├── results.ipynb                                      <- notebook of all results
├── .gitignore                                         <- List of files ignored by git
├── pip_requirements.txt                               <- File for installing python dependencies
├──report.md
├──results.ipynb
└── README.md


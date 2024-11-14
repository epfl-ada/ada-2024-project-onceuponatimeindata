# Why your favorite movie does/doesn't have a sequel
This is a template repo for your project to help you organise and document your code better. 
Please use this structure for your project and document the installation, usage and structure as below.


## Abstract
Our project, explores the patterns and factors that influence whether a movie spawns a sequel. By analyzing a movie dataset, we aim to uncover what are the genres that most often lead to sequels, the financial incentives needed, and viewer engagement that drive sequels the be produced. We’ll investigate questions like: What is the average box office revenue for movies with sequels? How do ratings compare between original movies and their sequels? And do certain genres, like action or comedy, have a higher likelihood of spawning a series? DO sequels have a longer or shorter playing time then the originals? Through this analysis, we aim to highlight the economic and creative motivations behind sequels, and examine whether sequels generally succeed in meeting or surpassing the popularity and quality of the original or if some of them are made to maximze profit. Ultimately, our project offers insights into why some stories continue, while others remain single installments, helping movie enthusiasts understand the trends shaping the industry.





## Research Questions

What genres are most likely to have sequels?

What is the average box office revenue for movies with sequels compared to standalone movies?

How do the ratings of sequels compare to the ratings of their original movies?

Does the presence of a sequel correlate with specific cast, director, or studio attributes?

What role does time between releases play in a sequel’s success?

What are the trends in sequel production over time?

What is the influence of initial audience ratings or critic reviews on the decision to produce a sequel?

Can we see a trend in the evolution of castings in sequels?


## Additional Dataset


## Methods

We plan to use following methods to deliver our results:

- Use the pandas library to shape our data the way we need it to be for further applications
- Scraping to get the the wiki id and associate to movie to a collection of sequels
- Doing statistical analysis like t-test to get evaluate correlation or linear regression 
- Also try clustering to try to find trends





## Quickstart

```bash
# clone project
git clone <project link>
cd <project repo>

# [OPTIONAL] create conda environment
conda create -n <env_name> python=3.11 or ...
conda activate <env_name>


# install requirements
pip install -r pip_requirements.txt
```



### How to use the library
Tell us how the code is arranged, any explanations goes here.
test git

The first step that is done in results.ipynb is to load the initial movie database contained in the folder data/MovieSummaries. This allows us to assess the available data and understand the scope of movies to work with. After examining the size and quality of this data, we proceed to load additional information from a secondary database, which contains a list of movies and their sequels. From there we combine both datasets using wikipedia id and combining both datasets. 



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
│   ├── collections
│   │       ├─collectiion_ids.json
│   │       ├─sequels_and_original_with_wiki_id.csv
│   │       └──sequels.csv
│   │                                  
│   ├── MovieSummaries
│   │        ├─character.metadata.tsv
│   │        ├─movie.metadata.csv
│   │        ├─name.clusters.txt
│   │        ├─plot_summaries.txt
│   │        ├─README.txt
│   │        └── tvtropes.clusters.txt       
│   ├── movie_sequel_tmbd.csv
│   ├── movie_with_keyword_sequel_with_wiki_id.csv
│   ├── movie_with_keyword_sequel.csv
│   └── sequel_film.csv
│
├── src                                               <- Source code
│   ├── data                                          <- Data directory
│   │     ├── __pyache__
│   │     │        └──TMDB_Movies.cpython-39.pyc 
│   │     │   
│   │     └── TMBD_Movies.py                                
│   │     
│   │
│   ├── models                                         <- Model directory
│   ├── utils                                          <- Utility directory
│   │     └── general_utils.py                           
│   └──  scripts                                       <- Shell scripts
│
├── tests                                              <- Tests of any kind
│    ├── main.py
│    └── test_dataloader.py                           
│
├── dat_analysis.ipynb
├── results.ipynb                                      <- notebook showing the results
├── .gitignore                                         <- List of files ignored by git
├── pip_requirements.txt                               <- File for installing python dependencies
└── README.md
```


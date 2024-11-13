from symbol import comparison

import fuzzymatcher
import numpy as np
import pandas as pd
import difflib
import cpi

import requests

import swifter
from tqdm import tqdm
from fuzzywuzzy import process

from src.data.TMDB_Movies import get_data, get_collection



if __name__ == "__main__":
    movie_df = pd.read_csv('data/MovieSummaries/movie.metadata.tsv', sep='\t', header=None)
    sequel_collections_with_wiki_id = pd.read_csv('data/collections/sequels_with_wiki_id.csv')

    movie_df.rename(columns={0: 'Wikipedia movie ID', 1: "Freebase movie ID", 2: "Movie name", 3: "Movie release date",
                             4: "Movie box office revenue", 5: "Movie runtime", 6: "Movie languages",
                             7: "Movie countries", 8: "Movie genres"}, inplace=True)

    movie_df_sequel = movie_df.join(sequel_collections_with_wiki_id.set_index('Wikipedia movie ID'), on="Wikipedia movie ID", how='inner')

    movie_df["release year"] = movie_df['Movie release date'].apply(lambda x: str(x)[:4] if str.isdigit(str(x)[:4]) else np.nan)
    movie_df["release year"] = movie_df["release year"].astype(float)

    movie_df_sequel["release year"] = movie_df_sequel["release_date"].apply(lambda x: str(x)[:4] if str.isdigit(str(x)[:4]) else np.nan)
    movie_df_sequel["release year"] = movie_df_sequel["release year"].astype(float)

    movies_per_years = movie_df.groupby("release year").count()
    movies_sequel_per_year = movie_df_sequel.groupby("release year").count()

    movies_ratio = movies_sequel_per_year["Movie name"] / movies_per_years["Movie name"]


########################################
    #correct box office inflation

    def inflate(revenue, year):
        if np.isnan(revenue) or np.isnan(year):
            return np.nan
        return cpi.inflate(revenue, year)

    movie_df["Movie box office revenue inflation adj"] = movie_df.apply(lambda x: inflate(x["Movie box office revenue"], int(x["release year"])), axis=1)
    movie_df_sequel["Movie box office revenue inflation adj"] = movie_df_sequel.apply(lambda x: cpi.inflate(movie_df_sequel["Movie box office revenue"], movie_df_sequel["release year"]), axis=1)


    box_office_per_year = movie_df.groupby("release year")["Movie box office revenue inflation adj"].agg('sum')
    box_office_sequel_per_year = movie_df_sequel.groupby("release year")["Movie box office revenue inflation adj"].agg('sum')

    box_office_ratio = (box_office_sequel_per_year / box_office_per_year).dropna()

    average_box_office = movie_df.groupby("release year")["Movie box office revenue inflation adj"].agg('mean')
    average_box_office_sequel = movie_df_sequel.groupby("release year")["Movie box office revenue inflation adj"].agg('mean')

    box_office_first_movie = movie_df_sequel.sort_values("release_date").groupby("collection").first()["Movie box office revenue inflation adj"]
    box_office_remainder = movie_df_sequel.groupby("collection")["Movie box office revenue inflation adj"].agg('sum') - box_office_first_movie
    box_office_remainder_avg = box_office_remainder / (movie_df_sequel.groupby("collection").count()["Movie name"] - 1)

########################################



    print(len(movie_df_sequel))

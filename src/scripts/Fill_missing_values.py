from src.data.TMDB_Movies import *

# Function to fill missing values in the dataset

movie_extended_df = pd.read_csv("data/collections/sequels_extended_1880_2010.csv")
movie_df_sequel_original.apply(lambda x : fill_missing_value(x, movie_extended_df[movie_extended_df["id"] == x["id"]], "Movie box office revenue","revenue"), axis=1)
print("Missing values filled for movie_df_sequel_original")

sequels_only_extended_df = pd.read_csv("data/sequels/sequels_extended.csv")
movie_df_sequel_only.apply(lambda x : fill_missing_value(x, sequels_only_extended_df[sequels_only_extended_df["id"] == x["id"]], "Movie box office revenue","revenue"), axis=1)
print("Missing values filled for movie_df_sequel_only")
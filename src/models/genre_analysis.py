import numpy as np
import pandas as pd
from netifaces import ifaddresses
from plotly import graph_objects as go
from tqdm import tqdm
import plotly.figure_factory as ff
import plotly.express as px

from utils.evaluation_utils import human_format


def get_genres(movie_frame):
    """
    Get the genres of the frames
    :param movie_frame: the movie frame
    :return: the genres
    """
    genres = {}
    movie_df = movie_frame.movie_df
    for genres_df in movie_df["Movie genres"]:
        if pd.isna(genres_df):
            continue
        list = genres_df.split(",")
        for genre in list:
            if len(genre.split("\"")) < 5:
                continue
            if genre.split("\"")[-2] not in genres:
                genres[genre.split("\"")[-2]] = 0
            genres[genre.split("\"")[-2]] += 1

    genre_df = pd.DataFrame(genres.items(), columns=["Genre", "Count"])
    return genre_df[genre_df["Count"] > 1000]


def genre_type(movie_frame, path_rating_list, debug=False):
    """
    Get the genre type of the movie
    :param movie_frame:  movie frame containing the movie data
    :param path_rating_list: the list of path to the rating
    :return: the figure with the plot
    """
    movie_frame.read_row_list(path_rating_list, "vote_average")
    genres = get_genres(movie_frame)

    box_office = "Movie box office revenue inflation adj" if not debug else "Movie box office revenue"

    split_movie_genre_list = {}
    for genre in tqdm(genres["Genre"], desc="Finding Movies fitting a genre"):
        for alternate_name, alternate_df in zip(movie_frame.get_all_alternate_df_names(), movie_frame.get_all_alternate_df()):
            if genre not in split_movie_genre_list:
                split_movie_genre_list[genre] = {}
            split_movie_genre_list[genre][alternate_name] = alternate_df[alternate_df["Movie genres"].str.contains(genre, case=False).fillna(False)]

    movie_genre_delta_df = get_value_genre_delta(box_office, movie_frame, split_movie_genre_list)

    z_box_office = movie_genre_delta_df.values
    z_text = np.array([[human_format(y) for y in x] for x in z_box_office])
    for i in range(len(z_text)):
        for j in range(len(z_text[i])):
            z_text[i][j] = "$" + z_text[i][j] if z_text[i][j][0] != "-" else "-$" + z_text[i][j][1:]

    fig_box_office = go.Figure()

    x = movie_genre_delta_df.columns.to_list()
    x = [x.replace(" ", "<br>") for x in x]
    y = movie_genre_delta_df.index.to_list()
    y = [y.replace(" ", "<br>") for y in y]
    fig_box_office.add_trace(go.Heatmap(z=z_box_office, x=x, y=y,
                                        hoverongaps=False, colorscale='sunset', colorbar=dict(title="Revenue <br>difference"),
                                        hoverinfo='text'))

    fig_box_office = fig_box_office.update_traces(text=z_text, texttemplate="%{text}")

    fig_box_office.update_layout(title=dict(text="Revenue difference between genre and all movies in millions of dollars"),
                                 xaxis_title="Kind of movies", yaxis_title="Genres")


    movie_genre_delta_rating_df = get_value_genre_delta("vote_average", movie_frame, split_movie_genre_list)

    z_rating = movie_genre_delta_rating_df.values

    x = movie_genre_delta_rating_df.columns.to_list()
    x = [x.replace(" ", "<br>") for x in x]
    y = movie_genre_delta_rating_df.index.to_list()
    y = [y.replace(" ", "<br>") for y in y]

    fig_rating = go.Figure()
    fig_rating.add_trace(go.Heatmap(z=z_rating, x=x, y=y,
                                    hoverongaps=False, colorscale='sunset', colorbar=dict(title="Rating <br>difference"),
                                    hoverinfo='text'))
    z_text = np.array([[round(y, 2) for y in x] for x in z_rating])
    fig_rating = fig_rating.update_traces(text=z_text, texttemplate="%{text}")
    fig_rating.update_layout(title=dict(text="Rating difference between genre and all movies"),
                                xaxis_title="Kind of movies", yaxis_title="Genres")


    return fig_box_office, fig_rating


def get_value_genre_delta(column, movie_frame, split_movie_genre_list):
    revenue_genre = {}
    for genre in split_movie_genre_list:
        for alternate_name in split_movie_genre_list[genre]:
            if genre not in revenue_genre:
                revenue_genre[genre] = {}
            if (len(split_movie_genre_list[genre][alternate_name].dropna(subset=column)) < 10):
                continue
            revenue_genre[genre][alternate_name] = split_movie_genre_list[genre][alternate_name][column].mean()
    movie_genre_alternate_df = pd.DataFrame.from_dict(revenue_genre).dropna(axis=1)
    movie_genre = {}
    for genre in movie_genre_alternate_df:
        movie_genre[genre] = movie_frame.movie_df[movie_frame.movie_df["Movie genres"].str.contains(genre, case=False).fillna(False)][
            column].mean()
    movie_genre_delta = {}
    for genre in movie_genre_alternate_df:
        for alternate_name in movie_genre_alternate_df.index:
            if genre not in movie_genre_delta:
                movie_genre_delta[genre] = {}
            movie_genre_delta[genre][alternate_name] = movie_genre_alternate_df[genre][alternate_name] - movie_genre[
                genre]
    movie_genre_delta_df = pd.DataFrame.from_dict(movie_genre_delta).dropna(axis=1)
    return movie_genre_delta_df


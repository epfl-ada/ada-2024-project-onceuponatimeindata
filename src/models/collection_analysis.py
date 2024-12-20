import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from pandas.io.sas.sas_constants import column_label_text_subheader_index_length

from utils.evaluation_utils import human_format

import plotly.graph_objects as go
from plotly import colors
from matplotlib import colormaps as cm

from utils.evaluation_utils import inflate


def plot_budget_vs_revenue(budget_df, box_office_revenue, collection_size):
    """
    Plot the budget vs box office revenue
    :param budget_df: dataframe with the budget for each collection
    :param box_office_revenue: dataframe with the box office revenue for each collection
    :param collection_size: number of movies in each collection
    :return: figure containing the plot
    """
    fig = go.Figure()

    text = box_office_revenue.index + "<br>Collection size: " + collection_size.apply(
        lambda x: str(x)) + "<br>Budget: " + budget_df.apply(
        human_format) + "<br>Box office revenue: " + box_office_revenue.apply(human_format)

    fig.add_trace(go.Scatter(
        x=budget_df,
        y=box_office_revenue,
        mode='markers',
        marker=dict(
            size=collection_size * 4,
            color=np.log(box_office_revenue + 1e-9),
            colorscale='sunset',
        ),
        text=budget_df.index,
        hoverinfo='text',
        hovertext=text,
        showlegend=False,
    ))

    lower_left = min(budget_df.min(), box_office_revenue.min())

    fig.add_trace(go.Scatter(x=[lower_left, 1e10], y=[lower_left, 1e10], mode='lines+text',
                             text='Return on investement',
                             line=dict(color='gray', width=2, dash='dash'),
                             textposition="top left",
                             showlegend=False))
    fig.update_layout(
        xaxis_title="Budget",
        yaxis_title="Box office revenue",
        title="Budget vs Box office revenue",
        xaxis_type="log",
        yaxis_type="log",
        yaxis=dict(
            range=[5.5, 11.5],
            tickvals=[1e6, 1e7, 1e8, 1e9, 1e10],
            ticktext=["1M", "10M", "100M", "1B", "10B"]
        ),
        xaxis=dict(
            range=[5.5, 9.5],
            tickvals=[1e6, 1e7, 1e8, 1e9, 1e10],
            ticktext=["1M", "10M", "100M", "1B", "10B"]
        )
    )

    return fig


def get_budget_vs_revenue(movie_frames, sequels_extended_file_list):
    """
    plot the budget vs box office revenue
    :param movie_frames: The MovieFrame class with the movies
    :param sequels_extended_file_list: list of files with additional budget information
    :return: the figure with the plot
    """

    collection_size = movie_frames.movie_df_sequel_original.groupby("collection").count()["Movie name"]

    # total inflation adjusted box office revenue for each collection

    box_office_name = "Movie box office revenue inflation adj" if "Movie box office revenue inflation adj" in movie_frames.movie_df_sequel_original.columns else "Movie box office revenue"
    box_office_revenue = movie_frames.movie_df_sequel_original.groupby("collection")[box_office_name].agg(
        'sum')

    movie_df_sequel_original_all = None
    for sequels_extended_file in sequels_extended_file_list:
        sequels_extended = pd.read_csv(sequels_extended_file)  # dataframe with additional budget information
        movie_df_sequel_original = pd.merge(movie_frames.movie_df_sequel_original, sequels_extended[["id", "budget"]],
                                            on="id",
                                            how="inner") if "budget" not in movie_frames.movie_df_sequel_original.columns else movie_frames.movie_df_sequel_original
        if movie_df_sequel_original_all is None:
            movie_df_sequel_original_all = movie_df_sequel_original
        else:
            movie_df_sequel_original_all = pd.concat([movie_df_sequel_original_all, movie_df_sequel_original])

    # total budget for each collection
    movie_df_sequel_original_all = movie_df_sequel_original_all.drop_duplicates(subset=["id"])
    movie_df_sequel_original_all["budget inflation adj"] = movie_df_sequel_original_all.apply(
        lambda x: inflate(x["budget"], x["release year"]), axis=1)
    budget_df = movie_df_sequel_original_all.groupby("collection")["budget inflation adj"].agg('sum')

    movie_frames.set_df("Sequels and Original", movie_df_sequel_original_all)

    # remove where bugdet is nan
    budget_df = budget_df.dropna()
    budget_df = budget_df[budget_df > 0]
    box_office_revenue = box_office_revenue.loc[budget_df.index]
    collection_size = collection_size.loc[budget_df.index]

    box_office_revenue = box_office_revenue[box_office_revenue > 0]
    box_office_revenue = box_office_revenue.dropna()
    budget_df = budget_df.loc[box_office_revenue.index]
    collection_size = collection_size.loc[box_office_revenue.index]


    fig = plot_budget_vs_revenue(budget_df, box_office_revenue, collection_size)

    return fig


def get_time(x):
    """
    Convert number of days to years, months and days
    """
    if np.isnan(x):
        return "First movie"
    if x == 0:
        return "First movie"
    years = x // 365
    months = (x % 365) // 30
    days = (x % 365) % 30
    return f"{int(years)} years {int(months)} month {int(days)} days"


def time_between_sequels_graph_plotly(collection_release_date):
    """
    Create a graph with the time between sequels
    :param collection_release_date: dataframe with the release date of the movies in the collection
    :return: figure with the graph
    """
    fig = go.Figure()

    box_office_name = "Movie box office revenue inflation adj" if "Movie box office revenue inflation adj" in collection_release_date.columns else "Movie box office revenue"

    collection_release_date = collection_release_date.sort_values(box_office_name,
                                                                  ascending=True)

    x = collection_release_date["movie date"]
    y = collection_release_date["collection"]

    text = (collection_release_date["movie title"] +
            "<br>Collection: " + collection_release_date["collection"] +
            "<br>Box office revenue: " + collection_release_date[box_office_name].apply(human_format) +
            "<br>Release year : " + collection_release_date["movie date"].apply(lambda x: str(x)[:4]) +
            "<br>Time from last: " + collection_release_date["time from last"].apply(lambda x: get_time(x)))

    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='markers',
        marker=dict(
            size=10 + collection_release_date[box_office_name].fillna(0) / pow(10, 8.5),
        ),
        text=text,
        hoverinfo='text',
        showlegend=False
    ))

    max_time = collection_release_date["time from last"].max()
    for i, movie in collection_release_date.iterrows():
        prev_year = movie["prequel date"]
        curr_year = movie["movie date"]
        collection = movie["collection"]
        prev_movie = movie["prequel name"]
        if prev_movie is not None:
            if (np.isnan(movie["time from last"])):
                color = "black"
            else:
                time = movie["time from last"]
                color = colors.sample_colorscale('sunset', 1 - np.log(time) / np.log(max_time) if time else "black")[0]

            fig.add_trace(go.Scatter(
                x=[prev_year, curr_year],
                y=[collection, collection],
                mode='lines',
                line=dict(width=2, color=color if color else 'black'),
                hoverinfo='skip',
                showlegend=False
            )
            )

    fig.update_layout(
        xaxis_title="Release date",
        yaxis_title="Collection",
        title="Time between sequels",
        yaxis=dict(
            tickvals=collection_release_date["collection"].unique(),
            ticktext=collection_release_date["collection"].unique()
        ),
        width=800,
        height=1200
    )

    return fig


def get_time_between_sequels(movie_frames):
    """
    plot the time between sequels
    :param movie_frames: The MovieFrame class with the movies
    :return: the figure with the plot
    """
    # get the first movie in each collection and the sequel movies
    first_movie = movie_frames.movie_df_sequel_original.sort_values("Movie release date").groupby("collection").first()
    sequel_movies = movie_frames.movie_df_sequel_original.sort_values("Movie release date").groupby("collection").tail(
        -1)

    box_office_name = "Movie box office revenue inflation adj" if "Movie box office revenue inflation adj" in first_movie.columns else "Movie box office revenue"

    # create a dataframe with the first movie in each collection, the release date and the box office revenue
    collection_release_date = pd.DataFrame()
    collection_release_date["collection"] = first_movie.index
    collection_release_date["movie date"] = first_movie["Movie release date"].values
    collection_release_date.loc[collection_release_date["movie date"].str.len() < 5] += "-01-01"
    collection_release_date["movie title"] = first_movie["Movie name"].values
    collection_release_date[box_office_name] = first_movie[
        box_office_name].values
    collection_release_date = collection_release_date.sort_values(box_office_name,
                                                                  ascending=False).head(50)

    # add the sequel movies to the dataframe
    sequel_temp = pd.DataFrame()
    sequel_movies_top = sequel_movies[sequel_movies["collection"].isin(collection_release_date["collection"].values)]
    sequel_temp["collection"] = sequel_movies_top["collection"].values
    sequel_temp["movie date"] = sequel_movies_top["Movie release date"].values
    sequel_temp.loc[sequel_temp["movie date"].str.len() < 5] += "-01-01"
    sequel_temp["movie title"] = sequel_movies_top["Movie name"].values
    sequel_temp[box_office_name] = sequel_movies_top[
        box_office_name].values

    collection_release_date = pd.concat([collection_release_date, sequel_temp])
    collection_release_date["movie date"] = pd.to_datetime(collection_release_date["movie date"])
    collection_release_date["collection"] = collection_release_date["collection"].apply(
        lambda x: x.replace(" Collection", ""))

    # calculate the time between sequels
    time_from_last = []
    prequel_name = []
    prequel_date = []
    collection_release_date = collection_release_date.sort_values(["collection", "movie date"])
    previous = 0
    collection_previous = ""
    movie_previous = ""
    for movie in collection_release_date.iterrows():
        collection = movie[1]["collection"]
        date = movie[1]["movie date"]
        if (collection != collection_previous):
            prequel_name.append(None)
            time_from_last.append(0)
            prequel_date.append(None)
        else:
            time_from_last.append((date - previous).days)
            prequel_name.append(movie_previous)
            prequel_date.append(previous)
        previous = date
        collection_previous = collection
        movie_previous = movie[1]["movie title"]

    # add the time between sequels to the dataframe
    collection_release_date["time from last"] = time_from_last
    collection_release_date["prequel name"] = prequel_name
    collection_release_date["prequel date"] = prequel_date
    collection_release_date = collection_release_date[
        collection_release_date.groupby("collection").collection.transform(len) > 1]

    # fig = time_between_sequels_graph(collection_release_date)
    fig1 = time_between_sequels_graph_plotly(collection_release_date)
    return fig1

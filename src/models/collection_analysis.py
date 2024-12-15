import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

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
    fig.add_trace(go.Scatter(
        x=budget_df,
        y=box_office_revenue,
        mode='markers',
        marker=dict(
            size=collection_size * 5,
            color=box_office_revenue,
            colorscale='deep',
            showscale=True
        ),
        text = budget_df.index,
        hoverinfo='text'
    ))

    lower_left = min(budget_df.min(), box_office_revenue.min())

    fig.add_trace(go.Scatter(x = [lower_left, 1e9], y = [lower_left, 1e9], mode='lines+text',
                             text='Return on investement',
                             line=dict(color='gray', width=2, dash='dash'),
                                textposition="top left"))
    fig.update_layout(
        xaxis_title="Budget",
        yaxis_title="Box office revenue",
        title="Budget vs Box office revenue",
        xaxis_type="log",
        yaxis_type="log",
        yaxis=dict(
            range = [5.5, 10.5],
            tickvals=[1e6, 1e7, 1e8, 1e9, 1e10],
            ticktext=["1M", "10M", "100M", "1B", "10B"]
        ),
        xaxis=dict(
            range = [5.5, 9],
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

    box_office_revenue = movie_frames.movie_df_sequel_original.groupby("collection")["Movie box office revenue"].agg(
        'sum')

    movie_df_sequel_original_all = None
    for sequels_extended_file in sequels_extended_file_list:
        sequels_extended = pd.read_csv(sequels_extended_file)  # dataframe with additional budget information
        movie_df_sequel_original = pd.merge(movie_frames.movie_df_sequel_original, sequels_extended[["id", "budget"]],
                                            on="id", how="inner")  if "budget" not in movie_frames.movie_df_sequel_original.columns \
                                                                   else movie_frames.movie_df_sequel_original
        if movie_df_sequel_original_all is None:
            movie_df_sequel_original_all = movie_df_sequel_original
        else:
            movie_df_sequel_original_all = pd.concat([movie_df_sequel_original_all, movie_df_sequel_original])


    # total budget for each collection

    movie_df_sequel_original_all["budget inflation adj"] = movie_df_sequel_original_all.swifter.apply(
        lambda x: inflate(x["budget"], x["release_date"]), axis=1)
    budget_df = movie_df_sequel_original_all.groupby("collection")["budget inflation adj"].agg('sum')

    #remove where bugdet is nan
    budget_df = budget_df.dropna()
    box_office_revenue = box_office_revenue.loc[budget_df.index]
    collection_size = collection_size.loc[budget_df.index]

    fig = plot_budget_vs_revenue(budget_df, box_office_revenue, collection_size)

    return fig

def time_between_sequels_graph_plotly(collection_release_date):
    """
    Create a graph with the time between sequels
    :param collection_release_date: dataframe with the release date of the movies in the collection
    :return: figure with the graph
    """
    fig = go.Figure()

    collection_release_date = collection_release_date.sort_values("Movie box office revenue",
                                                                  ascending=True)

    x = collection_release_date["movie date"]
    y = collection_release_date["collection"]

    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='markers',
        marker=dict(
            size=10 + collection_release_date["Movie box office revenue"].fillna(0) / pow(10, 8.5),
        ),
        text=collection_release_date["movie title"],
        hoverinfo='text',
        showlegend=False
    ))

    for i, movie in collection_release_date.iterrows():
        prev_year = movie["prequel date"]
        curr_year = movie["movie date"]
        collection = movie["collection"]
        prev_movie = movie["prequel name"]
        if prev_movie is not None:
            if(np.isnan(movie["time from last"])):
                color = "black"
            else :
                color = colors.sample_colorscale('inferno',
                                             1 - movie["time from last"] / collection_release_date["time from last"].max())[0] if movie["time from last"] else "black"

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

def time_between_sequels_graph(collection_release_date):
    """
    Create a graph with the time between sequels
    :param collection_release_date: dataframe with the release date of the movies in the collection
    :return: figure with the graph
    """
    fig = plt.figure(figsize=(20, 20))
    ax = fig.add_subplot(221)

    collection_release_date = collection_release_date.sort_values("Movie box office revenue",
                                                                  ascending=True)
    x = collection_release_date["movie date"]
    y = collection_release_date["collection"]

    # scatter plot of release date vs collection, with the size of the point representing the box office revenue of the movie
    ax.scatter(x, y, s=10 + collection_release_date["Movie box office revenue"].fillna(0) / 10000000,
               alpha=0.5)

    # Plot the lines between the sequels, and color according to time elapsed
    x_line, y_line = np.array([]), np.array([])

    max_time = collection_release_date["time from last"].max()

    time = collection_release_date["time from last"].values
    time = time[time != 0]

    color = cm.get_cmap("plasma")(np.linspace(0, 1, num=time.shape[0]))

    collection_release_date = collection_release_date.sort_values("time from last")
    j = 0
    for i, movie in collection_release_date.iterrows():
        prev_year = movie["prequel date"]
        curr_year = movie["movie date"]
        collection = movie["collection"]
        prev_movie = movie["prequel name"]
        if prev_movie is not None:
            x_line = np.append(x_line, [prev_year, curr_year])
            y_line = np.append(y_line, [collection, collection])
            ax.plot([prev_year, curr_year], [collection, collection], alpha=0.5, c=color[j], linewidth=2)
            j += 1

    ax.set_xlabel("Release date")
    ax.set_ylabel("Collection")
    ax.title.set_text("Time between sequels")
    plt.rc('ytick', labelsize=8)
    return fig

def get_time_between_sequels(movie_frames):
    """
    plot the time between sequels
    :param movie_frames: The MovieFrame class with the movies
    :return: the figure with the plot
    """
    # get the first movie in each collection and the sequel movies
    first_movie = movie_frames.movie_df_sequel_original.sort_values("release_date").groupby("collection").first()
    sequel_movies = movie_frames.movie_df_sequel_original.sort_values("release_date").groupby("collection").tail(-1)

    # create a dataframe with the first movie in each collection, the release date and the box office revenue
    collection_release_date = pd.DataFrame()
    collection_release_date["collection"] = first_movie.index
    collection_release_date["movie date"] = first_movie["release_date"].values
    collection_release_date["movie title"] = first_movie["Movie name"].values
    collection_release_date["Movie box office revenue"] = first_movie[
        "Movie box office revenue"].values
    collection_release_date = collection_release_date.sort_values("Movie box office revenue",
                                                                  ascending=False).head(50)

    # add the sequel movies to the dataframe
    sequel_temp = pd.DataFrame()
    sequel_movies_top = sequel_movies[sequel_movies["collection"].isin(collection_release_date["collection"].values)]
    sequel_temp["collection"] = sequel_movies_top["collection"].values
    sequel_temp["movie date"] = sequel_movies_top["release_date"].values
    sequel_temp["movie title"] = sequel_movies_top["Movie name"].values
    sequel_temp["Movie box office revenue"] = sequel_movies_top[
        "Movie box office revenue"].values

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

    #fig = time_between_sequels_graph(collection_release_date)
    fig1 = time_between_sequels_graph_plotly(collection_release_date)
    return  fig1
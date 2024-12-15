#import cpi
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from networkx.algorithms.bipartite.basic import color
from plotly import graph_objects as go

from utils.evaluation_utils import human_format


def comupute_graph_box_office_absolute(box_office_per_year, box_office_compared_per_year_list, names):
    """
    Plot the box office revenue per year
    :param box_office_per_year: box office revenue per year
    :param box_office_compared_per_year: box office revenue per year for movies with sequels
    :return: the figure with the plot
    """
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=box_office_per_year.index, y=box_office_per_year, mode='lines', name='Box office revenue of all movies'))

    for box_office_compared_per_year, name in zip(box_office_compared_per_year_list,names):
        fig.add_trace(go.Scatter(x=box_office_compared_per_year.index, y=box_office_compared_per_year, mode='lines',
                                 name=f'Box office revenue of {name.lower()}'))

    fig.update_layout(
        title='Box office revenue per year',
        xaxis_title='Year',
        yaxis_title='Box office revenue',
        yaxis=dict(tickformat='$.2s'),  # Format y-axis with scientific notation
        legend=dict(x=0, y=1)
    )

    return fig


def compute_box_office_ratio_graph(box_office_per_year, box_office_sequel_per_year_list, names):
    """
    Plot the box office revenue percentage per year
    :param box_office_per_year: box office revenue per year
    :param box_office_sequel_per_year_list: box office revenue per year for movies
    :param names: type of movies
    :return: the figure with the plot
    """
    fig = go.Figure()

    for box_office_sequel_per_year, name in zip(box_office_sequel_per_year_list, names):
        fig.add_trace(go.Scatter(x=box_office_sequel_per_year.index, y=box_office_sequel_per_year, mode='lines',
                                    name=f'Ratio of the box office taken by {name.lower()}'))
    fig.update_layout(
        title="Box office revenue percentage",
        xaxis_title="Year",
        yaxis_title="Percentage (%)",
        legend=dict(x=0, y=1)
    )

    return fig


def get_box_office_ratio(movie_frames):
    """
    Calculate the box office revenue percentage per year
    :param movie_frames: The MovieFrame class with the movies
    :return: the figure with the plot
    """
    movie_frames.drop_impossible_years()
    # sum of the box office revenue per year for all movies
    box_office_per_year = movie_frames.movie_df.groupby("release year")["Movie box office revenue inflation adj"].agg(
        'sum')
    box_office_per_year = box_office_per_year.fillna(0)

    box_office_sequel_per_year_list = []


    for df in movie_frames.get_all_alternate_df():
        bo = df.groupby("release year")["Movie box office revenue inflation adj"].agg('sum').fillna(0)
        bo = bo / box_office_per_year * 100
        bo = bo.fillna(0)
        box_office_sequel_per_year_list.append(bo)


    # calculate the percentage of box office revenue from movies with sequels

    # Plot figure 5: box office revenue percentage per year

    fig = compute_box_office_ratio_graph(box_office_per_year, box_office_sequel_per_year_list, movie_frames.get_all_alternate_df_names())


    return fig

def compute_average_box_office_revenue_graph(average_box_office, average_box_office_alternate, names):
    """
    Plot the average box office revenue per year
    :param average_box_office: average box office revenue per year
    :param average_box_office_alternate: average box office revenue per year for movies with sequels
    :return:
    """

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=average_box_office.index, y=average_box_office, mode='lines', name='Average box office revenue of all movies'))
    for average_box_office_alternate, name in zip(average_box_office_alternate, names):
        fig.add_trace(go.Scatter(x=average_box_office_alternate.index, y=average_box_office_alternate, mode='lines',
                                 name=f'Average box office revenue {name.lower()}'))

    fig.update_layout(
        title='Average Box Office Revenue per Year',
        xaxis_title='Year',
        yaxis_title='Revenue',
        yaxis=dict(tickformat='$.2s'),  # Format y-axis with scientific notation
        legend=dict(x=0, y=1.1)
    )

    return fig


def get_average_box_office_revenue(movie_frames):
    """
    Calculate the average box office revenue per year
    :param movie_frames: the database with the movies
    :return: the figure with the plot
    """

    average_box_office = movie_frames.movie_df.groupby("release year")["Movie box office revenue inflation adj"].agg('mean')
    average_box_office = average_box_office.fillna(0)

    # calculate box office revenue per movie for movies with sequels and fill NaN values with 0


    average_box_office_list = []
    for df in movie_frames.get_all_alternate_df():
        df_avg = df.groupby("release year")["Movie box office revenue inflation adj"].agg('mean').fillna(0)
        #remove when only one movie has box office revenue
        average_box_office_list.append(df_avg)



    fig = compute_average_box_office_revenue_graph(average_box_office, average_box_office_list, movie_frames.get_all_alternate_df_names())

    return fig


def get_box_office_absolute(movie_frames):
    """
    Calculate the box office revenue per year
    :param movie_frames: the database with the movies
    :return: the figure with the plot
    """
    movie_frames.drop_impossible_years()
    # inflation adjustement of the box office revenue

    # add the inflation adjusted box office revenue to the dataframes

    # sum of the box office revenue per year, first for all movies, then for movies with sequels # inflation adj
    box_office_per_year = movie_frames.movie_df.groupby("release year")["Movie box office revenue inflation adj"].agg('sum')
    box_office_per_year_list = []
    names = movie_frames.get_all_alternate_df_names()
    for df in movie_frames.get_all_alternate_df():
        box_office_per_year_list.append(df.groupby("release year")["Movie box office revenue inflation adj"].agg('sum').fillna(0))

    # replace NaN values by 0

    box_office_per_year = box_office_per_year.fillna(0)

    fig = comupute_graph_box_office_absolute(box_office_per_year, box_office_per_year_list, names)
    return fig

def get_compare_first_sequel_graph_plotly(first_vs_rest, average_movie_revenue):
    """
    Plot the comparison between the box office revenue of the first movie and the sequel movie
    :param first_vs_rest:  dataframe with the box office revenue of the first movie and the sequel movie
    :param average_movie_revenue: average box office revenue for all movies
    :return: the figure with the plot
    """

    fig_total = go.Figure()

    x = first_vs_rest["index"]
    y1 = first_vs_rest["first"]
    y2 = first_vs_rest["rest"]

    text_first = first_vs_rest.index + "<br>First movie box office revenue: " + y1.apply(human_format)
    text_sequel = first_vs_rest.index + "<br>Sequel movie box office revenue: " + y2.apply(human_format)

    fig_total.add_trace(go.Scatter(x=x, y=y1, mode='markers', name=f"First movie <br>box office revenue",
                             text=text_first, marker_color = 'blue', hoverinfo="text"))
    fig_total.add_trace(go.Scatter(x=x, y=y2, mode='markers', name="Sequel movie <br>box office revenue",
                             text=text_sequel, marker_color = "lightblue",hoverinfo="text"))


    for i in range(len(x)):
        if y1[i] > y2[i]:
            fig_total.add_shape(type="line", x0=x[i], x1=x[i], y0=y1[i], y1=y2[i], line=dict(color="red", width=1))
        else:
            fig_total.add_shape(type="line", x0=x[i], x1=x[i], y0=y1[i], y1=y2[i], line=dict(color="green", width=1))

    fig_total.update_layout(
        title="First movie vs Box office revenue of all sequels",
        xaxis_title="Collection",
        yaxis_title="Box office revenue",
        yaxis_type="log",
        width=1000,
        height=600
    )

    fig_avg = go.Figure()
    x = first_vs_rest["index"]
    y1 = first_vs_rest["first"]
    y2 = first_vs_rest["rest_avg"]

    text_first = first_vs_rest.index + "<br>First movie box office revenue: " + y1.apply(human_format)
    text_sequel = first_vs_rest.index + "<br>Average sequel movie box office revenue: " + y2.apply(human_format)

    fig_avg.add_trace(go.Scatter(x=x, y=y1, mode='markers', name=f"First movie <br>box office revenue",
                                text=text_first, marker_color = 'blue', hoverinfo="text"))
    fig_avg.add_trace(go.Scatter(x=x, y=y2, mode='markers', name="Average sequel movie <br>box office revenue",
                                text=text_sequel, marker_color = "lightblue",hoverinfo="text"))

    for i in range(len(x)):
        if y1[i] > y2[i]:
            fig_avg.add_shape(type="line", x0=x[i], x1=x[i], y0=y1[i], y1=y2[i], line=dict(color="red", width=1))
        else:
            fig_avg.add_shape(type="line", x0=x[i], x1=x[i], y0=y1[i], y1=y2[i], line=dict(color="green", width=1))

    fig_avg.add_hline(y=average_movie_revenue, line_dash="dot", line_color="yellow", name="Average movie box office revenue")

    fig_avg.update_layout(
        title="First movie vs Average sequel movie box office revenue",
        xaxis_title="Collection",
        yaxis_title="Box office revenue",
        yaxis_type="log",
        width=1000,
        height=600
    )
    return fig_total, fig_avg

def compare_first_sequel(movie_frame):
    """
    compare the box office revenue of the first movie and the sequel movie
    :param movie_frames: the database with the movies
    :return: the figure with the plot
    """

    box_office_first_movie = movie_frame.movie_df_sequel_original.sort_values("release_date").groupby("collection").first()[
        "Movie box office revenue inflation adj"]

    # calculate the remaining box office revenue for each collection # inflation adj

    box_office_remainder = movie_frame.movie_df_sequel_original.groupby("collection")["Movie box office revenue inflation adj"].agg(
        'sum') - box_office_first_movie

    # calculate the remaining box office revenue for each collection (excluding the first movie)

    box_office_remainder_avg = box_office_remainder / (
                movie_frame.movie_df_sequel_original.groupby("collection").count()["Movie name"] - 1)

    first_vs_rest = pd.DataFrame()
    first_vs_rest["first"] = box_office_first_movie
    first_vs_rest["rest"] = box_office_remainder
    first_vs_rest["rest_avg"] = box_office_remainder_avg

    first_vs_rest = first_vs_rest[first_vs_rest["rest"] > 0]  # remove collections with no revenue
    first_vs_rest = first_vs_rest.sort_values("first",
                                              ascending=True)  # sort in ascending order for the first movie (lowest to the highest)
    first_vs_rest['index'] = range(0, len(first_vs_rest))

    average_movie_revenue = movie_frame.movie_df.dropna(subset=['Movie box office revenue inflation adj'])[
        "Movie box office revenue inflation adj"].agg('mean')

    fig_total, fig_avg = get_compare_first_sequel_graph_plotly(first_vs_rest, average_movie_revenue)
    return fig_total, fig_avg
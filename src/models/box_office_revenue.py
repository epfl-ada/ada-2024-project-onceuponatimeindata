#import cpi
import numpy as np
import pandas as pd
from plotly import graph_objects as go


def inflate(revenue, year):
    """
    Adjust the revenue for inflation
    :param revenue: revenue to adjust
    :param year: the year of the revenue
    :return: the inflation adjusted revenue
    """
    if np.isnan(revenue) or np.isnan(year) or year < 1900:  #no inflation adjustement for missing values or years before 1900
        return np.nan
    if len(str(year)) != 4:
        year = int(str(year)[:4])
    return cpi.inflate(revenue, year)                       #apply Consumer Price Index (cpi) inflation adjustement

def comupute_graph_box_office_absolute(box_office_per_year, box_office_compared_per_year_list):
    """
    Plot the box office revenue per year
    :param box_office_per_year: box office revenue per year
    :param box_office_compared_per_year: box office revenue per year for movies with sequels
    :return: the figure with the plot
    """
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=box_office_per_year.index, y=box_office_per_year, mode='lines', name='Box office revenue'))

    for box_office_compared_per_year in box_office_compared_per_year_list:
        fig.add_trace(go.Scatter(x=box_office_compared_per_year.index, y=box_office_compared_per_year, mode='lines',
                                 name='Box office revenue sequel'))

    fig.update_layout(
        title='Box office revenue per year',
        xaxis_title='Year',
        yaxis_title='Box office revenue',
        yaxis=dict(tickformat='$.2s'),  # Format y-axis with scientific notation
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
    # sum of the box office revenue per year, first for all movies, then for movies with sequels
    box_office_per_year = movie_frames.movie_df.groupby("release year")["Movie box office revenue inflation adj"].agg(
        'sum')
    box_office_sequel_per_year = movie_frames.movie_df_sequel_only.groupby("release year")[
        "Movie box office revenue inflation adj"].agg('sum')

    # replace NaN values by 0

    box_office_per_year = box_office_per_year.fillna(0)
    box_office_sequel_per_year = box_office_sequel_per_year.fillna(0)

    # calculate the percentage of box office revenue from movies with sequels

    box_office_percentage = box_office_sequel_per_year / box_office_per_year * 100

    # Plot figure 5: box office revenue percentage per year

    box_office_percentage_plot, ax = plt.subplots()
    ax.bar(box_office_percentage.index, box_office_percentage, label="Box office revenue percentage", width=1)
    ax.legend(loc='upper left')
    ax.title.set_text("Box office revenue percentage from 1970")
    ax.set_xlabel("Year")
    ax.set_ylabel("Percentage (%)")
    return box_office_percentage_plot

def compute_average_box_office_revenue_graph(average_box_office, average_box_office_alternate):
    """
    Plot the average box office revenue per year
    :param average_box_office: average box office revenue per year
    :param average_box_office_alternate: average box office revenue per year for movies with sequels
    :return:
    """

    average_box_office_plot, ax = plt.subplots()
    ax.plot(average_box_office.index, average_box_office, label="Average box office revenue")
    ax.plot(average_box_office_alternate.index, average_box_office_alternate, label="Average box office revenue sequel")

    plt.draw()  # Draw the plot to get the current y-axis offset
    y_axis_offset = ax.get_yaxis().get_offset_text().get_text()  # get the scientific notation multiplier from the axis and use it in the label
    ax.set_ylabel(f"Revenue [{y_axis_offset}$]")
    ax.get_yaxis().get_offset_text().set_visible(
        False)  # remove the scientific notation from the axis to avoid duplication
    ax.legend()
    ax.set_title("Average Box Office Revenue per Year")

    return average_box_office_plot


def get_average_box_office_revenue(movie_frames):
    """
    Calculate the average box office revenue per year
    :param movie_frames: the database with the movies
    :return: the figure with the plot
    """

    average_box_office = movie_frames.movie_df.dropna(subset=['Movie box office revenue inflation adj']).groupby("release year")[
        "Movie box office revenue inflation adj"].agg('mean')
    average_box_office = average_box_office.fillna(0)

    # calculate box office revenue per movie for movies with sequels and fill NaN values with 0

    average_box_office_sequel = movie_frames.movie_df_sequel_only.dropna(subset=['Movie box office revenue inflation adj']).groupby("release year")[
        "Movie box office revenue inflation adj"].agg('mean')
    average_box_office_sequel = average_box_office_sequel.fillna(0)

    fig = compute_average_box_office_revenue_graph(average_box_office, average_box_office_sequel)

    return fig


def get_box_office_absolute(movie_frames):
    """
    Calculate the box office revenue per year
    :param movie_frames: the database with the movies
    :return: the figure with the plot
    """
    movie_frames.drop_impossible_years()
    # inflation adjustement of the box office revenue
    movie_df_inflation_adj = movie_frames.movie_df.apply(
        lambda x: inflate(x["Movie box office revenue"], x["release year"]), axis = 1)
    sequel_df_inflation_adj = movie_frames.movie_df_sequel_only.apply(
        lambda x: inflate(x["Movie box office revenue"], x["release year"]), axis = 1)
    sequel_and_original_df_inflation_adj = movie_frames.movie_df_sequel_original.apply(
        lambda x: inflate(x["Movie box office revenue"], x["release year"]), axis = 1)


    # add the inflation adjusted box office revenue to the dataframes
    movie_frames.add_column("movie_df", "Movie box office revenue inflation adj", movie_df_inflation_adj)
    movie_frames.add_column("movie_df_sequel_only", "Movie box office revenue inflation adj", sequel_df_inflation_adj)
    movie_frames.add_column("movie_df_sequel_original", "Movie box office revenue inflation adj", sequel_and_original_df_inflation_adj)


    # sum of the box office revenue per year, first for all movies, then for movies with sequels
    box_office_per_year = movie_frames.movie_df.groupby("release year")["Movie box office revenue inflation adj"].agg('sum')
    box_office_sequel_per_year = movie_frames.movie_df_sequel_only.groupby("release year")[
        "Movie box office revenue inflation adj"].agg('sum')

    # replace NaN values by 0

    box_office_per_year = box_office_per_year.fillna(0)
    box_office_sequel_per_year = box_office_sequel_per_year.fillna(0)

    fig = comupute_graph_box_office_absolute(box_office_per_year, box_office_sequel_per_year)
    return fig

def get_compare_first_sequel_graph(first_vs_rest, average_movie_revenue):
    """
    Plot the comparison between the box office revenue of the first movie and the sequel movie
    :param first_vs_rest:  dataframe with the box office revenue of the first movie and the sequel movie
    :param average_movie_revenue: average box office revenue for all movies
    :return: the figure with the plot
    """

    fig = plt.figure(figsize=(10, 10))
    ax1 = fig.add_subplot(221)
    x = first_vs_rest["index"]
    y1 = first_vs_rest["first"]
    y2 = first_vs_rest["rest"]
    ax1.plot(x, y1, 'ks', markersize=4, label="First movie box office revenue")
    ax1.plot(x, y2, 'bo', markersize=4, label="Sequel movie box office revenue")

    ax1.plot((x[y1 > y2], x[y1 > y2]), (y1[y1 > y2], y2[y1 > y2]), c="red",
             alpha=0.5)  # the first movie has a lower revenue than the sequel
    ax1.plot((x[y1 < y2], x[y1 < y2]), (y1[y1 < y2], y2[y1 < y2]), c="green",
             alpha=0.5)  # the first movie has a higher revenue than the sequel

    ax1.legend()
    ax1.title.set_text("First movie vs Sequel movie box office revenue")
    ax1.set_xlabel("Collection")
    ax1.set_ylabel("Box office revenue")
    ax1.set_yscale("log")

    # Plot figure 8: first movie vs average sequel movie box office revenue

    ax2 = fig.add_subplot(222)
    x = first_vs_rest["index"]
    y1 = first_vs_rest["first"]
    y2 = first_vs_rest["rest_avg"]
    ax2.plot(x, y1, 'ks', markersize=4, label="First movie box office revenue")
    ax2.plot(x, y2, 'bo', markersize=4, label="Sequel movie box office revenue average")

    ax2.plot((x[y1 > y2], x[y1 > y2]), (y1[y1 > y2], y2[y1 > y2]), c="red",
             alpha=0.5)  # the first movie has a lower revenue than the average sequel
    ax2.plot((x[y1 < y2], x[y1 < y2]), (y1[y1 < y2], y2[y1 < y2]), c="green",
             alpha=0.5)  # the first movie has a higher revenue than the average sequel
    ax2.axhline(y=average_movie_revenue, color='y', linestyle='-',
                label="Average movie box office revenue")  # average revenue for all movies

    ax2.legend()
    ax2.title.set_text("First movie box vs average Sequel movie box office revenue")
    ax2.set_xlabel("Collection")
    ax2.set_ylabel("Box office revenue")
    ax2.set_yscale("log")

    return fig

def compare_first_sequel(movie_frame):
    """
    compare the box office revenue of the first movie and the sequel movie
    :param movie_frames: the database with the movies
    :return: the figure with the plot
    """

    box_office_first_movie = movie_frame.movie_df_sequel_original.sort_values("release_date").groupby("collection").first()[
        "Movie box office revenue inflation adj"]

    # calculate the remaining box office revenue for each collection

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

    fig = get_compare_first_sequel_graph(first_vs_rest, average_movie_revenue)
    return fig
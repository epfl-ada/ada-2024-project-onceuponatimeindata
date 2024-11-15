import cpi
import numpy as np
from matplotlib import pyplot as plt


def inflate(revenue, year):
    if np.isnan(revenue) or np.isnan(year) or year < 1900:  #no inflation adjustement for missing values or years before 1900
        return np.nan
    if len(str(year)) != 4:
        year = int(str(year)[:4])
    return cpi.inflate(revenue, year)                       #apply Consumer Price Index (cpi) inflation adjustement

def comupute_graph_box_office_absolute(box_office_per_year, box_office_compared_per_year):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(box_office_per_year.index, box_office_per_year, label="Box office revenue")
    ax.plot(box_office_compared_per_year.index, box_office_compared_per_year, label="Box office revenue sequel")

    plt.draw()  # Draw the plot to get the current y-axis offset
    y_axis_offset = ax.get_yaxis().get_offset_text().get_text()  # get the scientific notation multiplier from the axis and use it in the label
    ax.set_ylabel(f"Box office revenue [{y_axis_offset}$]")
    ax.get_yaxis().get_offset_text().set_visible(
        False)  # remove the scientific notation from the axis to avoid duplication
    ax.legend()
    ax.set_title("Box office revenue per year")
    ax.set_xlabel("Year")

    return fig

def get_box_office_absolute(movieframes):

    # inflation adjustement of the box office revenue
    movie_df_inflation_adj = movieframes.movie_df["Movie box office revenue"].apply(
        lambda x: inflate(x, movieframes.movie_df["release year"]), axis=1)
    sequel_df_inflation_adj = movieframes.movie_df_sequel_only["Movie box office revenue"].apply(
        lambda x: inflate(x, movieframes.movie_df_sequel_only["release year"]), axis=1)
    seque_and_original_df_inflation_adj = movieframes.movie_df_sequel_original["Movie box office revenue"].apply(
        lambda x: inflate(x, movieframes.movie_df_sequel_original["release year"]), axis=1)

    # add the inflation adjusted box office revenue to the dataframes
    movieframes.add_column(movieframes.movie_df, "Movie box office revenue inflation adj", movie_df_inflation_adj)
    movieframes.add_column(movieframes.movie_df_sequel_only, "Movie box office revenue inflation adj", sequel_df_inflation_adj)
    movieframes.add_column(movieframes.movie_df_sequel_original, "Movie box office revenue inflation adj", seque_and_original_df_inflation_adj)


    # sum of the box office revenue per year, first for all movies, then for movies with sequels
    box_office_per_year = movieframes.movie_df.groupby("release year")["Movie box office revenue inflation adj"].agg('sum')
    box_office_sequel_per_year = movieframes.movie_df_sequel_only.groupby("release year")[
        "Movie box office revenue inflation adj"].agg('sum')

    # replace NaN values by 0

    box_office_per_year = box_office_per_year.fillna(0)
    box_office_sequel_per_year = box_office_sequel_per_year.fillna(0)

    fig = comupute_graph_box_office_absolute(box_office_per_year, box_office_sequel_per_year)
    return fig
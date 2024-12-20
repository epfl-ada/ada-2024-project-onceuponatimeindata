import pandas as pd
from plotly import graph_objects as go
import numpy as np
from utils.evaluation_utils import human_format
import plotly.express as px

from src.utils.evaluation_utils import human_format
from scipy.stats import ttest_ind,mannwhitneyu,kstest

import plotly.io as pio


def compute_graph_box_office_absolute(box_office_per_year, box_office_compared_per_year_list, names, sum_all, get_colors = None):
    """
    Plot the box office revenue per year
    :param box_office_per_year: box office revenue per year
    :param box_office_compared_per_year_list: box office revenue per year for movies
    :param names: type of movies
    :param sum_all: sum of the box office revenue of all non-original movies
    :param get_colors: function to get the color of the line
    :return: the figure with the plot
    """
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=box_office_per_year.index, y=box_office_per_year, mode='lines', name='Box office revenue of all movies', line = dict(color=get_colors("Movies"))))

    for box_office_compared_per_year, name in zip(box_office_compared_per_year_list,names):
        fig.add_trace(go.Scatter(x=box_office_compared_per_year.index, y=box_office_compared_per_year, mode='lines', line = dict(color = get_colors(name)),
                                 name=f'Box office revenue of {name.lower()}'))

    fig.add_trace(go.Scatter(x=sum_all.index, y=sum_all, mode='lines',
                             name='Sum of box office revenue of all non-original movies', line=dict(color=get_colors("all"), width=2)))


    fig.add_annotation(
        text = "We see the huge impact<br>of Gone with the Wind in 1939",
        x = 1939,
        y = box_office_per_year.loc[1939],
        showarrow = True,
        arrowhead = 1
    )

    fig.add_annotation(
        text = "We see the impact of<br>2001: A Space Odyssey in 1968",
        x = 1968,
        y = box_office_per_year.loc[1968],
        showarrow = True,
        arrowhead = 1
    )

    fig.add_annotation(
        text = "Covid made a<br>huge impact in 2020",
        x = 2020,
        y = box_office_per_year.loc[2020],
        showarrow = True,
        arrowhead = 1
    )


    fig.update_layout(
        title='Box office revenue per year',
        xaxis_title='Year',
        yaxis_title='Box office revenue',
        yaxis=dict(tickformat='$.2s'),  # Format y-axis with scientific notation
        legend=dict(x=0, y=1)
    )

    return fig


def compute_box_office_ratio_graph(box_office_per_year, box_office_adaptation_per_year_list, names, sum_all, get_colors = None):
    """
    Plot the box office revenue percentage per year
    :param box_office_per_year: box office revenue per year
    :param box_office_adaptation_per_year_list: box office revenue per year for movies
    :param names: type of movies
    :param sum_all: sum of the box office revenue of all non-original movies
    :param get_colors: function to get the color of the line
    :return: the figure with the plot
    """
    fig = go.Figure()

    for box_office_sequel_per_year, name in zip(box_office_adaptation_per_year_list, names):
        fig.add_trace(go.Scatter(x=box_office_sequel_per_year.index, y=box_office_sequel_per_year, mode='lines', line = dict(color = get_colors(name)),
                                    name=f'Ratio of the box office taken by {name.lower()}'))

    fig.add_trace(go.Scatter(x=sum_all.index, y=sum_all, mode='lines',
                                name='Sum of box office revenue of all non-original movies', line=dict(color=get_colors("all"), width=2)))

    fig.update_layout(
        title="Box office revenue percentage",
        xaxis_title="Year",
        yaxis_title="Percentage (%)",
        legend=dict(x=0, y=1)
    )

    fig.add_annotation(
        text = "We see the huge impact<br>of Gone with the Wind in 1939",
        x = 1939,
        y = sum_all.loc[1939],
        showarrow = True,
        arrowhead = 1
    )

    fig.add_annotation(
        text = "We see the impact of<br>Ben-Hur in 1959",
        x = 1959,
        y = sum_all.loc[1959],
        showarrow = True,
        arrowhead = 1
    )

    fig.add_annotation(
        text = "Mary Poppins and Goldfinger",
        x = 1964,
        y = sum_all.loc[1964],
        showarrow = True,
        arrowhead = 1,
        ax = 40,  # Adjust this value to change the angle
        ay = -40  # Adjust this value to change the angle
    )

    fig.add_annotation(
        text = "Jaws",
        x = 1975,
        y = sum_all.loc[1975],
        showarrow = True,
        arrowhead = 1,
    )

    fig.add_annotation(
        text="The Lion King",
        x=1994,
        y=sum_all.loc[1994],
        showarrow=True,
        arrowhead=1,
    )

    return fig


def get_box_office_ratio(movie_frames):
    """
    Calculate the box office revenue percentage per year
    :param movie_frames: The MovieFrame class with the movies
    :return: the figure with the plot
    """
    movie_frames.drop_impossible_years()
    box_office_name = "Movie box office revenue inflation adj" if "Movie box office revenue inflation adj" in movie_frames.movie_df.columns else "Movie box office revenue"
    # sum of the box office revenue per year for all movies
    box_office_per_year = movie_frames.movie_df.groupby("release year")[box_office_name].agg(
        'sum')
    box_office_per_year = box_office_per_year.fillna(0)

    box_office_sequel_per_year_list = []

    movie_non_original = None
    for df in movie_frames.get_all_alternate_df():
        bo = df.groupby("release year")[box_office_name].agg('sum').fillna(0)
        bo = bo / box_office_per_year * 100
        bo = bo.fillna(0)
        box_office_sequel_per_year_list.append(bo)

        if movie_non_original is None:
            movie_non_original = df
        else:
            movie_non_original = pd.concat([movie_non_original, df]).drop_duplicates()


    # Plot figure 5: box office revenue percentage per year

    ratio_non_original = movie_non_original.groupby("release year")[box_office_name].agg('sum').fillna(0) / box_office_per_year * 100

    fig = compute_box_office_ratio_graph(box_office_per_year, box_office_sequel_per_year_list, movie_frames.get_all_alternate_df_names(), ratio_non_original,
                                         movie_frames.get_color_discrete)


    return fig

def compute_average_box_office_revenue_graph(average_box_office, average_box_office_alternate, names, get_colors = None):
    """
    Plot the average box office revenue per year
    :param average_box_office: average box office revenue per year
    :param average_box_office_alternate: average box office revenue per year for movies with sequels
    :param names: type of movies
    :param get_colors: function to get the color of the line
    :return:
    """

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=average_box_office.index, y=average_box_office, mode='lines', name='Average box office revenue of all movies',
                  line = dict(color = get_colors("Movies"))))
    for average_box_office_alternate, name in zip(average_box_office_alternate, names):
        fig.add_trace(go.Scatter(x=average_box_office_alternate.index, y=average_box_office_alternate, mode='lines',
                                 name=f'Average box office revenue {name.lower()}', line = dict(color = get_colors(name))))

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

    box_office_name = "Movie box office revenue inflation adj" if "Movie box office revenue inflation adj" in movie_frames.movie_df.columns else "Movie box office revenue"

    average_box_office = movie_frames.movie_df.groupby("release year")[box_office_name].agg('mean')
    average_box_office = average_box_office.fillna(0)

    # calculate box office revenue per movie for movies with sequels and fill NaN values with 0


    average_box_office_list = []
    for df in movie_frames.get_all_alternate_df():
        df_avg = df.groupby("release year")[box_office_name].agg('mean').fillna(0)
        #remove when only one movie has box office revenue
        average_box_office_list.append(df_avg)



    fig = compute_average_box_office_revenue_graph(average_box_office, average_box_office_list, movie_frames.get_all_alternate_df_names(),
                                                   movie_frames.get_color_discrete)

    return fig


def get_box_office_absolute(movie_frames):
    """
    Calculate the box office revenue per year
    :param movie_frames: the database with the movies
    :return: the figure with the plot
    """
    movie_frames.drop_impossible_years()
    box_office_name = "Movie box office revenue inflation adj" if "Movie box office revenue inflation adj" in movie_frames.movie_df.columns else "Movie box office revenue"

    # sum of the box office revenue per year, first for all movies, then for movies with sequels # inflation adj
    box_office_per_year = movie_frames.movie_df.groupby("release year")[box_office_name].agg('sum')
    box_office_per_year_list = []
    names = movie_frames.get_all_alternate_df_names()
    non_original_movies = None
    for df in movie_frames.get_all_alternate_df():
        box_office_per_year_list.append(df.groupby("release year")[box_office_name].agg('sum').fillna(0))
        if non_original_movies is None:
            non_original_movies = df
        else:
            non_original_movies = pd.concat([non_original_movies, df]).drop_duplicates()


    # replace NaN values by 0

    box_office_per_year = box_office_per_year.fillna(0)

    box_office_total = non_original_movies.groupby("release year")[box_office_name].agg('sum').fillna(0)

    fig = compute_graph_box_office_absolute(box_office_per_year, box_office_per_year_list, names, box_office_total, movie_frames.get_color_discrete)
    return fig





def get_compare_first_sequel_graph_plotly(first_vs_rest, average_movie_revenue, get_colors = None):
    """
    Plot the comparison between the box office revenue of the first movie and the sequel movie
    :param first_vs_rest:  dataframe with the box office revenue of the first movie and the sequel movie
    :param average_movie_revenue: average box office revenue for all movies
    :param get_colors: function to get the color of the line
    :return: the figure with the plot
    """

    fig_total = go.Figure()

    x = first_vs_rest["index"]
    y1 = first_vs_rest["first"]
    y2 = first_vs_rest["rest"]

    text_first = first_vs_rest.index + "<br>First movie box office revenue: " + y1.apply(human_format)
    text_sequel = first_vs_rest.index + "<br>Sequel movie box office revenue: " + y2.apply(human_format)

    fig_total.add_trace(go.Scatter(x=x, y=y1, mode='markers', name=f"First movie <br>box office revenue",
                             text=text_first, marker_color = get_colors("Movie"), hoverinfo="text"))
    fig_total.add_trace(go.Scatter(x=x, y=y2, mode='markers', name="Sequel movie <br>box office revenue",
                             text=text_sequel, marker_color = get_colors("Sequels"),hoverinfo="text"))

    for xi, yi1, yi2 in zip(x, y1, y2):
        color = "firebrick" if yi1 > yi2 else "palegreen"
        fig_total.add_shape(type="line", x0=xi, x1=xi, y0=yi1, y1=yi2, line=dict(color=color, width=1))

    fig_total.update_layout(
        title="First movie vs Box office revenue of all sequels",
        xaxis_title="Collection",
        yaxis_title="Box office revenue",
        yaxis_type="log",
        width=800,
        height=600,
        legend = dict(
            yanchor="bottom",
            y=0,
            xanchor="right",
            x=1
        )
    )

    fig_total.add_annotation(
        text = "The James Bond collection<br>has the highest difference",
        x = first_vs_rest["index"].loc["James Bond Collection"],
        y = np.log10(y2["James Bond Collection"]),
        showarrow = True,
        arrowhead=1,
    )

    fig_total.add_annotation(
        text = "Knives Out, with a sequel<br>during the Covid pandemic",
        x = first_vs_rest["index"].loc["Knives Out Collection"],
        y = np.log10(first_vs_rest["rest"].loc["Knives Out Collection"]),
        showarrow = True,
        arrowhead=1,
        ax = -40,
        ay= 40
    )

    fig_avg = go.Figure()
    x = first_vs_rest["index"]
    y1 = first_vs_rest["first"]
    y2 = first_vs_rest["rest_avg"]

    text_first = first_vs_rest.index + "<br>First movie box office revenue: " + y1.apply(human_format)
    text_sequel = first_vs_rest.index + "<br>Average sequel movie box office revenue: " + y2.apply(human_format)

    fig_avg.add_trace(go.Scatter(x=x, y=y1, mode='markers', name=f"First movie <br>box office revenue",
                                text=text_first, marker_color = get_colors("Movie"), hoverinfo="text"))
    fig_avg.add_trace(go.Scatter(x=x, y=y2, mode='markers', name="Average sequel movie <br>box office revenue",
                                text=text_sequel, marker_color = get_colors("Sequels"),hoverinfo="text"))



    for xi, yi1, yi2 in zip(x, y1, y2):
        color = "firebrick" if yi1 > yi2 else "palegreen"
        fig_avg.add_shape(type="line", x0=xi, x1=xi, y0=yi1, y1=yi2, line=dict(color=color, width=1))

    fig_avg.add_hline(y=average_movie_revenue, line_dash="dot", line_color="peru",
                      name="Average box-office revenue of a movie", annotation_text="Average box-office<br>of a movie",
                      annotation_y=np.log10(average_movie_revenue), annotation_position='top left')
    fig_avg.add_hline(y=y2.mean(), line_dash="dot", line_color="blue",
                      name="Average box-office revenue of a sequel movie", annotation_text="Average box-office<br>of a sequel movie",
                      annotation_y=np.log10(y2.mean()), annotation_position='top right')
    fig_avg.add_hline(y=y1.mean(), line_dash="dot", line_color="red",
                      name="Average box-office revenue of a first movie", annotation_text="Average box-office<br>of a first movie",
                      annotation_y=np.log10(y1.mean()), annotation_position='top left',)
    closest_to_average = first_vs_rest["index"].loc[(y2 - average_movie_revenue).abs().idxmin()]
    fig_avg.add_annotation(
        text = "Most movies with sequels<br>preform better than average",
        x = closest_to_average, y = np.log10(average_movie_revenue),
        showarrow = True,
        arrowhead = 1,
        ax = 80,
        ay = 100 )

    fig_avg.add_annotation(
        text = "Spider-Man (MCU) Collection,<br>one of the few increase in<br>successful movies",
        x = first_vs_rest["index"].loc["Spider-Man (MCU) Collection"],
        y = np.log10(y2["Spider-Man (MCU) Collection"]),
        showarrow = True,
        arrowhead = 1,
    )

    fig_avg.update_layout(
        title="First movie vs Average sequel movie box office revenue",
        xaxis_title="Collection",
        yaxis_title="Box office revenue",
        yaxis_type="log",
        width=800,
        height=600,
        legend = dict(
            yanchor="bottom",
            y=0,
            xanchor="right",
            x=1
        )
    )
    return fig_total, fig_avg

def compare_first_sequel(movie_frame):
    """
    compare the box office revenue of the first movie and the sequel movie
    :param movie_frame: the database with the movies
    :return: the figure with the plot
    """

    box_office_name = "Movie box office revenue inflation adj" if "Movie box office revenue inflation adj" in movie_frame.movie_df.columns else "Movie box office revenue"

    box_office_first_movie = movie_frame.movie_df_sequel_original.sort_values("release_date").groupby("collection").first()[
        box_office_name]

    # calculate the remaining box office revenue for each collection # inflation adj

    box_office_remainder = movie_frame.movie_df_sequel_original.groupby("collection")[box_office_name].agg(
        'sum') - box_office_first_movie

    # calculate the remaining box office revenue for each collection (excluding the first movie)

    box_office_remainder_avg = box_office_remainder / (
                movie_frame.movie_df_sequel_original.groupby("collection").count()["Movie name"] - 1)

    first_vs_rest = pd.DataFrame()
    first_vs_rest["first"] = box_office_first_movie
    first_vs_rest["rest"] = box_office_remainder
    first_vs_rest["rest_avg"] = box_office_remainder_avg
    first_vs_rest = first_vs_rest.dropna()
    first_vs_rest = first_vs_rest[first_vs_rest["first"] > 0]
    first_vs_rest = first_vs_rest[first_vs_rest["rest"] > 0]  # remove collections with no revenue
    first_vs_rest = first_vs_rest.sort_values("first",
                                              ascending=True)  # sort in ascending order for the first movie (lowest to the highest)
    first_vs_rest['index'] = range(0, len(first_vs_rest))

    average_movie_revenue = movie_frame.movie_df.dropna(subset=[box_office_name])[
        box_office_name].agg('mean')

    fig_total, fig_avg = get_compare_first_sequel_graph_plotly(first_vs_rest, average_movie_revenue, movie_frame.get_color_discrete)
    return fig_total, fig_avg

def box_office_vs_vote(movie_frame):
    """
    Compare the box office revenue and the average vote of standalone movies and first movies in a collection
    :param df: The dataframe with the movies
    :param df_sequels: The dataframe with the sequels
    """


    movie_frame.read_row_list(["data/collections/sequels_and_original_2010_2024_extended.csv"], "vote_average")
    movie_frame.read_row_list(["data/all_sample/all_sample_2010_2024_extended.csv"], "vote_average")

    df = movie_frame.movie_df
    df_sequels = movie_frame.movie_df_sequel_original

    title = "Movie name" if "Movie name" in df.columns else "title"
    revenue = "Movie box office revenue inflation adj" if "Movie box office revenue inflation adj" in df.columns else "Movie box office revenue" if "Movie box office revenue" in df.columns else "revenue"

    df_sa = df[~df[title].isin(df_sequels[title])]

    df_sa = df_sa[df_sa[revenue]!=0]
    df_sequels = df_sequels[df_sequels[revenue]!=0]

    release_date = "Movie release date" if "Movie release date" in df.columns else "release_date"
    df_sequels[release_date] = df_sequels[release_date].apply(lambda x : pd.to_datetime(x))
    #Trier par collection et date de sortie
    df_sequels = df_sequels.sort_values(by=['collection', release_date])
    df_sequels = df_sequels.drop_duplicates(subset=["id"], keep="first")
    # Attribuer un numéro à chaque film dans une collection
    df_sequels['Numéro'] = df_sequels.groupby('collection').cumcount() + 1

    df_sequels = df_sequels[df_sequels['Numéro']==1]

    standalone_sample = df_sa.sample(n=100, random_state=42)  # Adjust sample size as needed
    first_movie_sample = df_sequels.sample(n=100, random_state=42)

    # Combine the samples into one DataFrame with a new column indicating type
    sampled_movies = pd.concat([
        standalone_sample.assign(sample_type='Standalone'),
        first_movie_sample.assign(sample_type='First in Collection')
    ])

    # Create a Plotly figure
    text = sampled_movies[title] + '<br>' + sampled_movies['sample_type']
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sampled_movies[revenue], y=sampled_movies['vote_average'], mode='markers', marker=dict(
        color=sampled_movies['sample_type'].map({'Standalone': movie_frame.get_color_discrete("Movies"), 'First in Collection': movie_frame.get_color_discrete("Sequels")}),
        size=8,),
                             hovertext=text,))

    # Customize layout
    fig.update_layout(
        legend_title_text='Movie Type',
        xaxis_title='Box Office Revenue',
        yaxis_title='Average vote',
        xaxis=dict(type='log',range=[3,10]),
        yaxis=dict(range=([3,8.5])),
    )

    # Show the plot



    #t-test

    standalone_revenue = df_sa[revenue].dropna()
    first_movie_revenue = df_sequels[revenue].dropna()


    ## check for normal distr


    stat, p_value = kstest(first_movie_revenue ,'norm', args=(first_movie_revenue.mean(), first_movie_revenue.std()))
    print(f"KS Statistic: {stat:.10f}")

    if p_value < 0.05:
        print("Data is not normally distributed.")
    else:
        print("Data is normally distributed.")




    standalone_vote = df_sa['vote_average'].dropna()
    first_movie_vote = df_sequels['vote_average'].dropna()

    stat, p_value = kstest(first_movie_vote ,'norm', args=(first_movie_vote.mean(), first_movie_vote.std()))
    print(f"KS Statistic: {stat:.10f}")

    if p_value < 0.05:
        print("Data is not normally distributed.")
    else:
        print("Data is normally distributed.")


    u_stat_revenue, p_value_u_revenue = mannwhitneyu(standalone_revenue, first_movie_revenue)

    print(f"U_stat: {u_stat_revenue}, p-value : {p_value_u_revenue}")
    if p_value_u_revenue < 0.05:
        print("Significant difference in revenue! Mannytest")
    else:
        print("No significant difference in revenue! Mannytest")

    stat_vote , p_value_vote = ttest_ind(standalone_vote ,first_movie_vote)

    print(f"U_stat: {stat_vote}, p-value : {p_value_vote}")
    if p_value_vote < 0.05:
        print("Significant difference in vote! T-test")
    else:
        print("No significant difference in vote! T-test")

    return fig
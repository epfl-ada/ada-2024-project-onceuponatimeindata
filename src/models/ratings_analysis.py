import pandas as pd
from networkx.algorithms.bipartite.basic import color
from plotly import graph_objects as go

from models.box_office_revenue import get_compare_first_sequel_graph_plotly

def get_compare_first_sequel_graph_rating(first_vs_rest, average_rating, get_colors):
    """
    plot the box office revenue of the first movie and the sequel movie
    :param first_vs_rest: the dataframe with the box office revenue
    :param average_rating: the average rating of a movie
    :param get_colors: function to get the color
    :return: the figure with the plot
    """
    fig_avg = go.Figure()
    x = first_vs_rest["index"]
    y1 = first_vs_rest["first"]
    y2 = first_vs_rest["rest_avg"]

    text_first = first_vs_rest.index + "<br>First movie box average rating: " + y1.astype(str)
    text_sequel = first_vs_rest.index + "<br>Average sequel movie rating average: " + y2.astype(str)

    fig_avg.add_trace(go.Scatter(x=x, y=y1, mode='markers', name=f"First movie rating",
                                 text=text_first, marker_color=get_colors("Movie"), hoverinfo="text"))
    fig_avg.add_trace(go.Scatter(x=x, y=y2, mode='markers', name="Average sequel movie rating",
                                 text=text_sequel, marker_color=get_colors("Sequels"), hoverinfo="text"))

    for i in range(len(x)):
        if y1[i] > y2[i]:
            fig_avg.add_shape(type="line", x0=x[i], x1=x[i], y0=y1[i], y1=y2[i], line=dict(color="lightcoral", width=1))
        else:
            fig_avg.add_shape(type="line", x0=x[i], x1=x[i], y0=y1[i], y1=y2[i], line=dict(color="palegreen", width=1))

    fig_avg.add_hline(y=average_rating, line_dash="dot", line_color="peru", annotation_position='top left',
                      name="Average rating of a movie", annotation_text="Average rating of a movie",)

    fig_avg.add_hline(y=y2.mean(), line_dash="dot", line_color="blue",
                        name="Average rating<br>of a sequel movie", annotation_text="Average rating<br>of a sequel movie",)

    fig_avg.add_hline(y=y1.mean(), line_dash="dot", line_color="red",
                        name="Average rating<br>of a first movie", annotation_text="Average rating<br>of a first movie",)

    fig_avg.update_layout(
        title="First movie vs Average sequel movie box office revenue",
        xaxis_title="Collection",
        yaxis_title="Box office revenue",
        width=1000,
        height=600,
        legend=dict(
            yanchor="bottom",
            y=0,
            xanchor="right",
            x=1
        )
    )
    return fig_avg


def compare_first_sequel_ratings(movie_frame, ratings_path_list):
    """
    compare the box office revenue of the first movie and the sequel movie
    :param movie_frame: the database with the movies
    :param ratings_path_list: list of files with additional ratings information
    :return: the figure with the plot
    """

    for ratings_path in ratings_path_list:
        ratings = pd.read_csv(ratings_path)
        movie_frame.movie_df_sequel_original = pd.merge(movie_frame.movie_df_sequel_original, ratings[["id", "vote_average"]],
                                                        on="id", how="outer") if "vote_average" not in movie_frame.movie_df_sequel_original.columns \
                                                        else movie_frame.movie_df_sequel_original


    # calculate the box office revenue for the first movie of each collection
    box_office_first_movie = movie_frame.movie_df_sequel_original.sort_values("release_date").groupby("collection").first()[
        "vote_average"]

    # calculate the remaining box office revenue for each collection # inflation adj

    box_office_remainder = movie_frame.movie_df_sequel_original.groupby("collection")["vote_average"].agg(
        'sum') - box_office_first_movie

    # calculate the remaining box office revenue for each collection (excluding the first movie)

    box_office_remainder_avg = box_office_remainder / (
                movie_frame.movie_df_sequel_original.groupby("collection").count()["Movie name"] - 1)

    first_vs_rest = pd.DataFrame()
    first_vs_rest["first"] = box_office_first_movie
    first_vs_rest["rest"] = box_office_remainder
    first_vs_rest["rest_avg"] = box_office_remainder_avg
    first_vs_rest = first_vs_rest.dropna()
    first_vs_rest = first_vs_rest[first_vs_rest["first"] > 0]  # remove collections with no ratings
    first_vs_rest = first_vs_rest[first_vs_rest["rest"] > 0]
    first_vs_rest = first_vs_rest[first_vs_rest["rest_avg"] > 0]
    first_vs_rest = first_vs_rest.sort_values("first",
                                              ascending=True)  # sort in ascending order for the first movie (lowest to the highest)
    first_vs_rest['index'] = range(0, len(first_vs_rest))

    average_rating = movie_frame.movie_df_sequel_original["vote_average"].mean()

    fig_avg = get_compare_first_sequel_graph_rating(first_vs_rest, average_rating, movie_frame.get_color_discrete)
    return fig_avg


def get_all_production_companies(prod_companies):
    """
    Get all the production companies
    :param prod_companies: the list of production companies for each movie, each in a dictionary
    :return: the list of all production companies
    """

    all_prod_companies = set()
    for prod_company in prod_companies:
        for company in prod_company:
            all_prod_companies.add(company["name"])
    return all_prod_companies

def get_button(x, y):
    button = list([
        dict(type="buttons",
             direction="left",
             buttons=[dict(label="Sequels",
                           method="update",
                           args=[{"visible": [True, False, False, False]}]),
                      dict(label="Books",
                           method="update",
                           args=[{"visible": [False, True, False, False]}]),
                      dict(label="Comics",
                           method="update",
                           args=[{"visible": [False, False, True, False]}]),
                      dict(label="Remakes",
                           method="update",
                           args=[{"visible": [False, False, False, True]}]),
                      ],

             pad={"r": 10, "t": 10},
             showactive=True,
             x=x,
             xanchor="left",
             y=y,
             yanchor="top"
             ),
    ])
    return button



def violin_chart_studio(movie_frame, extended_path_list):
    """
    Create a violin plot with the rating of the movies per production company
    :param movie_frame: the database with the movies
    :param extended_path_list: list of files with additional rating information
    :return: the figure with the plot
    """

    movie_frame.read_row_list(extended_path_list, "vote_average")
    movie_frame.read_row_list(extended_path_list, "production_companies")
    # for df in movie_frame.get_all_alternate_df():
    #     df = df.copy()
    #     df = df.dropna(subset=["vote_average", "production_companies"])
    #     df["production_companies_dict"] = df["production_companies"].apply(lambda x: list(eval(x)))
    #     prod_companies = prod_companies.union(get_all_production_companies(df["production_companies_dict"]))
    studio_count = {}

    studio_and_average_dict = {}
    for i, (name, df) in enumerate(zip(movie_frame.get_all_alternate_df_names(), movie_frame.get_all_alternate_df())):
        df = df.dropna(subset=["vote_average", "production_companies"])
        df = df[df["vote_average"] > 0]
        df["production_companies_dict"] = df["production_companies"].apply(lambda x: list(eval(x)))
        df = df.dropna(subset=["production_companies_dict"])

        studio_and_average_dict[name] = df.explode("production_companies_dict")[["production_companies_dict", "vote_average", "Movie name"]]
        studio_and_average_dict[name]["company name"] = studio_and_average_dict[name]["production_companies_dict"].apply(lambda x: x["name"] if isinstance(x, dict) else x)
        studio_count[name] = studio_and_average_dict[name]["company name"].value_counts().to_dict()

    top = 12
    studio_count_df = pd.DataFrame(studio_count)
    studio_df_top = studio_count_df.apply(lambda x: x.nlargest(top).index.tolist(), axis=0)

    fig = go.Figure()
    button = get_button(0.5, 1.2)
    for type in studio_df_top.columns:
        x = studio_df_top[type]
        data = studio_and_average_dict[type].loc[studio_and_average_dict[type]["company name"].isin(x), ["vote_average", "company name", "Movie name"]]
        data["company name"] = pd.Categorical(data["company name"], categories=x, ordered=True)
        text = data["Movie name"] + "<br>Rating: " + data["vote_average"].astype(str)
        fig.add_trace(go.Violin(x=data["company name"].apply(lambda x: x.replace(" ", "<br>").replace("-", "<br>")), y=data["vote_average"], name=type, box_visible=True, meanline_visible=True,
                                points="all", hovertext=text, hoverinfo="text+y",
                                visible= "legendonly" if type != "Sequels" else True,
                                marker=dict(color=movie_frame.get_color_discrete(type))))

    data = [trace for trace in fig.data]
    update_menu = get_button(0, 1.1)

    layout = dict(updatemenus=update_menu,
        title="Rating of movies per production company",
        xaxis_title="Production company",
        yaxis_title="Rating",
        width=1000,
        height=600,
        showlegend=False
    )
    fig = go.Figure(data=data, layout=layout)

    return fig
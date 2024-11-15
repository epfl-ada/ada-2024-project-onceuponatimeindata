import pandas as pd
from matplotlib import pyplot as plt


def plot_budget_vs_revenue(budget_df, box_office_revenue, collection_size):
    """
    Plot the budget vs the box office revenue
    """
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(221)

    ax.scatter(budget_df, box_office_revenue, s=collection_size * 50, alpha=0.5, c=box_office_revenue, cmap="cool")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Budget")
    ax.set_ylabel("Box office revenue")

    ax.set_xlim(xmin=1e5)
    ax.set_ylim(ymax=5e11)

    ax.title.set_text("Budget vs Box office revenue")
    return fig

def get_budget_vs_revenue(movieframe):
    # total number of movies in each collection

    collection_size = movieframe.movie_df_sequel_original.groupby("collection").count()["Movie name"]

    # total inflation adjusted box office revenue for each collection

    box_office_revenue = movieframe.movie_df_sequel_original.groupby("collection")["Movie box office revenue inflation adj"].agg(
        'sum')

    sequels_extended = pd.read_csv(
        "data/sequels/sequels_extended_1880_2010.csv")  # dataframe with additional budget information
    movie_df_sequel_original = pd.merge(movieframe.movie_df_sequel_original, sequels_extended[["id", "budget"]],
                                        on="id", how="inner")  if "budget" not in movieframe.movie_df_sequel_original.columns \
                                                               else movieframe.movie_df_sequel_original

    # total budget for each collection

    budget_df = movie_df_sequel_original.groupby("collection")["budget"].agg('sum')

    return fig
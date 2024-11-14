import os

import pandas as pd
from tqdm import tqdm

from src.data.TMDB_Movies import get_data, get_collection, get_movie_data_extended, get_movie_metadatalike_db

from more_itertools import sliced
from src.data.TMDB_Movies import get_wikipedia_id_from_title


def get_wikipedia_id_for_db(df, file, skip = 0):
    wiki_df = None if not os.path.exists(file) else pd.read_csv(file)
    slices = sliced(seq=range(len(df)), n=50)
    i = 0

    for index in tqdm(slices, total=len(df) // 50):
        if i < skip:
            i += 1
            continue
        chunk = df.iloc[index].copy()
        chunk["Wikipedia movie ID"] = chunk.apply(lambda x: get_wikipedia_id_from_title(x["title"], x["release_date"]),
                                                  axis=1)
        wiki_df = pd.concat([wiki_df, chunk], axis=0, ignore_index=True,
                            sort=False) if wiki_df is not None else chunk
        wiki_df.to_csv(file)
    return wiki_df

if __name__ == "__main__":
    book = pd.read_csv("data/book/movie_with_book_1880_2010.csv")
    book_with_wiki_id = get_wikipedia_id_for_db(book, 'data/book/book_with_wiki_id_1880_2010.csv', skip = 14)
    book_with_wiki_id.to_csv('data/book/book_with_wiki_id_1880_2010.csv')

    comics = pd.read_csv("data/comics/movie_with_comics_1880_2010.csv")
    comics_with_wiki_id = get_wikipedia_id_for_db(comics, 'data/comics/comics_with_wiki_id_1880_2010.csv')
    comics_with_wiki_id.to_csv('data/comics/comics_with_wiki_id_1880_2010.csv')

    remake = pd.read_csv("data/remake/movie_with_remake_1880_2010.csv")
    remake_with_wiki_id = get_wikipedia_id_for_db(remake, 'data/remake/remake_with_wiki_id.csv')
    remake_with_wiki_id.to_csv('data/remake/remake_with_wiki_id.csv')



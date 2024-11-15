import os

import pandas as pd
from tqdm import tqdm

from src.data.TMDB_Movies import get_data, get_collection, get_movie_data_extended, get_movie_metadatalike_db, \
    randomly_sample_movie

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
    randomly_sample_movie("2010-01-01", "2024-01-01", 10000)



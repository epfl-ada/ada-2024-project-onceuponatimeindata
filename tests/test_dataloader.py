import pandas as pd

from src.data.TMDB_Movies import get_data
from src.data.TMDB_Movies import get_collection

def test_get_data():
    sequels = pd.read_csv("data/movie_with_keyword_sequel.json")
    get_collection(sequels)



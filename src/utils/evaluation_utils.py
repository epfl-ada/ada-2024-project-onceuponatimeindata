import pandas as pd
import numpy as np


def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

inflation_df = pd.read_csv("data/inflation.csv")

def inflate(revenue, year):
    """
    Inflates the revenue to the current year
    :param revenue: The revenue to inflate
    :param year: The year of the revenue
    :return: The inflated revenue
    """

    if type(year) == str:
        year = int(str(year)[:4])

    if np.isnan(revenue) or np.isnan(year):  # no inflation adjustement for missing values or years before 1900
        return np.nan

    if year < 1913:
        year = 1913

    if year > 2023:
        year = 2023

    inflation_year = inflation_df[inflation_df["Year"] == year]
    inflation_current = inflation_df[inflation_df["Year"] == 2023]

    return revenue * inflation_current["Annual"].values[0] / inflation_year["Annual"].values[0]

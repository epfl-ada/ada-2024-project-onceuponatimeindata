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

def rgb_string_to_array(color):
    """
    Converts a rgb string to a tuple
    :param color: The rgb string of type "rgb(r, g, b)"
    :return: The tuple
    """
    return np.array(color[4:-1].split(",")).astype(int)

def array_to_rgb_string(color):
    """
    Converts a tuple to a rgb string
    :param color: The tuple
    :return: The rgb string of type "rgb(r, g, b)"
    """
    color = color.astype(int)
    return f"rgb({color[0]}, {color[1]}, {color[2]})"

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

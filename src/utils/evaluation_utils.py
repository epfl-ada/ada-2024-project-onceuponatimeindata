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
    # Valider year
    try:
        year = int(str(year)[:4])
    except (ValueError, TypeError):
        return np.nan  # Retourner NaN si year est invalide

    # Vérifier les valeurs manquantes
    if revenue is None or year is None or np.isnan(revenue) or np.isnan(year):
        return np.nan

    # Limiter l'année à la plage 1913-2023
    year = max(1913, min(2023, year))

    # Obtenir les données d'inflation
    inflation_year = inflation_df[inflation_df["Year"] == year]
    inflation_current = inflation_df[inflation_df["Year"] == 2023]

    # Vérifier si les données d'inflation existent
    if inflation_year.empty or inflation_current.empty:
        return np.nan

    # Calculer la valeur ajustée pour l'inflation
    return revenue * inflation_current["Annual"].values[0] / inflation_year["Annual"].values[0]

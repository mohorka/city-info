"""Module for getting information about cities."""
from dataclasses import dataclass

import pandas as pd


@dataclass
class CityInfo:
    """Class, representing information about a city."""

    min_temp: float
    max_temp: float


def get_city_info(df: pd.DataFrame, city: str, year: int) -> CityInfo:
    """Get the min and max temperatures for a city in a given year."""
    filtered_data = df[(df["City"] == city) & (df["dt"].dt.year == year)]
    min_temp, max_temp = filtered_data["AverageTemperature"].agg(["min", "max"])
    if pd.isna(min_temp) or pd.isna(max_temp):
        raise ValueError(f"City {city} not found in year {year}")
    return CityInfo(min_temp, max_temp)


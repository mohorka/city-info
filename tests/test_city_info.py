"""Tests for the get_city_info function."""
import pandas as pd
import pytest

from city_info import CityInfo, get_city_info


@pytest.mark.parametrize(
    "data, city, year, expected",
    [
        (
            pd.DataFrame(
                {
                    "dt": pd.to_datetime(["2013-01-01", "2013-01-02"]),
                    "City": ["City A", "City A"],
                    "AverageTemperature": [1.0, 2.0],
                },
            ),
            "City A",
            2013,
            CityInfo(1.0, 2.0),
        ),
        (  # Same values for min and max
            pd.DataFrame(
                {
                    "dt": pd.to_datetime(["2013-01-01", "2013-01-02"]),
                    "City": ["City A", "City A"],
                    "AverageTemperature": [2.0, 2.0],
                },
            ),
            "City A",
            2013,
            CityInfo(2.0, 2.0),
        ),
        (  # Single row
            pd.DataFrame(
                {
                    "dt": pd.to_datetime(["2013-01-01"]),
                    "City": ["City A"],
                    "AverageTemperature": [1.0],
                },
            ),
            "City A",
            2013,
            CityInfo(1.0, 1.0),
        ),
    ],
)
def test_get_city_info(
    data: pd.DataFrame,
    city: str,
    year: int,
    expected: CityInfo,
) -> None:
    """Test that the function returns the correct values."""
    assert get_city_info(data, city, year) == expected


@pytest.mark.parametrize(
    "data, city, year, expected_error",
    [
        (  # Empty dataframe
            pd.DataFrame(),
            "City A",
            2013,
            KeyError,
        ),
        (  # Missing dt column
            pd.DataFrame(
                {
                    "some_other_column": pd.to_datetime(["2013-01-01", "2013-01-02"]),
                    "City": ["City A", "City A"],
                    "AverageTemperature": [1.0, 2.0],
                },
            ),
            "City A",
            2013,
            KeyError,
        ),
        (  # Missing City column
            pd.DataFrame(
                {
                    "dt": pd.to_datetime(["2013-01-01", "2013-01-02"]),
                    "some_other_name": ["City A", "City A"],
                    "AverageTemperature": [1.0, 2.0],
                },
            ),
            "City A",
            2013,
            KeyError,
        ),
        (  # Missing AverageTemperature column
            pd.DataFrame(
                {
                    "dt": pd.to_datetime(["2013-01-01", "2013-01-02"]),
                    "City": ["City A", "City A"],
                    "some_other_name": [1.0, 2.0],
                },
            ),
            "City A",
            2013,
            KeyError,
        ),
        (  # Year not found
            pd.DataFrame(
                {
                    "dt": pd.to_datetime(["2013-01-01", "2013-01-02"]),
                    "City": ["City A", "City A"],
                    "AverageTemperature": [1.0, 2.0],
                },
            ),
            "City A",
            2014,
            ValueError,
        ),
        (  # City not found
            pd.DataFrame(
                {
                    "dt": pd.to_datetime(["2013-01-01", "2013-01-02"]),
                    "City": ["City A", "City A"],
                    "AverageTemperature": [1.0, 2.0],
                },
            ),
            "City B",
            2013,
            ValueError,
        ),
    ],
)
def test_get_city_info_error(data, city, year, expected_error) -> None:
    """Test that the function raises the correct errors."""
    with pytest.raises(expected_error):
        get_city_info(data, city, year)

import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import datetime, timezone

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
def get_weather(lat, long):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": long,
        "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "precipitation_hours", "wind_speed_10m_max", "wind_direction_10m_dominant"],
        "timezone": "Asia/Bangkok",
        "forecast_days": 1
    }

    # Request the weather data
    responses = openmeteo.weather_api(url, params=params)

    # # Process the first location response
    # response = responses[0]
    # print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    # print(f"Elevation {response.Elevation()} m asl")
    # print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    # print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # # Process daily data
    # daily = response.Daily()
    # daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
    # daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
    # daily_precipitation_sum = daily.Variables(2).ValuesAsNumpy()
    # daily_precipitation_hours = daily.Variables(3).ValuesAsNumpy()
    # daily_wind_speed_10m_max = daily.Variables(4).ValuesAsNumpy()
    # daily_wind_direction_10m_dominant = daily.Variables(5).ValuesAsNumpy()

    # # Build the daily DataFrame
    # daily_data = {
    #     "date": pd.date_range(
    #         start=pd.to_datetime(daily.Time(), unit="s", utc=True),
    #         end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
    #         freq=pd.Timedelta(seconds=daily.Interval()),
    #         inclusive="left"
    #     ),
    #     "temperature_2m_max": daily_temperature_2m_max,
    #     "temperature_2m_min": daily_temperature_2m_min,
    #     "precipitation_sum": daily_precipitation_sum,
    #     "precipitation_hours": daily_precipitation_hours,
    #     "wind_speed_10m_max": daily_wind_speed_10m_max,
    #     "wind_direction_10m_dominant": daily_wind_direction_10m_dominant
    # }

    # daily_dataframe = pd.DataFrame(data=daily_data)

    # # Ensure the `date` column in daily_dataframe is timezone-aware
    # if daily_dataframe["date"].dt.tz is None:
    #     daily_dataframe["date"] = daily_dataframe["date"].dt.tz_localize("Asia/Bangkok")

    # # Ensure `current_time` is also timezone-aware and in the same timezone
    # current_time = pd.Timestamp.now(tz="Asia/Bangkok")

    # # Calculate the time difference
    # daily_dataframe["time_diff"] = abs(daily_dataframe["date"] - current_time)

    # # Find the closest row
    # closest_row = daily_dataframe.loc[daily_dataframe["time_diff"].idxmin()]
    # closest_data = closest_row.to_dict()

    # # Print results
    # print("Current time:", current_time)
    # print("\nDaily DataFrame:")
    # print(daily_dataframe)
    # print("\nClosest Data:")
    # print(closest_data)



    response = responses[0]
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
    daily_precipitation_sum = daily.Variables(2).ValuesAsNumpy()
    daily_precipitation_hours = daily.Variables(3).ValuesAsNumpy()
    daily_wind_speed_10m_max = daily.Variables(4).ValuesAsNumpy()
    daily_wind_direction_10m_dominant = daily.Variables(5).ValuesAsNumpy()

    daily_data = {"date": pd.date_range(
        start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
        end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = daily.Interval()),
        inclusive = "left"
    )}
    # daily_data["temperature_2m_max"] = daily_temperature_2m_max
    # daily_data["temperature_2m_min"] = daily_temperature_2m_min

    avg_temp = (daily_temperature_2m_max + daily_temperature_2m_min) / 2
    daily_data["temperature_2m_avg"] = avg_temp
    daily_data["precipitation_sum"] = daily_precipitation_sum
    daily_data["precipitation_hours"] = daily_precipitation_hours
    daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
    daily_data["wind_direction_10m_dominant"] = daily_wind_direction_10m_dominant

    # daily_dataframe = pd.DataFrame(data = daily_data)
    return daily_data

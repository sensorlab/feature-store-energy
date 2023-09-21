import numpy as np
import pandas as pd

import src.features as F
from src import DATA_PATH

hue_meta = pd.read_parquet(DATA_PATH / "processed" / "HUE_metadata.parquet")
hue_data = pd.read_parquet(DATA_PATH / "processed" / "HUE_residentials.parquet")
hue_weather = pd.read_parquet(DATA_PATH / "processed" / "HUE_weather.parquet")


hue_meta.drop(columns=["first_reading", "last_reading"], inplace=True)

# Drop weather (str) because it's incomplete and defined only in one region
hue_weather.drop(columns=["weather"], inplace=True)

df = hue_data.merge(
    hue_meta.set_index("residential_id"), how="left", left_on="residential_id", right_index=True
).merge(hue_weather, how="left", left_on=["timestamp", "region"], right_on=["timestamp", "region"])

df.dropna(subset=['timestamp'], inplace=True)

df["is_holiday"] = df.apply(F.calc_is_holiday, axis=1).astype(bool)

df["weekday"] = df.apply(F.calc_weekday, axis=1).astype(int)
df["is_weekend"] = df.apply(F.calc_is_weekend, axis=1).astype(bool)

# Figure out percent of the day
df["day_percent"] = df.apply(F.calc_day_percent, axis=1).astype(float)

# Figure out percent of the week
df["week_percent"] = df.apply(F.calc_week_percent, axis=1).astype(float)

# Figure out percentage of the year
df["year_percent"] = df.apply(F.calc_year_percent, axis=1).astype(float)

df["solar_altitude"] = df.apply(F.calc_solar_altitude, axis=1).astype(float)
df["solar_azimuth"] = df.apply(F.calc_solar_azimuth, axis=1).astype(float)
df["solar_radiation"] = df.apply(F.calc_solar_radiation, axis=1).astype(float)

df.to_parquet(DATA_PATH / "hue-dataset-hourly.parquet")

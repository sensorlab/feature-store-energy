import numpy as np
import pandas as pd

import src.features as F
from src import DATA_PATH


lerta_data = pd.read_parquet(DATA_PATH / "processed" / "lerta_data.parquet")

non_ts_columns = ['location_id', 'lat', 'lon', 'tz', 'country']

df = []

for (location_id, lat, lon, tz, country), _group in lerta_data.groupby(by=non_ts_columns):
    group = _group.copy()

    # Make sure values are sorted by timestamp. This is important because of
    # calculation of energy in the next steps.
    group.sort_values(by="timestamp", inplace=True)

    # Obtain delta of time between samples.
    group["dt"] = group.timestamp.diff().dt.seconds.fillna(0)

    # To calculate energy (discrete form), we need to multiply power times delta of time. Output is in Wh
    ts_columns = [col for col in group.columns if col not in non_ts_columns + ['dt', 'timestamp']]
    for col in ts_columns:
        group[col] = group[col].rolling(window=2, min_periods=2).mean() * group["dt"] / 3600.0

    # Drop columns
    group.drop(columns=["dt"], inplace=True)

    # To complete calculation of energy, we sum the products of power and delta-time.
    group.set_index("timestamp", inplace=True, verify_integrity=True)

    # Resample all time series
    group = group.resample('1H').sum(min_count=1, numeric_only=True)

    group['location_id'] = location_id
    group['lat'] = lat
    group['lon'] = lon
    group['tz'] = tz
    group['country'] = country

    group['timestamp'] = group.index.to_pydatetime()
    group.reset_index(drop=True, inplace=True)

    df.append(group)


df = pd.concat(df, ignore_index=True)

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


df.to_parquet(DATA_PATH / "lerta-dataset-hourly.parquet")
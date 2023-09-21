import numpy as np
import pandas as pd

import src.features as F
from src import DATA_PATH

uciml = pd.read_parquet(DATA_PATH / "processed" / "uciml_household.parquet")
uciml.set_index("timestamp", inplace=True)
uciml.sort_index(inplace=True)


ts_columns = [
    "global_active_power",
    "global_reactive_power",
    "sub_metering_1",
    "sub_metering_2",
    "sub_metering_3",
    "unmetered",
    "voltage",
    "global_intensity",
]


df = uciml[ts_columns].resample('1H').agg({
    'global_active_power': np.sum,
    'global_reactive_power': np.sum,
    'sub_metering_1': np.sum,
    'sub_metering_2': np.sum,
    'sub_metering_3': np.sum,
    'unmetered': np.sum,
    'voltage': np.mean,
    'global_intensity': np.mean,
})

for key, value in uciml[["country", "region", "lat", "lon", "tz"]].iloc[0].to_dict().items():
    df[key] = value


df["timestamp"] = df.index

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

df.to_parquet(DATA_PATH / "uciml-dataset-hourly.parquet")

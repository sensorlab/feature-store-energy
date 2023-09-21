import re
from collections import defaultdict
from datetime import date
from glob import glob
from pathlib import Path

import pandas as pd
pd.set_option("display.max_rows", None)
#pd.set_option("max_columns", None)

from src import PROJECT_PATH

UCIML_DATASET_PATH = PROJECT_PATH / "data" / "raw" / "UCI-ML-course"

extras = dict(country="France", region="Sceaux", lat=48.77644, lon=2.29026, tz="Europe/Paris")


def transform_household_data(path=UCIML_DATASET_PATH / "household_power_consumption.txt"):
    df = pd.read_csv(path, sep=";", na_values=['?'])

    #df.columns = [str.lower(column) for column in df.columns]
    df.rename(columns={col: col.lower().strip() for col in df.columns}, inplace=True)

    #df["timestamp"] = pd.to_datetime(df["date"] + "T" + df["time"] + ' CET', dayfirst=True)

    df["timestamp"] = pd.to_datetime(df["date"] + " " + df["time"] + ' +0100', format='%d/%m/%Y %H:%M:%S %z')

    #print(df[(df.timestamp >= '2008-10-26') & (df.timestamp < '2008-10-27')])
    #raise



    # Timestamp is in localtime.
    #df['timestamp'] = df['timestamp'].dt.tz_localize(tz='Europe/Paris', ambiguous='NaT', nonexistent='NaT')
    #df['timestamp'] = df['timestamp'].dt.tz_convert(tz='Europe/Paris')

    df.drop(columns=["date", "time"], inplace=True)
    df.dropna(subset=['timestamp'], inplace=True)

    # Sanity check
    invalid_timestamps = df.timestamp.diff().dt.total_seconds() <= 0
    assert invalid_timestamps.sum() == 0, (invalid_timestamps.sum(), df.timestamp.dt.year.unique())



    # Fix columns with mixed types. >?< is replaced with NaN.
    #for column in df.columns[2:]:
    #    df[column] = pd.to_numeric(df[column], errors="coerce")

    # Convert from kWmin to Wh
    df["global_active_power"] = df["global_active_power"] * 1000 / 60
    df["global_reactive_power"] = df["global_reactive_power"] * 1000 / 60

    # All features related to energy consumption are given Watt-hours.
    df["unmetered"] = df["global_active_power"] - df["sub_metering_1"] - df["sub_metering_2"] - df["sub_metering_3"]

    for key, value in extras.items():
        df[key] = value

    return df


if __name__ == "__main__":
    df = transform_household_data()
    df.to_parquet(PROJECT_PATH / "data" / "processed" / f"uciml_household.parquet")

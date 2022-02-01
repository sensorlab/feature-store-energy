import pandas as pd
import holidays
from datetime import datetime as dt, timedelta
from pysolar import solar, radiation
import pytz
import argparse
from pathlib import Path
import numpy as np




metadata = pd.read_parquet('./residentials-metadata.parquet')
residentials = pd.read_parquet('./residentials.parquet')
weather = pd.read_parquet('./weather.parquet')

## Workarounds
# Household #7, #18 has invalid data. #15 is in different region.
#residentials[~residentials.residential_id.isin([7, 15, 18])]
metadata = metadata[~metadata.residential_id.isin([7, ])]



def enrich_with_metadata_features(df: pd.DataFrame, meta: pd.DataFrame) -> pd.DataFrame:

    # Merge dataset with metadata table
    df = pd.merge(df, meta, how='inner', on='residential_id')

    return df
    


def enrich_with_weather_features(df: pd.DataFrame, weather: pd.DataFrame) -> pd.DataFrame:

    # Merge dataset with weather data
    df = pd.merge(df, weather, how='left', on=['region', 'timestamp'])

    return df


def enrich_with_contextual_features(df: pd.DataFrame):

    # Holiday info
    canada_holidays = holidays.Canada()
    df['is_holiday'] = df.timestamp.apply(lambda ts: ts.date() in canada_holidays)

    # Weekday
    df['weekday'] = df.timestamp.apply(lambda ts: ts.weekday())

    # Weekend info
    df['is_weekend'] = df.timestamp.apply(lambda ts: ts.weekday() >= 5)

    # Figure out percent of the day
    day_start = lambda ts: dt(year=ts.year, month=ts.month, day=ts.day)
    day_end = lambda ts: day_start(ts) + timedelta(days=1)
    df['day_percent'] = df.timestamp.apply(lambda ts: (ts - day_start(ts)).total_seconds() / (day_end(ts) - day_start(ts)).total_seconds())
    
    # Figure out percent of the week
    df['week_percent'] = df.timestamp.apply(lambda ts: ts.weekday() / 6.0)

    # Figure out percentage of the year
    year_start = lambda ts: dt(ts.year, month=1, day=1)
    year_end = lambda ts: dt(ts.year+1, month=1, day=1)
    percent_of_year = lambda ts: (ts - year_start(ts)).total_seconds() / (year_end(ts) - year_start(ts)).total_seconds()
    df['year_percent'] = df.timestamp.apply(percent_of_year)


    def calc_solar_altitude(x: pd.Series) -> float:
        lat, lon, ts, tz = x['lat'], x['lon'], x['timestamp'], x['tz']
        ts = pytz.timezone(tz).localize(ts)
        return solar.get_altitude(lat, lon, ts)

    df['solar_altitude'] = df.apply(calc_solar_altitude, axis=1)

    def calc_solar_azimuth(x: pd.Series) -> float:
        lat, lon, ts, tz = x['lat'], x['lon'], x['timestamp'], x['tz']
        ts = pytz.timezone(tz).localize(ts)
        return solar.get_azimuth(lat, lon, ts)

    df['solar_azimuth'] = df.apply(calc_solar_azimuth, axis=1)

    def calc_solar_radiation(x: pd.Series) -> float:
        alt, ts, tz = x['solar_altitude'], x['timestamp'], x['tz']
        ts = pytz.timezone(tz).localize(ts)
        return radiation.get_radiation_direct(ts, alt)

    df['solar_radiation'] = df.apply(calc_solar_radiation, axis=1)

    return df



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', required=True)
    args = parser.parse_args()

    residentials = enrich_with_metadata_features(residentials, metadata)

    residentials = enrich_with_weather_features(residentials, weather)

    residentials = enrich_with_contextual_features(residentials)


    output_path = Path(args.output).resolve()
    residentials.to_parquet(output_path)





from typing import Union
import pandas as pd
from datetime import datetime, timedelta
from pysolar import solar, radiation
import pytz
import argparse
from pathlib import Path


def timeit(func):
    from time import time
    from functools import wraps

    @wraps(func)
    def wrap(*args, **kwargs):
        ts = time()
        result = func(*args, **kwargs)
        te = time()
        print(f'func:{func.__name__} args:[{args}, {kwargs}] took: {te-ts:2.4f} sec')

        return result
    return wrap


def calc_solar_altitude(x: pd.Series) -> float:
    lat, lon, ts, tz = x['lat'], x['lon'], x['timestamp'], x['tz']
    ts = ts if isinstance(ts, datetime) else datetime.fromtimestamp(ts)
    ts = pytz.timezone(tz).localize(ts)
    return solar.get_altitude(lat, lon, ts)

def calc_solar_azimuth(x: pd.Series) -> float:
    lat, lon, ts, tz = x['lat'], x['lon'], x['timestamp'], x['tz']
    ts = ts if isinstance(ts, datetime) else datetime.fromtimestamp(ts)
    ts = pytz.timezone(tz).localize(ts)
    return solar.get_azimuth(lat, lon, ts)

def calc_solar_radiation(x: pd.Series) -> float:
    lat, lon, ts, tz = x['lat'], x['lon'], x['timestamp'], x['tz']
    ts = ts if isinstance(ts, datetime) else datetime.fromtimestamp(ts)
    ts = pytz.timezone(tz).localize(ts)
    alt = solar.get_altitude(lat, lon, ts)
    return 0.0 if alt < 0 else radiation.get_radiation_direct(ts, alt)

def calc_day_percent(ts: Union[int, datetime]) -> float:
    ts = ts if isinstance(ts, datetime) else datetime.fromtimestamp(ts)

    day_start = datetime(year=ts.year, month=ts.month, day=ts.day)
    day_end = day_start + timedelta(days=1)

    day_percent =  (ts - day_start).total_seconds() / (day_end - day_start).total_seconds()
    return day_percent

def calc_week_percent(ts: Union[int, datetime]) -> float:
    ts = ts if isinstance(ts, datetime) else datetime.fromtimestamp(ts)

    week_percent = ts.weekday() / 6.0
    return week_percent

def calc_year_percent(ts: Union[int, datetime]) -> float:
    ts = ts if isinstance(ts, datetime) else datetime.fromtimestamp(ts)

    year_start = datetime(ts.year, month=1, day=1)
    year_end = datetime(ts.year+1, month=1, day=1)
    year_percent = (ts - year_start).total_seconds() / (year_end - year_start).total_seconds()
    return year_percent

def calc_weekday(ts: Union[int, datetime]) -> int:
    ts = ts if isinstance(ts, datetime) else datetime.fromtimestamp(ts)
    return ts.weekday()

def calc_is_weekend(ts: Union[int, datetime]) -> bool:
    ts = ts if isinstance(ts, datetime) else datetime.fromtimestamp(ts)
    return bool(ts.weekday() >= 5)

def calc_is_holiday(ts: Union[int, datetime]) -> bool:
    import holidays
    ts = ts if isinstance(ts, datetime) else datetime.fromtimestamp(ts)
    canada_holidays = holidays.Canada()
    return bool(ts.date() in canada_holidays)




def enrich_with_metadata_features(df: pd.DataFrame, meta: pd.DataFrame) -> pd.DataFrame:

    # Merge dataset with metadata table
    df = pd.merge(df, meta, how='inner', on='residential_id')

    return df
    


def enrich_with_weather_features(df: pd.DataFrame, weather: pd.DataFrame) -> pd.DataFrame:

    # Merge dataset with weather data
    df = pd.merge(df, weather, how='left', on=['region', 'timestamp'])

    return df


def enrich_with_contextual_features(df: pd.DataFrame):

    timestamps = df['timestamp']

    df['is_holiday'] = timestamps.apply(calc_is_holiday).astype(bool)

    df['weekday'] = timestamps.apply(calc_weekday).astype(int)

    df['is_weekend'] = timestamps.apply(calc_is_weekend).astype(bool)

    # Figure out percent of the day

    df['day_percent'] = timestamps.apply(calc_day_percent).astype(float)
    
    # Figure out percent of the week
    df['week_percent'] = timestamps.apply(calc_week_percent).astype(float)

    # Figure out percentage of the year
    df['year_percent'] = timestamps.apply(calc_year_percent).astype(float)

    df['solar_altitude'] = df.apply(calc_solar_altitude, axis=1).astype(float)
    df['solar_azimuth'] = df.apply(calc_solar_azimuth, axis=1).astype(float)
    df['solar_radiation'] = df.apply(calc_solar_radiation, axis=1).astype(float)

    return df


@timeit
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', required=True)
    args = parser.parse_args()

    metadata = pd.read_parquet('./residentials-metadata.parquet')
    residentials = pd.read_parquet('./residentials.parquet')
    weather = pd.read_parquet('./weather.parquet')

    ## Workarounds
    # Household #7, #18 has invalid data. #15 is in different region.
    #residentials[~residentials.residential_id.isin([7, 15, 18])]
    metadata = metadata[~metadata.residential_id.isin([7, ])]


    residentials = enrich_with_metadata_features(residentials, metadata)

    residentials = enrich_with_weather_features(residentials, weather)

    residentials = enrich_with_contextual_features(residentials)


    output_path = Path(args.output).resolve()
    residentials.to_parquet(output_path)


if __name__ == '__main__':
    main()





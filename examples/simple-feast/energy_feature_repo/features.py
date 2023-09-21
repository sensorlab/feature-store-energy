from pathlib import Path
from typing import Union

import pandas as pd
from feast import Entity, Feature, FeatureView, FileSource, ValueType
from feast.data_source import RequestDataSource
from feast.on_demand_feature_view import on_demand_feature_view
from feast.request_feature_view import RequestFeatureView
from google.protobuf.duration_pb2 import Duration

from datetime import datetime, timedelta
import pytz
from pysolar import radiation, solar
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[3]
SRC_DATA_PATH = PROJECT_ROOT / 'examples' / 'simple-dvc'

residential_dataset_path = SRC_DATA_PATH / 'residentials.parquet'
assert residential_dataset_path.exists()

metadata_dataset_path = SRC_DATA_PATH / 'residentials-metadata.parquet'
assert metadata_dataset_path.exists()

weather_dataset_path = SRC_DATA_PATH / 'weather.parquet'
assert weather_dataset_path.exists()

residential_id = Entity(
    name='residential_id',
    value_type=ValueType.INT64,
    description='residential ID'
)

region_id = Entity(
    name='region',
    value_type=ValueType.STRING,
    description='region ID'
)


residential_hourly_stats = FileSource(
    path=str(residential_dataset_path),
    event_timestamp_column='timestamp',
)

residential_hourly_stats_view = FeatureView(
    name='residential_hourly_stats',
    # What columns are entities. Used when data is joined.
    entities=['residential_id'],
    # Measurement validity period. 1h in our case. Used when data is joined
    ttl=Duration(seconds=3600),
    # Describe features in the data
    features=[
        Feature(name='timestamp', dtype=ValueType.FLOAT),
        Feature(name='energy', dtype=ValueType.FLOAT)
    ],
    online=True,
    # source of the data (parquet file in our case)
    batch_source=residential_hourly_stats,
    tags={},
)


residential_metadata = FileSource(
    path=str(metadata_dataset_path),
    event_timestamp_column='first_reading',
)

residential_metadata_view = FeatureView(
    name='residential_metadata',
    # What columns are entities. Used when data is joined.
    entities=['residential_id'],
    # "measurement" validity period. Metadata is valid indefinitely.
    ttl=Duration(seconds=0),
    features=[
        Feature(name='house_type', dtype=ValueType.STRING),
        Feature(name='facing', dtype=ValueType.STRING),
        Feature(name='region', dtype=ValueType.STRING),
        Feature(name='RUs', dtype=ValueType.FLOAT),
        Feature(name='EVs', dtype=ValueType.FLOAT),
        Feature(name='SN', dtype=ValueType.FLOAT),
        Feature(name='FAGF', dtype=ValueType.INT64),
        Feature(name='HP', dtype=ValueType.INT64),
        Feature(name='FPG', dtype=ValueType.INT64),
        Feature(name='FPE', dtype=ValueType.INT64),
        Feature(name='NAC', dtype=ValueType.INT64),
        Feature(name='FAC', dtype=ValueType.INT64),
        Feature(name='PAC', dtype=ValueType.INT64),
        Feature(name='BHE', dtype=ValueType.INT64),
        Feature(name='IFRHE', dtype=ValueType.INT64),
        Feature(name='WRHIR', dtype=ValueType.INT64),
        Feature(name='GEOTH', dtype=ValueType.INT64),
        Feature(name='lat', dtype=ValueType.FLOAT),
        Feature(name='lon', dtype=ValueType.FLOAT),
        Feature(name='tz', dtype=ValueType.STRING),
    ],
    online=True,
    # source of the data (parquet file in our case)
    batch_source=residential_metadata,
    tags={},
)


weather_hourly_stats = FileSource(
    path=str(weather_dataset_path),
    event_timestamp_column='timestamp',
)

weather_hourly_stats_view = FeatureView(
    name='weather_hourly_stats',
    # What columns are entities. Used when data is joined.
    entities=['region'],
    # Measurement validity period. 1h in our case. Used when data is joined
    ttl=Duration(seconds=3600),
    features=[
        Feature(name='temperature', dtype=ValueType.FLOAT),
        Feature(name='humidity', dtype=ValueType.FLOAT),
        Feature(name='pressure', dtype=ValueType.FLOAT),
        Feature(name='weather', dtype=ValueType.STRING),
    ],
    online=True,
    # source of the data (parquet file in our case)
    batch_source=weather_hourly_stats,
    tags={},
)


def calc_solar_altitude(x: pd.Series) -> float:
    lat, lon, ts, tz = x['lat'], x['lon'], x['timestamp'], x['tz']
    ts = ts if isinstance(ts, datetime) else datetime.fromtimestamp(ts)
    ts = pytz.timezone(tz).localize(ts)
    return solar.get_altitude(lat, lon, ts)

def calc_solar_azimuth(x: pd.Series) -> float:
    lat, lon, ts, tz = x['lat'], x['lon'], x['timestamp'], x['tz']
    ts = pytz.timezone(tz).localize(ts)
    ts = ts if isinstance(ts, datetime) else datetime.fromtimestamp(ts)
    return solar.get_azimuth(lat, lon, ts)

def calc_solar_radiation(x: pd.Series) -> float:
    lat, lon, ts, tz = x['lat'], x['lon'], x['timestamp'], x['tz']
    ts = ts if isinstance(ts, datetime) else datetime.fromtimestamp(ts)
    alt = solar.get_altitude(lat, lon, ts)
    ts = pytz.timezone(tz).localize(ts)
    return radiation.get_radiation_direct(ts, alt)


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

#solar_altitude = calc_solar_altitude(dict(lat=0, lon=0, timestamp=dt.now(), tz='GMT'))
#solar_azimuth = calc_solar_azimuth(dict(lat=0, lon=0, timestamp=dt.now(), tz='GMT'))
#solar_radiation = calc_solar_radiation(dict(solar_altitude=solar_altitude, timestamp=dt.now(), tz='GMT'))

#print(solar_altitude, solar_azimuth, solar_radiation)

# On demand transformations
# @on_demand_feature_view(
#     inputs={
#         'residential_hourly_stats': residential_hourly_stats_view,
#         'residential_metadata': residential_metadata_view,
#     },
#     features=[
#         Feature(name='is_holiday', dtype=ValueType.BOOL),

#         Feature(name='weekday', dtype=ValueType.INT64),
#         Feature(name='is_weekend', dtype=ValueType.BOOL),

#         #Feature(name='day_percent', dtype=ValueType.FLOAT),
#         #Feature(name='week_percent', dtype=ValueType.FLOAT),
#         #Feature(name='year_percent', dtype=ValueType.FLOAT),

#         #Feature(name='solar_altitude', dtype=ValueType.FLOAT),
#         #Feature(name='solar_azimuth', dtype=ValueType.FLOAT),
#         #Feature(name='solar_radiation', dtype=ValueType.FLOAT),
#     ],
# )
# def contextual_features(inputs: pd.DataFrame) -> pd.DataFrame:
#     df = pd.DataFrame()

#     timestamps = inputs['timestamp']
#     #geodata = inputs[['lat', 'lon', 'timestamp', 'tz']]

#     df['is_holiday'] = timestamps.apply(calc_is_holiday).astype(bool)

#     df['weekday'] = timestamps.apply(calc_weekday).astype(int)

#     df['is_weekend'] = timestamps.apply(calc_is_weekend).astype(bool)

#     # Figure out percent of the day

#     df['day_percent'] = timestamps.apply(calc_day_percent).astype(float)
    
#     # Figure out percent of the week
#     df['week_percent'] = timestamps.apply(calc_week_percent).astype(float)

#     # Figure out percentage of the year
#     df['year_percent'] = timestamps.apply(calc_year_percent).astype(float)

#     #df['solar_altitude'] = geodata.apply(calc_solar_altitude, axis=1).astype(float)
#     #df['solar_azimuth'] = geodata.apply(calc_solar_azimuth, axis=1).astype(float)
#     #df['solar_radiation'] = geodata.apply(calc_solar_radiation, axis=1).astype(float)

#     return df




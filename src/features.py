from typing import Union
from datetime import datetime, timedelta
import pylunar
import holidays
import pytz

from pysolar import solar, radiation

import pandas as pd


def calc_solar_altitude(x: pd.Series) -> float:
    lat, lon, ts, tz = x['lat'], x['lon'], x['timestamp'].to_pydatetime(), x['tz']
    if not isinstance(ts, datetime):
        ts = datetime.fromtimestamp(ts)
        
    try:
        ts = pytz.timezone(tz).localize(ts)
    except ValueError: # ValueError: Not naive datetime (tzinfo is already set)
        pass

    return solar.get_altitude(lat, lon, ts)

def calc_solar_azimuth(x: pd.Series) -> float:
    lat, lon, ts, tz = x['lat'], x['lon'], x['timestamp'].to_pydatetime(), x['tz']
    if not isinstance(ts, datetime):
        ts = datetime.fromtimestamp(ts)
        
    try:
        ts = pytz.timezone(tz).localize(ts)
    except ValueError: # ValueError: Not naive datetime (tzinfo is already set)
        pass

    return solar.get_azimuth(lat, lon, ts)

def calc_solar_radiation(x: pd.Series) -> float:
    lat, lon, ts, tz = x['lat'], x['lon'], x['timestamp'].to_pydatetime(), x['tz']
    if not isinstance(ts, datetime):
        ts = datetime.fromtimestamp(ts)
        
    try:
        ts = pytz.timezone(tz).localize(ts)
    except ValueError: # ValueError: Not naive datetime (tzinfo is already set)
        pass

    alt = solar.get_altitude(lat, lon, ts)
    return 0.0 if alt < 0 else radiation.get_radiation_direct(ts, alt)

def calc_day_percent(x: pd.Series) -> float:
    lat, lon, ts, tz = x['lat'], x['lon'], x['timestamp'].to_pydatetime(), x['tz']
    if not isinstance(ts, datetime):
        datetime.fromtimestamp(ts)

    day_start = datetime(year=ts.year, month=ts.month, day=ts.day, tzinfo=ts.tzinfo)
    day_end = day_start + timedelta(days=1)

    day_percent =  (ts - day_start).total_seconds() / (day_end - day_start).total_seconds()
    return day_percent

def calc_week_percent(x: pd.Series) -> float:
    lat, lon, ts, tz = x['lat'], x['lon'], x['timestamp'].to_pydatetime(), x['tz']
    if not isinstance(ts, datetime):
        ts = datetime.fromtimestamp(ts)
    
    week_percent = ts.weekday() / 6.0
    return week_percent

def calc_year_percent(x: pd.Series) -> float:
    lat, lon, ts, tz = x['lat'], x['lon'], x['timestamp'].to_pydatetime(), x['tz']
    if not isinstance(ts, datetime):
        ts = datetime.fromtimestamp(ts)
        
    year_start = datetime(ts.year, month=1, day=1, tzinfo=ts.tzinfo)
    year_end = datetime(ts.year+1, month=1, day=1, tzinfo=ts.tzinfo)
    year_percent = (ts - year_start).total_seconds() / (year_end - year_start).total_seconds()
    return year_percent

def calc_weekday(x: pd.Series) -> int:
    lat, lon, ts, tz = x['lat'], x['lon'], x['timestamp'].to_pydatetime(), x['tz']
    if not isinstance(ts, datetime):
        ts = datetime.fromtimestamp(ts)
        
    try:
        ts = pytz.timezone(tz).localize(ts)
    except ValueError: # ValueError: Not naive datetime (tzinfo is already set)
        pass

    return ts.weekday()

def calc_is_weekend(x: pd.Series) -> bool:
    lat, lon, ts, tz = x['lat'], x['lon'], x['timestamp'].to_pydatetime(), x['tz']
    if not isinstance(ts, datetime):
        ts = datetime.fromtimestamp(ts)
        
    try:
        ts = pytz.timezone(tz).localize(ts)
    except ValueError: # ValueError: Not naive datetime (tzinfo is already set)
        pass

    return bool(ts.weekday() >= 5)

def calc_is_holiday(x: pd.Series) -> bool:
    lat, lon, ts, tz, country = x['lat'], x['lon'], x['timestamp'].to_pydatetime(), x['tz'], x['country']
    if not isinstance(ts, datetime):
        ts = datetime.fromtimestamp(ts)
    
    try:
        ts = pytz.timezone(tz).localize(ts)
    except ValueError: # ValueError: Not naive datetime (tzinfo is already set)
        pass

    country_holidays = holidays.country_holidays(country=country)
    return bool(ts.date() in country_holidays)
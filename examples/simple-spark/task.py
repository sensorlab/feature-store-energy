
from typing import Union
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, FloatType, BooleanType
from pyspark.sql.functions import udf


from os import environ
from datetime import datetime, timedelta
from pysolar import solar, radiation
import pytz


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





@udf(returnType=FloatType())
def calc_solar_altitude(lat, lon, ts, tz) -> float:
    ts = ts if isinstance(ts, datetime) else datetime.fromtimestamp(ts)
    ts = pytz.timezone(tz).localize(ts)
    return solar.get_altitude(lat, lon, ts)

@udf(returnType=FloatType())
def calc_solar_azimuth(lat, lon, ts, tz) -> float:
    ts = ts if isinstance(ts, datetime) else datetime.fromtimestamp(ts)
    ts = pytz.timezone(tz).localize(ts)
    return solar.get_azimuth(lat, lon, ts)

@udf(returnType=FloatType())
def calc_solar_radiation(lat, lon, ts, tz) -> float:
    ts = ts if isinstance(ts, datetime) else datetime.fromtimestamp(ts)
    ts = pytz.timezone(tz).localize(ts)
    alt = solar.get_altitude(lat, lon, ts)
    return 0.0 if alt < 0 else radiation.get_radiation_direct(ts, alt)

@udf(returnType=FloatType())
def calc_day_percent(ts: Union[int, datetime]) -> float:
    ts = ts if isinstance(ts, datetime) else datetime.fromtimestamp(ts)

    day_start = datetime(year=ts.year, month=ts.month, day=ts.day)
    day_end = day_start + timedelta(days=1)

    day_percent =  (ts - day_start).total_seconds() / (day_end - day_start).total_seconds()
    return day_percent

@udf(returnType=FloatType())
def calc_week_percent(ts: Union[int, datetime]) -> float:
    ts = ts if isinstance(ts, datetime) else datetime.fromtimestamp(ts)
    week_percent = ts.weekday() / 6.0
    return week_percent

@udf(returnType=FloatType())
def calc_year_percent(ts: Union[int, datetime]) -> float:
    ts = ts if isinstance(ts, datetime) else datetime.fromtimestamp(ts)
    year_start = datetime(ts.year, month=1, day=1)
    year_end = datetime(ts.year+1, month=1, day=1)
    year_percent = (ts - year_start).total_seconds() / (year_end - year_start).total_seconds()
    return year_percent

@udf(returnType=IntegerType())
def calc_weekday(ts: Union[int, datetime]) -> int:
    ts = ts if isinstance(ts, datetime) else datetime.fromtimestamp(ts)
    return ts.weekday()

@udf(returnType=BooleanType())
def calc_is_weekend(ts: Union[int, datetime]) -> bool:
    ts = ts if isinstance(ts, datetime) else datetime.fromtimestamp(ts)
    return bool(ts.weekday() >= 5)

@udf(returnType=BooleanType())
def calc_is_holiday(ts: Union[int, datetime]) -> bool:
    import holidays
    ts = ts if isinstance(ts, datetime) else datetime.fromtimestamp(ts)
    canada_holidays = holidays.Canada()
    return bool(ts.date() in canada_holidays)


@timeit
def main():
    master_uri = environ['SPARK_MASTER'] or 'spark://spark-master:7077'

    spark = SparkSession.builder \
        .master(master_uri) \
        .appName("Test") \
        .getOrCreate()
        #.config("spark.driver.memory", "4g") \
        #.config('spark.executor.memory', '6g') \


    meta_df = spark.read.parquet(f'file:////media/processed/residential-metadata.parquet')
    meta_df = meta_df.filter(~meta_df.residential_id.isin([7]))


    energy_df = spark.read.parquet(f'file:////media/processed/residential-data.parquet')
    weather_df = spark.read.parquet(f'file:////media/processed/weather.parquet')

    df = energy_df.join(meta_df, on=['residential_id'], how='inner')

    df = df.join(weather_df, on=['region', 'timestamp'], how='left')

    # Enrich with contextual data
    df = df.withColumn('is_holiday', calc_is_holiday('timestamp'))
    df = df.withColumn('weekday', calc_weekday('timestamp'))
    df = df.withColumn('is_weekend', calc_is_weekend('timestamp'))

    df = df.withColumn('day_percent', calc_day_percent('timestamp'))
    df = df.withColumn('week_percent', calc_week_percent('timestamp'))
    df = df.withColumn('year_percent', calc_year_percent('timestamp'))


    df = df.withColumn('solar_altitude', calc_solar_altitude('lat', 'lon', 'timestamp', 'tz'))
    df = df.withColumn('solar_azimuth', calc_solar_azimuth('lat', 'lon', 'timestamp', 'tz'))
    df = df.withColumn('solar_radiation', calc_solar_radiation('lat', 'lon', 'timestamp', 'tz'))

    print(df.printSchema())
    print('Length', df.count())

    df.write.csv('/app/features.csv', mode='overwrite')

    df = spark.read.csv('/app/features.csv')
    print(df.printSchema())
    print('Length', df.count())


if __name__ == '__main__':
    main()
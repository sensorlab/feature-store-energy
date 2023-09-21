
from typing import Union
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, FloatType, BooleanType, TimestampType
from pyspark.sql.functions import udf


from os import environ
from datetime import datetime, timedelta
from pysolar import solar, radiation
import pytz
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .master(environ['SPARK_MASTER']) \
    .appName("Test") \
    .getOrCreate()


df = spark.read.parquet('file:////media/processed/features.parquet')
print(df.printSchema())

dates = ("2016-01-01",  "2017-01-01")
date_from, date_to = [F.to_date(F.lit(s)).cast(TimestampType()) for s in dates]

subset = df.where((df.timestamp >= date_from) & (df.timestamp < date_to))
subset.select('*').collect()
import re
from collections import defaultdict
from glob import glob
from io import StringIO
from pathlib import Path

import pandas as pd

from src import PROJECT_PATH

REFIT_DATASET_PATH = PROJECT_PATH / "data" / "raw" / "REFIT"
REFIT_OUTPUT_PATH = PROJECT_PATH / "data" / "processed"

extras = dict(country="GB", location="Loughborough", lat=52.7709, lon=-1.2097, tz="Europe/London")

meta = """
House, Occupancy, Construction Year, Appliances Owned, Type, Size
1	,	2	,	1975-1980				, 35 , Detached			, 4 bed
2	,	4	,	-						, 15 , Semi-detached	, 3 bed
3	,	2	,	1988					, 27 , Detached			, 3 bed
4	,	2	,	1850-1899 				, 33 , Detached			, 4 bed
5	,	4	,	1878					, 44 , Mid-terrace		, 4 bed
6	,	2	,	2005					, 49 , Detached			, 4 bed
7	,	4	,	1965-1974				, 25 , Detached			, 3 bed
8	,	2	,	1966					, 35 , Detached			, 2 bed
9	,	2	,	1919-1944				, 24 , Detached			, 3 bed
10	,	4	,	1919-1944				, 31 , Detached			, 3 bed
11	,	1	,	1945-1964				, 25 , Detached			, 3 bed
12	,	3	,	1991-1995				, 26 , Detached			, 3 bed
13	,	4	,	post 2002				, 28 , Detached			, 4 bed
15	,	1	,	1965-1974				, 19 , Semi-detached	, 3 bed
16	,	6	,	1981-1990				, 48 , Detached			, 5 bed
17	,	3	,	mid 60s					, 22 , Detached			, 3 bed
18	,	2	,	1965-1974				, 34 , Detached			, 3 bed
19	,	4	,	1945-1964				, 26 , Semi-detached	, 3 bed
20	,	2	,	1965-1974				, 39 , Detached			, 3 bed
21	,	4	,	1981-1990				, 23 , Detached			, 3 bed
"""


def process_metadata(meta: str = meta) -> pd.DataFrame:
    # Household info

    meta = meta.replace("\t", " ")

    meta = pd.read_csv(StringIO(meta))
    meta.rename(columns={col: col.lower().strip() for col in meta.columns}, inplace=True)
    #meta.columns = [str.lower(column) for column in meta.columns]
    meta = meta.set_index("house", drop=False)

    for key, value in extras.items():
        meta[key] = value

    meta.columns = [c.strip().lower().replace(" ", "_") for c in meta.columns]

    meta.rename(columns={"type": "house_type", "size": "house_size"}, inplace=True)


    appliances = [
        'aggregate, fridge, chest freezer, upright freezer, tumble dryer, washing machine, dishwasher, computer site, television site, electric heater',
        'aggregate, fridge-freezer, washing machine, dishwasher, television, microwave, toaster, hi-fi, kettle, oven extractor fan',
        'aggregate, toaster, fridge-freezer, freezer, tumble dryer, dishwasher, washing machine, television, microwave, kettle',
        'aggregate, fridge, freezer, fridge-freezer, washing machine (1), washing machine (2), computer site, television site, microwave, kettle',
        'aggregate, fridge-freezer, tumble dryer 3, dishwasher, computer site, television site, combination microwave, kettle, toaster',
        'aggregate, freezer (utility room), washing machine, dishwasher, mjy computer, television site, microwave, kettle, toaster, pgm computer',
        'aggregate, fridge, freezer (garage), freezer, tumble dryer, washing machine, dishwasher, television site, toaster, kettle',
        'aggregate, fridge, freezer, dryer, washing machine, toaster, computer, television site, microwave, kettle',
        'aggregate, fridge-freezer, washer dryer, washing machine, dishwasher, television site, microwave, kettle, hi-fi, electric heater',
        'aggregate, magimix (blender), freezer, chest freezer (in garage), fridge-freezer, washing machine, dishwasher, television site, microwave, kenwood kmix',
        'aggregate, fridge, fridge-freezer, washing machine, dishwasher, computer site, microwave, kettle, router, hi-fi',
        'aggregate, fridge-freezer, television site(lounge), microwave, kettle, toaster, television site (bedroom), not used, not used, not used',
        'aggregate, television site, unknown, washing machine, dishwasher, tumble dryer, television site, computer site, microwave, kettle',
        None,
        'aggregate, fridge-freezer, tumble dryer, washing machine, dishwasher, computer site, television site, microwave, kettle, toaster',
        'aggregate, fridge-freezer (1), fridge-freezer (2), electric heater (1)?, electric heater (2), washing machine, dishwasher, computer site, television site, dehumidifier/heater',
        'aggregate, freezer (garage), fridge-freezer, tumble dryer (garage), washing machine, computer site, television site, microwave, kettle, plug site (bedroom)',
        'aggregate, fridge(garage), freezer(garage), fridge-freezer, washer dryer(garage), washing machine, dishwasher, desktop computer, television site, microwave',
        'aggregate, fridge & freezer, washing machine, television site, microwave, kettle, toaster, bread-maker, lamp (80watts), hi-fi',
        'aggregate, fridge, freezer, tumble dryer, washing machine, dishwasher, computer site, television site, microwave, kettle',
        'aggregate, fridge-freezer, tumble dryer, washing machine, dishwasher, food mixer, television, kettle/toaster, vivarium, pond pump',
    ]
    

    meta['appliances'] = meta.apply(lambda x: appliances[x['house'] - 1], axis=1)

    return meta


def process_household_data(path: Path) -> pd.DataFrame:
    entity = path.name

    idx = int(re.findall(r"\d+", entity)[-1])

    df = pd.read_csv(path)
    df.columns = [str.lower(column) for column in df.columns]

    df["house"] = idx
    # df['timestamp'] = pd.to_datetime(df['time'])
    
    # We assume that time is given in UTC
    df["timestamp"] = pd.to_datetime(df['unix'], unit='s', utc=True)

    df['timestamp'] = df['timestamp'].dt.tz_convert('Europe/London')

    # Sanity check
    invalid_timestamps = df.timestamp.diff().dt.total_seconds() <= 0
    assert invalid_timestamps.sum() == 0, (invalid_timestamps.sum(), df.timestamp.dt.year.unique())

    df.drop(columns=["time", "unix"], inplace=True)
    df.rename(columns={c: c.strip().lower() for c in df.columns}, inplace=True)

    return df


if __name__ == "__main__":
    df = process_metadata()
    df.to_parquet(REFIT_OUTPUT_PATH / "refit_metadata.parquet")

    dfs = []

    for filepath in glob(str(REFIT_DATASET_PATH / "CLEAN_House*.csv")):
        filepath = Path(filepath)
        df = process_household_data(filepath)
        dfs.append(df)

    dfs = pd.concat(dfs, ignore_index=True)
    dfs.to_parquet(REFIT_OUTPUT_PATH / "refit_data.parquet")

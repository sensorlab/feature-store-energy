# from src.features import calculate
import re
from collections import defaultdict
from glob import glob
from pathlib import Path

import pandas as pd

from src import DATA_PATH, PROJECT_PATH

LERTA_DATASET_PATH = DATA_PATH / "raw" / "Lerta"

residential_datasets = sorted(glob(str(LERTA_DATASET_PATH / "CLEAN_Lerta_House*.csv")))
assert len(residential_datasets) == 4


extras = dict(country="Poland", lat=51.9194, lon=19.1451, tz="Europe/Warsaw")



def process_residential_data(dataset_path: str) -> pd.DataFrame:
    dataset_path: Path = Path(dataset_path).resolve()
    assert dataset_path.exists()

    
    df = pd.read_csv(dataset_path)
    df.rename(columns={col: col.lower().strip() for col in df.columns}, inplace=True)
    df.rename(columns={'time': 'timestamp', 'aggregate': 'energy'}, inplace=True)

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    # Timestamp is already in UTC format: 2020-02-27 00:00:18+00:00,347.00000000000006,60.0,17.0,51.0,43.0,73.0,0.0,1.0,0.0,0.0,5.0
    # We just adapt it to local time
    df['timestamp'] = df.timestamp.dt.tz_convert('Europe/Warsaw')

    # Sanity check
    invalid_timestamps = df.timestamp.diff().dt.total_seconds() <= 0
    assert invalid_timestamps.sum() == 0, (invalid_timestamps.sum(), df.timestamp.dt.year.unique())


    location_id = int(re.findall(r"(\d+)", dataset_path.stem)[-1])
    df['location_id'] = location_id


    for key, value in extras.items():
        df[key] = value

    return df


if __name__ == '__main__':
    dfs = []
    for dataset_path in residential_datasets:
        df = process_residential_data(dataset_path)
        #print(sorted(df.columns), len(df.columns))
        dfs.append(df)

    dfs = pd.concat(dfs, ignore_index=True, sort=False)
    dfs.to_parquet(DATA_PATH / "processed" / "lerta_data.parquet")

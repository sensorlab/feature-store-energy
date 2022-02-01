import argparse
from pathlib import Path
from glob import glob
import re

import pandas as pd


def process_weather_data(dataset_path:str) -> pd.DataFrame:
    dataset_path:Path = Path(dataset_path).resolve()
    assert dataset_path.exists()

    df = pd.read_csv(dataset_path)
    df['hour'] -= 1
    df['timestamp'] = pd.to_datetime(df['date'].astype(str) + 'T' + df['hour'].astype(str) + ':00:00')
    
    df.drop(['date', 'hour'], axis=1, inplace=True)
    
    df['weather'] = df.weather.fillna('')
    
    # Fill missing values
    df['temperature'] = df['temperature'].interpolate(method='linear', limit=5)
    df['humidity'] = df['humidity'].interpolate(method='linear', limit=5)
    df['pressure'] = df['pressure'].interpolate(method='linear', limit=5)

    # Parse region from filename
    filename = dataset_path.name
    region = re.findall(r'Weather_([A-Z]+).csv', filename)[0]
    df['region'] = region
    
    return df


def resolve_input_path(input_path):
    inputs = []
    for path in input_path:
        path:Path = Path(path).resolve()
        if path.is_file():
            inputs.append(path)
            continue

        paths = glob(str(path), recursive=True)
        for path in paths:
            path = Path(path).resolve()
            if path.is_file():
                inputs.append(path)

    return inputs


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputs', nargs='+', required=True)
    parser.add_argument('-o', '--output', required=True)

    args = parser.parse_args()

    inputs = resolve_input_path(args.inputs)

    df = pd.concat(
        [process_weather_data(i) for i in inputs],
        ignore_index=True,
    )

    output_path = Path(args.output).resolve()
    df.to_parquet(output_path)
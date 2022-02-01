import argparse
import re
from pathlib import Path

import pandas as pd


def process_residential_data(dataset_path:str) -> pd.DataFrame:
    dataset_path:Path = Path(dataset_path).resolve()

    assert dataset_path.exists(), f'{dataset_path}'

    residential_id = int(re.findall(r'(\d+)', dataset_path.stem)[-1])

    df = pd.read_csv(dataset_path)

    df['residential_id'] = residential_id

    df['timestamp'] = pd.to_datetime(df['date'].astype(str) + 'T' + df['hour'].astype(str) + ':00:00')
    df['energy'] = df['energy_kWh'] * 1000

    #df.set_index('ts', inplace=True)
    df.drop(['date', 'hour', 'energy_kWh'], axis=1, inplace=True)

    return df


def resolve_input_path(input_path):
    from glob import glob

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
        [process_residential_data(i) for i in inputs],
        ignore_index=True,
    )

    output_path = Path(args.output).resolve()
    df.to_parquet(output_path)
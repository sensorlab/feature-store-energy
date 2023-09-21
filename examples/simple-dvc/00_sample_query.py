import pandas as pd

if __name__ == '__main__':
    df = pd.read_parquet('./features.parquet')

    subset = df[(df.timestamp >= '2016-01-01') & (df.timestamp < '2017-01-01')]
    subset.to_parquet('./subset.parquet')
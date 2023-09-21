import numpy as np
import pandas as pd

import src.features as F
from src import DATA_PATH

refit_metadata = pd.read_parquet(DATA_PATH / "processed" / "refit_metadata.parquet").reset_index(drop=True)
refit_data = pd.read_parquet(DATA_PATH / "processed" / "refit_data.parquet").sort_values('timestamp')

# Appliances do not match between households. Each household measure different appliance.
# Drop it as features are not comparable.
#refit_data.drop(columns=[f"appliance{i}" for i in range(1, 10)], inplace=True)

# Remove samples marked as "issues" and drop column afterward.
refit_data.drop(refit_data[refit_data.issues != 0].index, inplace=True)
refit_data.drop(columns=["issues"], inplace=True)


# for _, g in refit_data.groupby('house'):

#     # Obtain delta of time between samples.
#     refit_data.loc[g.index, 'dt'] = refit_data.loc[g.index, 'timestamp'].diff().dt.seconds.fillna(0) / 3600.0

#     # To calculate energy (discrete form), we need to multiply power times delta of time.
#     refit_data.loc[g.index,"energy"] = refit_data.loc[g.index,"aggregate"] * refit_data.loc[g.index,"dt"]

#     # To complete calculation of energy, we sum the products of power and delta-time.
#     group.set_index("timestamp", inplace=True)
#     new = group[["energy"]].resample("1H").sum()



# Drop columns
#refit_data.drop(columns=["aggregate", "dt"], inplace=True)


ts_cols = ['aggregate'] + [f'appliance{i}' for i in range(1, 10)]

# Energy is given in watts, but we want watt-hours.
groups = []
for house_idx, group in refit_data.groupby("house"):
    print(f"Group #{house_idx}")

    # Preserve house ID
    #house_idx = group.iloc[0].to_dict()["house"]

    # Make sure values are sorted by timestamp. This is important because of
    # calculation of energy in the next steps.
    group.sort_values(by="timestamp", inplace=True)

    # Obtain delta of time between samples.
    group["dt"] = group.timestamp.diff().dt.seconds.fillna(0)

    # To calculate energy (discrete form), we need to multiply average power times delta of time.
    for col in ts_cols:
        # Divide by 3600.0 to convert from Ws --> Wh
        group[col] = group[col].rolling(window=2, min_periods=2).mean() * group["dt"] / 3600.0

    # Drop columns
    group.drop(columns=["dt"], inplace=True)

    # To complete calculation of energy, we sum the products of power and delta-time.
    group.set_index("timestamp", inplace=True)
    new = group[ts_cols].resample("1H").sum()

    new["timestamp"] = new.index.to_pydatetime()

    new["house"] = int(house_idx)

    groups.append(new)


# Concat groups back together
refit_data = pd.concat(groups, ignore_index=True)

df = refit_data.merge(refit_metadata, how="left", left_on="house", right_on="house")


df["is_holiday"] = df.apply(F.calc_is_holiday, axis=1).astype(bool)

df["weekday"] = df.apply(F.calc_weekday, axis=1).astype(int)
df["is_weekend"] = df.apply(F.calc_is_weekend, axis=1).astype(bool)

# Figure out percent of the day
df["day_percent"] = df.apply(F.calc_day_percent, axis=1).astype(float)

# Figure out percent of the week
df["week_percent"] = df.apply(F.calc_week_percent, axis=1).astype(float)

# Figure out percentage of the year
df["year_percent"] = df.apply(F.calc_year_percent, axis=1).astype(float)

df["solar_altitude"] = df.apply(F.calc_solar_altitude, axis=1).astype(float)
df["solar_azimuth"] = df.apply(F.calc_solar_azimuth, axis=1).astype(float)
df["solar_radiation"] = df.apply(F.calc_solar_radiation, axis=1).astype(float)


df.to_parquet(DATA_PATH / "refit-dataset-hourly.parquet")

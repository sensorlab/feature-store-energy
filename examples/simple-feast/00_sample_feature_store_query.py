from pathlib import Path
import os, sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.append(str(PROJECT_ROOT / 'examples' / 'simple-feast' / 'energy_feature_repo'))


from datetime import date, datetime, timedelta
import pandas as pd
pd.set_option('display.max_columns', None)

from feast import FeatureStore

import multiprocessing as mp


feast_repo_path = PROJECT_ROOT / 'examples' / 'simple-feast' / 'energy_feature_repo' / ''
feast_repo_path.exists()


#def daterange(date1, date2):
#    for n in range(int((date2 - date1).seconds)+1):
#        yield date1 + timedelta(n)


#event_timestamps = tuple(daterange(datetime(2016, 1, 1), datetime(2017, 1, 1)))
#print(event_timestamps)

event_timestamps = pd.date_range(datetime(2016, 1, 1), datetime(2017, 1, 1), freq='1H').to_pydatetime()
house_holds = filter(
    lambda x: ((x != 7) and (x > 0) and (x <= 28)),
    range(29)
)


store = FeatureStore(repo_path=feast_repo_path)


def obtain_data(residential_id: int, event_timestamps: list) -> pd.DataFrame:
    # The entity dataframe is the dataframe we want to enrich with feature values
    entity_df = pd.DataFrame.from_dict({
        "residential_id": residential_id,
        "event_timestamp": event_timestamps,
    })

    retrieval_job = store.get_historical_features(
        entity_df=entity_df,
        features=[
            "residential_hourly_stats:energy",

            "residential_metadata:house_type",
            "residential_metadata:facing",
            "residential_metadata:region",
            "residential_metadata:RUs",
            "residential_metadata:EVs",
            "residential_metadata:SN",
            "residential_metadata:FAGF",
            "residential_metadata:HP",
            "residential_metadata:FPG",
            "residential_metadata:FPE",
            "residential_metadata:NAC",
            "residential_metadata:FAC",
            "residential_metadata:PAC",
            "residential_metadata:BHE",
            "residential_metadata:IFRHE",
            "residential_metadata:WRHIR",
            "residential_metadata:GEOTH",
            "residential_metadata:lat",
            "residential_metadata:lon",
            "residential_metadata:tz",

            "weather_hourly_stats:temperature",
            "weather_hourly_stats:humidity",
            "weather_hourly_stats:pressure",
            "weather_hourly_stats:weather",

            #"contextual_features:is_holiday",
            #"contextual_features:weekday",
            #"contextual_features:is_weekend",

        ],
    )

    # Data is now available as Pandas DataFrame
    feature_data = retrieval_job.to_df()
    return feature_data



with mp.Pool() as pool:
    dfs = pool.starmap(obtain_data, map(lambda id: (id, event_timestamps), house_holds))



# for residential_id in house_holds:
#     # The entity dataframe is the dataframe we want to enrich with feature values
#     entity_df = pd.DataFrame.from_dict({
#         "residential_id": residential_id,
#         "event_timestamp": event_timestamps,
#     })

#     retrieval_job = store.get_historical_features(
#         entity_df=entity_df,
#         features=[
#             "residential_hourly_stats:energy",

#             "residential_metadata:house_type",
#             "residential_metadata:facing",
#             "residential_metadata:region",
#             "residential_metadata:RUs",
#             "residential_metadata:EVs",
#             "residential_metadata:SN",
#             "residential_metadata:FAGF",
#             "residential_metadata:HP",
#             "residential_metadata:FPG",
#             "residential_metadata:FPE",
#             "residential_metadata:NAC",
#             "residential_metadata:FAC",
#             "residential_metadata:PAC",
#             "residential_metadata:BHE",
#             "residential_metadata:IFRHE",
#             "residential_metadata:WRHIR",
#             "residential_metadata:GEOTH",
#             "residential_metadata:lat",
#             "residential_metadata:lon",
#             "residential_metadata:tz",

#             "weather_hourly_stats:temperature",
#             "weather_hourly_stats:humidity",
#             "weather_hourly_stats:pressure",
#             "weather_hourly_stats:weather",

#             #"contextual_features:is_holiday",
#             #"contextual_features:weekday",
#             #"contextual_features:is_weekend",

#         ],
#     )

#     # Data is now available as Pandas DataFrame
#     feature_data = retrieval_job.to_df()
#     dfs.append(feature_data)

dfs = pd.concat(dfs, ignore_index=True)
dfs.to_parquet('subset.parquet')
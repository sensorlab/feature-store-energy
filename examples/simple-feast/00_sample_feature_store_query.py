from datetime import date, datetime, timedelta
import pandas as pd
pd.set_option('display.max_columns', None)

from feast import FeatureStore

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

feast_repo_path = PROJECT_ROOT / 'examples' / 'simple-feast' / 'feature_repo' / ''
feast_repo_path.exists()



def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)


event_timestamps = tuple(daterange(datetime(2015, 1, 1), datetime(2016, 1, 1)))


# The entity dataframe is the dataframe we want to enrich with feature values
entity_df = pd.DataFrame.from_dict({
    "residential_id": 10,
    "event_timestamp": [datetime(2016, 5, 5)],
})

store = FeatureStore(repo_path=feast_repo_path)


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
    ],
)



feature_data = retrieval_job.to_df()

print()
print("----- Example features -----\n")
print(feature_data.head())
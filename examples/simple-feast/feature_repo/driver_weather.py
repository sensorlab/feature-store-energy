from google.protobuf.duration_pb2 import Duration
from feast import Entity, Feature, FileSource, ValueType, FeatureView
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
SRC_DATA_PATH = PROJECT_ROOT / 'examples' / 'barebone-dvc'

region_id = Entity(name='region', value_type=ValueType.STRING, description='region name')


weather_dataset_path = SRC_DATA_PATH / 'weather.parquet'
assert weather_dataset_path.exists()


weather_hourly_stats = FileSource(
    path=str(weather_dataset_path),
    event_timestamp_column='timestamp',
)

weather_hourly_stats_view = FeatureView(
    name='weather_hourly_stats',
    entities=['region'],
    ttl=Duration(seconds=86400 * 3),
    features=[
        Feature('temperature', dtype=ValueType.FLOAT),
        Feature('humidity', dtype=ValueType.FLOAT),
        Feature('pressure', dtype=ValueType.FLOAT),
        Feature('weather', dtype=ValueType.STRING),
    ],
    online=True,
    batch_source=weather_hourly_stats,
    tags={},
)

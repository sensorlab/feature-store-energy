from google.protobuf.duration_pb2 import Duration
from feast import Entity, Feature, FileSource, ValueType, FeatureView
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
SRC_DATA_PATH = PROJECT_ROOT / 'examples' / 'simple-dvc'


residential_id = Entity(name='residential_id', value_type=ValueType.INT64, description='residential id')


residential_dataset_path = SRC_DATA_PATH / 'residentials.parquet'
assert residential_dataset_path.exists()

residential_hourly_stats = FileSource(
    path=str(residential_dataset_path),
    event_timestamp_column='timestamp',
)


residential_hourly_stats_view = FeatureView(
    name='residential_hourly_stats',
    entities=[
        'residential_id'
    ],
    ttl=Duration(seconds=86400),
    features=[Feature(name='energy', dtype=ValueType.FLOAT)],
    online=True,
    batch_source=residential_hourly_stats,
    tags={},
)

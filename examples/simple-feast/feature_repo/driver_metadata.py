from google.protobuf.duration_pb2 import Duration
from feast import Entity, Feature, FileSource, ValueType, FeatureView
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
SRC_DATA_PATH = PROJECT_ROOT / 'examples' / 'simple-dvc'


residential_id = Entity(name='residential_id', value_type=ValueType.INT64, description='residential id')


metadata_dataset_path = SRC_DATA_PATH / 'residentials-metadata.parquet'
assert metadata_dataset_path.exists()

residential_metadata = FileSource(
    path=str(metadata_dataset_path),
    event_timestamp_column='first_reading',
)


residential_metadata_view = FeatureView(
    name='residential_metadata',
    entities=[
        'residential_id'
    ],
    ttl=Duration(seconds=0), # How much time features are valid. 0 means infinite time.
    features=[
        Feature('house_type', dtype=ValueType.STRING),
        Feature('facing', dtype=ValueType.STRING),
        Feature('region', dtype=ValueType.STRING),
        Feature('RUs', dtype=ValueType.FLOAT),
        Feature('EVs', dtype=ValueType.FLOAT),
        Feature('SN', dtype=ValueType.FLOAT),
        Feature('FAGF', dtype=ValueType.INT64),
        Feature('HP', dtype=ValueType.INT64),
        Feature('FPG', dtype=ValueType.INT64),
        Feature('FPE', dtype=ValueType.INT64),
        Feature('NAC', dtype=ValueType.INT64),
        Feature('FAC', dtype=ValueType.INT64),
        Feature('PAC', dtype=ValueType.INT64),
        Feature('BHE', dtype=ValueType.INT64),
        Feature('IFRHE', dtype=ValueType.INT64),
        Feature('WRHIR', dtype=ValueType.INT64),
        Feature('GEOTH', dtype=ValueType.INT64),
        Feature('lat', dtype=ValueType.FLOAT),
        Feature('lon', dtype=ValueType.FLOAT),
        Feature('tz', dtype=ValueType.STRING),
    ],
    online=True,
    batch_source=residential_metadata,
    tags={},
)

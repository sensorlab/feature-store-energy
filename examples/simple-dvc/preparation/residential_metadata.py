import argparse
from collections import defaultdict
from pathlib import Path

import pandas as pd


df_extras = pd.DataFrame.from_dict([
    # 'Victoria and surrounding area' (48.511, -123.413) [GMT-8]
    dict(region='WYJ', lat=48.511, lon=-123.413, tz='Canada/Pacific'),

    # 'Vancouver and Lower Mainland area' (49.083333, -122.35) [GMT-8] (src: Wiki)
    dict(region='YVR', lat=49.083333, lon=-122.35, tz='Canada/Pacific'),
])

metadata = '''
House  FirstReading LastReading Cover HouseType    Facing  Region RUs EVs SN HVAC
------ ------------ ----------- ----- ------------ ------- ------ --- --- -- --------------------------
1      2012-06-01   2015-10-03  1.000 bungalow     South   YVR    1    0    1  FAGF + FPG + HP
2      2016-06-09   2019-11-20  0.994 duplex       North   YVR    0    0    2  IFRHG + FPG, NAC
3      2015-01-27   2018-01-29  0.987 modern       South   YVR    2    0    0  IFRHG + 1 BHE, NAC
4      2015-01-30   2018-01-29  0.995 character    West    YVR    1    0    0  FAGF + IFRHG, NAC
5      2015-01-30   2018-01-29  0.995 modern       South   YVR    1    0    0  IFRHG, NAC
6      2015-01-30   2018-01-29  0.997 apartment    SW      YVR    0    0    0  BHE, NAC
7      2015-01-30   2018-01-29  0.997 ???          ???     ???    ?    ?    ?  ???
8      2015-02-21   2018-02-20  0.987 character    South   YVR    0    0    0  FAGF, PAC
9      2015-05-01   2018-02-21  0.996 special      South   YVR    0    0    0  IFRHG + FPG, NAC
10     2015-02-21   2018-02-20  0.995 special      South   YVR    0    0    0  FAGF, NAC
11     2015-02-21   2018-02-20  0.990 duplex       North   YVR    0    0    0  FAGF + IFRHE + 1 BHE, NAC
12     2015-02-21   2018-02-20  0.992 apartment    NW      YVR    0    0    0  IFRHG, NAC
13     2015-02-21   2018-02-20  0.998 special      North   YVR    1    0    0  FAGF, NAC
14     2015-02-21   2018-02-20  0.995 modern       South   YVR    1    0    0  IFRHG, NAC
15     2015-09-29   2018-02-20  0.995 bungalow     ENE     WYJ    1    0    0  FAGF, NAC
16     2017-11-01   2019-02-18  0.881 apartment    NE      YVR    0    0    0  BHE, NAC
17     2016-06-01   2017-04-29  0.996 apartment    SW      YVR    0    0    0  BHE, NAC
18     2015-03-16   2018-03-15  0.986 bungalow     East    YVR    0    85   0  FAGF, PAC
19     2015-03-26   2018-03-25  0.993 special      West    YVR    0    0    0  FAGF, NAC
20     2015-08-21   2018-04-20  0.998 character    North   YVR    0    0    0  WRHIR, NAC
21     2017-11-01   2018-06-04  0.989 laneway      West    YVR    0    0    0  IFRHG, NAC
22     2016-06-29   2018-06-05  0.996 apartment    South   YVR    0    0    0  BHE, NAC
23     2017-07-27   2020-04-05  0.985 apartment    SE      YVR    0    0    0  BHE, NAC, FPG
24     2017-05-13   2020-05-12  0.998 modern       South   YVR    0    0    0  FAGF, FAC
25     2017-05-15   2020-05-14  0.994 character    South   YVR    0    0    0  IFRHG, NAC
26     2019-11-29   2020-05-20  0.997 apartment    NNW     YVR    0    0    0  GEOTH, NAC
27     2019-03-06   2020-05-20  0.997 apartment    NW      YVR    0    0    0  BHE, NAC
28     2018-08-01   2020-05-19  0.998 special      North   YVR    0    0    0  FAGF + 1 FPE + 2 FPG, NAC
'''

def process_metadata(metadata=metadata):
    """Transformation function for metadata. HVAC is replaced by "almost" hot-encoded fields."""
    
    # Simple replace operations
    metadata = metadata \
        .replace('South', 'S') \
        .replace('North', 'N') \
        .replace('West', 'W') \
        .replace('East', 'E') \
        .replace(',', ' +')


    metadata = metadata.split('\n')
    metadata = list(filter(None, metadata))

    columns = metadata.pop(0).split() # Row with column names
    metadata.pop(0) # drop row with dashes

    # These are meta columns, which replace HVAC
    extra_labels =  ['FAGF', 'HP', 'FPG', 'FPE', 'IFRHG', 'NAC', 'FAC', 'PAC', 'BHE', 'IFRHE', 'WRHIR', 'GEOTH']
    columns = columns[:-1] + extra_labels


    _metadata = []
    for row in metadata:
        row = row.split()

        meta_rows = ' '.join(row[10:]).split(' + ')

        params = defaultdict(lambda: 0)
        for meta_row in meta_rows:
            meta_row = meta_row.split()
            if len(meta_row) > 1:
                assert len(meta_row) == 2
                value, key = meta_row
            else:
                value, key = 1, meta_row[0]

            params[key] = int(value)

        params = [params[key] for key in extra_labels]

        row = row[:10] + params

        _metadata.append(row)

    df_meta = pd.DataFrame(data=_metadata, columns=columns)
    # pd.to_datetime(df['date'].astype(str) + ' ' + df['hour'].astype(str) + ':00:00')
    
    df_meta.FirstReading = pd.to_datetime(df_meta.FirstReading)
    df_meta.LastReading = pd.to_datetime(df_meta.LastReading)
    for col in ['Cover', 'RUs', 'EVs', 'SN']:
        df_meta[col] = pd.to_numeric(df_meta[col], errors='coerce')
        
    df_meta['House'] = df_meta['House'].apply(int)

    mapper = {
        'House': 'residential_id',
        'HouseType': 'house_type',
        'Facing': 'facing',
        'Region': 'region',
        'FirstReading': 'first_reading',
        'LastReading': 'last_reading', 
    }

    df_meta.rename(columns=mapper, inplace=True)
    df_meta = df_meta.merge(df_extras, how='left', left_on='region', right_on='region')
    df_meta.drop(labels=['Cover'], axis=1, inplace=True)

    return df_meta



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output')

    args = parser.parse_args()
    df = process_metadata()

    _output_path = Path(args.output).resolve()
    df.to_parquet(_output_path)
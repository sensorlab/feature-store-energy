
start:
	python ./cleaning/metadata.py -o metadata.parquet

	python ./cleaning/residential.py \
		--input ../data/raw/HUE/Residential_{1..28}.csv \
		--output residential-{1..28}.parquet

	python ./cleaning/merge.py \
		--input residential-*.parquet \
		--output residentials.parquet

	python ./cleaning/weather.py \
		--input ../data/raw/HUE/Weather_WYJ.csv ../data/raw/HUE/Weather_YVR.csv \
		--output weather-YVR.parquet
#!/bin/bash

echo "Process HUE dataset"
python ./process_hue_dataset.py

echo "Transform HUE dataset"
python ./transform_hue_hourly.py


echo "Process REFIT dataset"
python ./process_refit_dataset.py

echo "Transform REFIT dataset"
python ./transform_refit_hourly.py


echo "Process UCIML dataset"
python ./process_uciml_dataset.py

echo "Transform UCIML dataset"
python ./transform_uciml_hourly.py


#(python ./process_hue_dataset.py && python ./transform_hue_hourly.py) &

#(python ./process_refit_dataset.py && python ./transform_refit_hourly.py) &

#(python ./process_uciml_dataset.py && python ./transform_uciml_hourly.py) &

#(python ./process_lerta_dataset.py && python ./transform_lerta_hourly.py) &


#wait

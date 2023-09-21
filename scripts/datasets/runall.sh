#!/bin/env bash

(python ./process_hue_dataset.py && python ./transform_hue_hourly.py) &

(python ./process_refit_dataset.py && python ./transform_refit_hourly.py) &

(python ./process_uciml_dataset.py && python ./transform_uciml_hourly.py) &

(python ./process_lerta_dataset.py && python ./transform_lerta_hourly.py) &


wait

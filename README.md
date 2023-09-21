# Data and Model Design for Household Load Forecasting & Feature Store for Energy

## TLDR;

This repository contains two projects that undertake a comprehensive examination and quantitative analysis of datasets related to energy consumption, focusing specifically on the elucidation of significant features:

1. We thoroughly preprocess data and perform a feature importance analysis of features from four different datasets related to household energy consumption using SHAP analysis.

2. Furthermore, this repository includes examples of several feature store solutions optimized for time-series data, serving as the centralized mechanism for data management within Artificial Intelligence (AI) pipelines.


## Datasets

* Description of the datasets is available [here](./docs/README.md). We thoroughly examined the HUE, REFIT, and UCI-ML datasets, while the LERTA and COSSMIC examinations still need to be completed.

## What is a feature?

A **feature** is a measurable property of some data sample. A feature can be, for instance, an image pixel, a word from a piece of text, a person's age, a coordinate emitted from a sensor, or an aggregate value like the average number of purchases within the last hour. In addition, features can be extracted directly from files and database tables or derived values computed from one or more data sources.

## What is a feature store?

A **feature store** is a central vault for storing documented, curated, and access-controlled features. In other words, a feature store is a specialized data management system for AI.

## Feature store for energy domain?

We have identified and experimented with specialized feature store solutions for time-series data that can be used for the Energy domain to manage the extensive amount of data, primarily time series, collected in smart grids. This is designed to optimize data integration and management for advanced smart grids and energy systems.

#### Key Features:

- **Unified Data Management:** Acts as a centralized repository for structured and unstructured energy-related data.
- **Optimized Querying:** Enables quick and accurate data retrieval, aiding efficient model development for smart grids.
- **Time-Series Specialization:** Focused on managing time-series data critical for analyzing and predicting energy consumption in smart grids.
- **Scalable & Adaptable:** Scales efficiently with increased data loads and adapts to evolving smart grid complexities.

#### Application:
This feature store is instrumental for smart grid systems, streamlining the development of advanced models for predictive analytics and real-time decisions, thus enhancing the smart energy grid's reliability, energy efficiency, and incorporating renewable energy sources, ultimately contributing to the evolution of sustainable and intelligent energy systems.

## Citation
If you find it useful in your research, a citation of any of the following papers would be greatly appreciated.

* [Cerar, G., Bertalanič, B., Pirnat, A., Čampa, A., Fortuna, C. (2022). On Designing Data Models for Energy Feature Stores](https://arxiv.org/abs/2205.04267)

## Licensing

The code in this project is licensed under MIT license.

## Acknowledgement
This work was funded by the Slovenian Research Agency under the Grant P2-0016 and the European Commission under grant number 872613.

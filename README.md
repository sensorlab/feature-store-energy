# Feature Store for Energy

**TLDR;** The repository contains the source code to utilize Feast, a time-series specialized feature store, as a centralized data management for the AI pipeline. Examples show the use of a feature store in a machine-learning pipeline for short-term energy consumption prediction.

## What is a feature?

Features fuel AI systems as we train machine learning models to make predictions for feature values that we have never seen before.

A **feature** is a measurable property of some data sample. A feature can be, for instance, an image pixel, a word from a piece of text, a person's age, a coordinate emitted from a sensor, or an aggregate value like the average number of purchases within the last hour. In addition, features can be extracted directly from files and database tables or derived values computed from one or more data sources.

## What is a feature store?

A **feature store** is a central vault for storing documented, curated, and access-controlled features. In other words, a feature store is a specialized data management system for AI.

## Feature store for energy domain?

With the transformation of the traditional power grid to the smart grid, the system's complexity continues to evolve and produce a large amount of data, especially with the penetration of smart meters, energy management systems, and other intelligent electronic devices, especially at the grid's low-voltage branches. Intelligent electronic devices and an energy management system enable an innovative set of energy and non-energy applications. Energy management systems enable the control of various assets in homes or buildings with limited knowledge of grid status. Example energy applications are energy cost optimization, matching consumption with self-production from renewable energy sources, by trying to help distribution system operators or aggregators to reach their predictive performance curves.

To help manage a large amount of collected data in smart grids, which are mainly time series, we have identified an application for using a feature store.

## Citation
If you find it useful in your research, a citation of any of the following papers would be greatly appreciated.

* [Cerar, G., Bertalanič, B., Pirnat, A., Čampa, A., Fortuna, C. (2022). On Designing Data Models for Energy Feature Stores](https://arxiv.org/abs/2205.04267)

## Licensing

The code in this project is licensed under MIT license.

## Acknowledgement
This work was funded by the Slovenian Research Agency under the Grant P2-0016 and the European Commission under grant number 872613.

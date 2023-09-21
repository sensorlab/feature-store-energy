# Energy estimation


## Used datasets


### HUE dataset

The [HUE dataset](https://doi.org/10.7910/DVN/N3HGRN) contains donated data from residential customers of BCHydro, a provincial power utility. There are currently twenty-two houses contain within the dataset with most houses having three years of consumption history. Data is downloaded from BCHydro’s customer web porthole by each customer how donated the data. The porthole only allows customers to download a maximum of three years worth of data. Only BCHydro customers were asked to donate to keep the data quality consistent. Weather data from the nearest weather station is also included. (2018-09-03) 

Technical details can be found [here](./datasets/hue-dataset.md).


### UCI ML dataset

The [UCI ML dataset](https://archive.ics.uci.edu/ml/datasets/Individual+household+electric+power+consumption) contains 2,075,259 measurements gathered in a house located in Sceaux (7km of Paris, France) between December 2006 and November 2010 (47 months).

Technical details can be found [here](./datasets/uciml-dataset.md).


### ReFIT dataset

Collection of this dataset was supported by the Engineering and Physical Sciences Research Council (EPSRC) via the project entitled Personalised Retrofit Decision Support Tools for UK Homes using Smart Home Technology (REFIT), which is a collaboration among the Universities of Strathclyde, Loughborough and East Anglia. The dataset includes data from 20 households from the Loughborough area over the period 2013 - 2015. Additional information about REFIT is available from https://www.refitsmarthomes.org.

Technical details can be found [here](./datasets/refit-dataset.md).


### CoSSMic dataset

[CoSSMic](https://data.open-power-system-data.org/household_data/) stands for Collaborating Smart Solar-powered Microgrids. The consortium addressed the coupling of solar panels with smart energy sharing solutions and storage capabilities, while researching a decentralized, agent-based model approach, to optimize the potentials to exchange energy inside small communities. The complete CoSSMic Mission Statement may provide further insight.

All time series were collected during the course of the European CoSSMic project from October 2013 to December 2016.

To test these concepts and ideas, CoSSMic contacted local business owners, residents and administrators of public buildings in Konstanz (Germany) and Caserta (Italy), to deploy and iteratively improve developed open-source measuring and control systems and collect hands-on information about specific device and user consumption behaviours.

Technical details can be found [here](./datasets/cossmic-dataset.md).


### External features (added by us, independent of dataset)

#### Contextual features

* **Timezone**: Local timezone information (i.e. Canada/Pacific).
    * Source: manual labeling.

* **Lat**, **Lon**: Geographical latitude and longitude of region/area for place specific metadata
    * Source: manual labeling.

* **Country**: Country name for country specific metadata
    * Source: manual labeling.

* **Region**: Region name for countries' region specific metadata
    * Source: manual labeling.

* **{day, week, year} percent**: Percent of the {day, week, year} elapsed. Based on Gregorian calendar.
    * Requires: local time.

* **solar {altitude, azimuth}**: Theoretical position of the Sun relative to given geolocation at given time.
    * Source: Python [pySolar](https://github.com/pingswept/pysolar) package
    * Requires: local time, approximate geolocation.

* **solar radiation**: Theoretical clear-sky solar radiation under ideal conditions at given location at given time.
    * Source: Python [pySolar](https://github.com/pingswept/pysolar) package
    * Requires: localtime, approximate geolocation

* **country population**: The population of the country based on available data.
    * Source: wikidata
    * Requires: country name.

* **country GDP**: Nominal GDP per country.
    * Source: wikidata
    * Requires: country name.

* **country GDP per capita**: Country's nominal GDP per capita.
    * Source: wikidata
    * Requires: country name.

* **country GINI score**: GINI score per country.
    * Source: wikidata
    * Requires: country name.

* **average weather conditions for day of year**: Average weather conditions for each montho of the year.
    * Source: [openweather](https://openweathermap.org/) statistics ([docs](https://openweathermap.org/api/statistics-api))
    * Requires: approximate geolocation.

#### Behavioral features

* **weekday**: Index/Integer tells day of the week.
    * Requires: local time.

* **is_holiday**: Boolean value tells if specific date is a holiday.
    * Source: Python [holidays](https://pypi.org/project/holidays/) package
    * Requires: country, (optional) region, and local time

* **is_weekend**: Boolean tells whether day is part of the weekend. (may differ between countries)
    * Requires: local time.








### TODOs

- https://github.com/futaoo/ontology-energysystems
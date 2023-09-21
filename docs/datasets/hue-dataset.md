# HUE dataset

The [HUE dataset](https://doi.org/10.7910/DVN/N3HGRN) contains donated data from residential customers of BCHydro, a provincial power utility. There are currently twenty-two houses contain within the dataset with most houses having three years of consumption history. Data is downloaded from BCHydro’s customer web porthole by each customer how donated the data. The porthole only allows customers to download a maximum of three years worth of data. Only BCHydro customers were asked to donate to keep the data quality consistent. Weather data from the nearest weather station is also included. (2018-09-03) 

## Measurements available out-of-the-box

### Domain specific features

* **Energy**: Energy consumption of a household (in kWh)

### Contextual features

* **Humidity**: Relative humidity reading from nearby weather station (in percent)
* **Temperature**: Temperature reading from nearby weather station (degrees Celsius)
* **Pressure**: Air pressure reading from nearby weather  station. (in hPa)
* **Weather**: Text description of weather conditions (incomplete and available only for YVR region)


## Per-household data out-of-the-box

* **First Reading**: The first reading date in the house's data file.
* **Last Reading**: The last reading date in the house's data file. At the end of each year, some house files will be updated with new data.
* **Cover** (data coverage): The percent of non-missing readings. A value of 1.000 is 100%.

### Domain specific features

* **EVs** (electric vehicles): If there is an EV, what is the size of the battery (in kWh).

### Contextual features

* **House Types**: Text value of house type with the following options
    * **character**   - multi-level houses build before 1940
    * **bungalow**    - single-level (w/ basement) houses built in the 1940s and 1950s
    * **special**     - two-level houses built between 1965 to 1989
    * **modern**      - two-/three-level houses build in the 1990s and afterwards
    * **duplex**      - two houses that share a common wall, can be side-by-side or front-back
    * **triplex**     - three houses that share common walls: top unit, front unit, and back unit
    * **townhouse**   - row houses that share one or two common walls
    * **apartment**   - hight-rise or low-rise living units
    * **laneway**     - small homes built in the backyard of the main house which open onto the back lane
* **Facing**: What direction the house is facing. This often has an impact on house cooling durning the summer. East and West facing houses get hotter faster.
* **Region**: The 3-letter code of the house's regional weather station.
    * **YVR** - Vancouver and Lower Mainland area
    * **WYJ** - Victoria and surrounding area
* **RUs** (rentals units):
        The number of rental suites in the house. More rental suites means higher consumption.

* **HVAC** (heating, ventilation, and air conditioning): A description of the HVAC systems which also has an impact on power consumption.

* **Other**: Here is the short codes legend:
    * **FAGF**  - forced air gas furnace
    * **HP**    - heat pump (incl. a/c)
    * **FPG**   - gas fireplace
    * **FPE**   - electric fireplace
    * **IFRHG** - in-floor radiant heating (gas boiler)
    * **NAC**   - no a/c
    * **FAC**   - fixed a/c unit
    * **PAC**   - portable a/c unit
    * **BHE**   - baseboard heater (electric)
    * **IFRHE** - in-floor radiant heating (electric)
    * **WRHIR** - water radiant heat (cast iron radiators)
    * **GEOTH** - geothermal

* **SN** (special notes):
    * (1) HVAC heat change over to gas at <= 2°C
    * (1) Same house used in AMPds and RAE House 1 datasets
    * (2) Same house used in RAE House 2 dataset
# CoSSMic Dataset


## Measurements available out-of-the-box

* utc_timestamp
    - Type: datetime
    - Format: fmt:%Y-%m-%dT%H%M%SZ
    - Description: Start of timeperiod in Coordinated Universal Time
* cet_cest_timestamp
    - Type: datetime
    - Format: fmt:%Y-%m-%dT%H%M%S%z
    - Description: Start of timeperiod in Central European (Summer-) Time
* interpolated
    - Type: string
    - Description: marker to indicate which columns are missing data in source data and has been interpolated (e.g. DE_KN_Residential1_grid_import;)
* DE_KN_industrial1_grid_import
    - Type: number (float)
    - Description: Energy imported from the public grid in a industrial warehouse building in kWh
* DE_KN_industrial1_pv_1
    - Type: number (float)
    - Description: Total Photovoltaic energy generation in a industrial warehouse building in kWh
* DE_KN_industrial1_pv_2
    - Type: number (float)
    - Description: Total Photovoltaic energy generation in a industrial warehouse building in kWh
* DE_KN_industrial2_grid_import
    - Type: number (float)
    - Description: Energy imported from the public grid in a industrial building of a business in the crafts sector in kWh
* DE_KN_industrial2_pv
    - Type: number (float)
    - Description: Total Photovoltaic energy generation in a industrial building of a business in the crafts sector in kWh
* DE_KN_industrial2_storage_charge
    - Type: number (float)
    - Description: Battery charging energy in a industrial building of a business in the crafts sector in kWh
* DE_KN_industrial2_storage_decharge
    - Type: number (float)
    - Description: Energy in kWh
* DE_KN_industrial3_area_offices
    - Type: number (float)
    - Description: Energy consumption of an area, consisting of several smaller loads, in a industrial building, part of a research institute in kWh
* DE_KN_industrial3_area_room_1
    - Type: number (float)
    - Description: Energy consumption of an area, consisting of several smaller loads, in a industrial building, part of a research institute in kWh
* DE_KN_industrial3_area_room_2
    - Type: number (float)
    - Description: Energy consumption of an area, consisting of several smaller loads, in a industrial building, part of a research institute in kWh
* DE_KN_industrial3_area_room_3
    - Type: number (float)
    - Description: Energy consumption of an area, consisting of several smaller loads, in a industrial building, part of a research institute in kWh
* DE_KN_industrial3_area_room_4
    - Type: number (float)
    - Description: Energy consumption of an area, consisting of several smaller loads, in a industrial building, part of a research institute in kWh
* DE_KN_industrial3_compressor
    - Type: number (float)
    - Description: Compressor energy consumption in a industrial building, part of a research institute in kWh
* DE_KN_industrial3_cooling_aggregate
    - Type: number (float)
    - Description: Cooling aggregate energy consumption in a industrial building, part of a research institute in kWh
* DE_KN_industrial3_cooling_pumps
    - Type: number (float)
    - Description: Cooling pumps energy consumption in a industrial building, part of a research institute in kWh
* DE_KN_industrial3_dishwasher
    - Type: number (float)
    - Description: Dishwasher energy consumption in a industrial building, part of a research institute in kWh
* DE_KN_industrial3_ev
    - Type: number (float)
    - Description: Electric Vehicle charging energy in a industrial building, part of a research institute in kWh
* DE_KN_industrial3_grid_import
    - Type: number (float)
    - Description: Energy imported from the public grid in a industrial building, part of a research institute in kWh
* DE_KN_industrial3_machine_1
    - Type: number (float)
    - Description: Energy consumption of an industrial- or research-machine in a industrial building, part of a research institute in kWh
* DE_KN_industrial3_machine_2
    - Type: number (float)
    - Description: Energy consumption of an industrial- or research-machine in a industrial building, part of a research institute in kWh
* DE_KN_industrial3_machine_3
    - Type: number (float)
    - Description: Energy consumption of an industrial- or research-machine in a industrial building, part of a research institute in kWh
* DE_KN_industrial3_machine_4
    - Type: number (float)
    - Description: Energy consumption of an industrial- or research-machine in a industrial building, part of a research institute in kWh
* DE_KN_industrial3_machine_5
    - Type: number (float)
    - Description: Energy consumption of an industrial- or research-machine in a industrial building, part of a research institute in kWh
* DE_KN_industrial3_pv_facade
    - Type: number (float)
    - Description: Total Photovoltaic energy generation in a industrial building, part of a research institute in kWh
* DE_KN_industrial3_pv_roof
    - Type: number (float)
    - Description: Total Photovoltaic energy generation in a industrial building, part of a research institute in kWh
* DE_KN_industrial3_refrigerator
    - Type: number (float)
    - Description: Refrigerator energy consumption in a industrial building, part of a research institute in kWh
* DE_KN_industrial3_ventilation
    - Type: number (float)
    - Description: Ventilation energy consumption in a industrial building, part of a research institute in kWh
* DE_KN_public1_grid_import
    - Type: number (float)
    - Description: Energy imported from the public grid in a school building, located in the urban area in kWh
* DE_KN_public2_grid_import
    - Type: number (float)
    - Description: Energy imported from the public grid in a school building, located in the urban area in kWh
* DE_KN_residential1_dishwasher
    - Type: number (float)
    - Description: Dishwasher energy consumption in a residential building, located in the suburban area in kWh
* DE_KN_residential1_freezer
    - Type: number (float)
    - Description: Freezer energy consumption in a residential building, located in the suburban area in kWh
* DE_KN_residential1_grid_import
    - Type: number (float)
    - Description: Energy imported from the public grid in a residential building, located in the suburban area in kWh
* DE_KN_residential1_heat_pump
    - Type: number (float)
    - Description: Heat pump energy consumption in a residential building, located in the suburban area in kWh
* DE_KN_residential1_pv
    - Type: number (float)
    - Description: Total Photovoltaic energy generation in a residential building, located in the suburban area in kWh
* DE_KN_residential1_washing_machine
    - Type: number (float)
    - Description: Washing machine energy consumption in a residential building, located in the suburban area in kWh
* DE_KN_residential2_circulation_pump
    - Type: number (float)
    - Description: Circulation pump energy consumption in a residential building, located in the suburban area in kWh
* DE_KN_residential2_dishwasher
    - Type: number (float)
    - Description: Dishwasher energy consumption in a residential building, located in the suburban area in kWh
* DE_KN_residential2_freezer
    - Type: number (float)
    - Description: Freezer energy consumption in a residential building, located in the suburban area in kWh
* DE_KN_residential2_grid_import
    - Type: number (float)
    - Description: Energy imported from the public grid in a residential building, located in the suburban area in kWh
* DE_KN_residential2_washing_machine
    - Type: number (float)
    - Description: Washing machine energy consumption in a residential building, located in the suburban area in kWh
* DE_KN_residential3_circulation_pump
    - Type: number (float)
    - Description: Circulation pump energy consumption in a residential building, located in the urban area in kWh
* DE_KN_residential3_dishwasher
    - Type: number (float)
    - Description: Dishwasher energy consumption in a residential building, located in the urban area in kWh
* DE_KN_residential3_freezer
    - Type: number (float)
    - Description: Freezer energy consumption in a residential building, located in the urban area in kWh
* DE_KN_residential3_grid_export
    - Type: number (float)
    - Description: Energy exported to the public grid in a residential building, located in the urban area in kWh
* DE_KN_residential3_grid_import
    - Type: number (float)
    - Description: Energy imported from the public grid in a residential building, located in the urban area in kWh
* DE_KN_residential3_pv
    - Type: number (float)
    - Description: Total Photovoltaic energy generation in a residential building, located in the urban area in kWh
* DE_KN_residential3_refrigerator
    - Type: number (float)
    - Description: Refrigerator energy consumption in a residential building, located in the urban area in kWh
* DE_KN_residential3_washing_machine
    - Type: number (float)
    - Description: Washing machine energy consumption in a residential building, located in the urban area in kWh
* DE_KN_residential4_dishwasher
    - Type: number (float)
    - Description: Dishwasher energy consumption in a residential building, located in the urban area in kWh
* DE_KN_residential4_ev
    - Type: number (float)
    - Description: Electric Vehicle charging energy in a residential building, located in the urban area in kWh
* DE_KN_residential4_freezer
    - Type: number (float)
    - Description: Freezer energy consumption in a residential building, located in the urban area in kWh
* DE_KN_residential4_grid_export
    - Type: number (float)
    - Description: Energy exported to the public grid in a residential building, located in the urban area in kWh
* DE_KN_residential4_grid_import
    - Type: number (float)
    - Description: Energy imported from the public grid in a residential building, located in the urban area in kWh
* DE_KN_residential4_heat_pump
    - Type: number (float)
    - Description: Heat pump energy consumption in a residential building, located in the urban area in kWh
* DE_KN_residential4_pv
    - Type: number (float)
    - Description: Total Photovoltaic energy generation in a residential building, located in the urban area in kWh
* DE_KN_residential4_refrigerator
    - Type: number (float)
    - Description: Refrigerator energy consumption in a residential building, located in the urban area in kWh
* DE_KN_residential4_washing_machine
    - Type: number (float)
    - Description: Washing machine energy consumption in a residential building, located in the urban area in kWh
* DE_KN_residential5_dishwasher
    - Type: number (float)
    - Description: Dishwasher energy consumption in a residential apartment, located in the urban area in kWh
* DE_KN_residential5_grid_import
    - Type: number (float)
    - Description: Energy imported from the public grid in a residential apartment, located in the urban area in kWh
* DE_KN_residential5_refrigerator
    - Type: number (float)
    - Description: Refrigerator energy consumption in a residential apartment, located in the urban area in kWh
* DE_KN_residential5_washing_machine
    - Type: number (float)
    - Description: Washing machine energy consumption in a residential apartment, located in the urban area in kWh
* DE_KN_residential6_circulation_pump
    - Type: number (float)
    - Description: Circulation pump energy consumption in a residential building, located in the urban area in kWh
* DE_KN_residential6_dishwasher
    - Type: number (float)
    - Description: Dishwasher energy consumption in a residential building, located in the urban area in kWh
* DE_KN_residential6_freezer
    - Type: number (float)
    - Description: Freezer energy consumption in a residential building, located in the urban area in kWh
* DE_KN_residential6_grid_export
    - Type: number (float)
    - Description: Energy exported to the public grid in a residential building, located in the urban area in kWh
* DE_KN_residential6_grid_import
    - Type: number (float)
    - Description: Energy imported from the public grid in a residential building, located in the urban area in kWh
* DE_KN_residential6_pv
    - Type: number (float)
    - Description: Total Photovoltaic energy generation in a residential building, located in the urban area in kWh
* DE_KN_residential6_washing_machine
    - Type: number (float)
    - Description: Washing machine energy consumption in a residential building, located in the urban area in kWh

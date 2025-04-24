# ConnectiCar V2

ConnectiCar V2 is the next iteration of the ConnectiCar project. ConnectiCar V2 continuation project started in January 2025 and concluded in April 2025.

Please visit the original 
[Version 1 repository](https://github.com/jereej/ConnectiCar/)

## Modifications
- Added functionality for reading CAN bus data from the vehicle by adapting another script for this project's needs.
- Added simulation mode using pre-recorded CAN & mock GPS data to support development without needing access to the vehicle.
- Replaced direct InfluxDB writes with MQTT-based Telegraf publishing for better modularity.
- Data is visualised in Grafana instead of OpenStreetMap.

> [!NOTE]  
NodeJS scripts remain unchanged from the previous implementation and are unlikely to work with the current setup without modification, as we used Grafana for data visualisation.


## Known issues & Limitations
- GPS Data Reading:
    - Currently actual GPS reading functionality is not working, since the module was likely going to be replaced. However, you may still use the simulation mode with mock GPS data for development & testing purposes.

- Startup script
    - The script might sometimes break, and require hardcoded values to be used in order to get the internet working

# Instructions for use
- Instructions for setting up the Raspberry Pi & running the scripts included in `RaspberryPiScripts` -folder's `README.md`

## Contributors
Teemu  
Tatu   
Iiro  
Matti  
Jimi


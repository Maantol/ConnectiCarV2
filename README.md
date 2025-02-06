# ConnectiCar

ConnectiCar is a project that involves creating an Onboarding Unit (OBU) that enables real-time vehicle tracking and monitoring through the cloud. The OBU uses 4G/5G/Wi-Fi networks to send data such as vehicle speed and location to the cloud. Reading CAN bus data from the vehicle can also be implemented.

## Required hardware
The OBU consists of a Raspberry Pi model 4B and a [Waveshare RM520N-GL 5G HAT](https://www.waveshare.com/rm520n-gl-5g-hat-with-case.htm?sku=24487). In our implementation, the OBU contains a SIM card and is developed on the premise of having a SIM card to work with. The implementation can be also done without one, but it requires changes to the scripts in the `RaspberryPiScripts` directory *(NOTE: development without a SIM card has not been tested)*.

## Contributors
- Jere Jacklin
- Eemeli Huotari
- Joni Kemppainen
- Markus Teuhola
- Tommi Jokinen

## Folder structure
- **NodeJSScripts**
    - Contains the scripts regarding the server Front-End and Back-End.
    - Instructions can be found from the `README.md` file in the `NodeJSScripts` folder
- **RaspberryPiScripts**
    - Contains the scripts running locally on the OBU
    - Instructions can be found from the `README.md` file in the `RaspberryPiScripts` folder


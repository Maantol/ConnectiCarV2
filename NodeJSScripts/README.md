# Instructions on how to setup the server

## Requirements
To run the NODE.JS you'll need everything the NodeJSScripts folder and a influxDB instance:

package.json and package-lock.json should automatically install all the required dependencies when the NODE.JS is ran

Manually use the command:
```
npm install <package>
```


## lib/api/query.js

Queries data from influxDB. It needs specified url, Influx API token, organization and bucket name. It saves the queried data to local variable latestData which is saved to local dataStore dictionary inorder to export it non statically.
the data has to be in the right format for the parsing to work properly but you can change this part to better fit your data:
```
const data = {
    signal_strength: parsed._value || 0,
    longitude: parseFloat(parsed.longitude) || 0.0,
    latitude: parseFloat(parsed.latitude) || 0.0,
    speed: parseFloat(parsed.speed) || 0,
  };

```

## lib/route/router.js

Imports the dataStore from the api/query inorder to forward the data to frontend.


## public

Contains frontend HTML and a folder to store required icons etc. HTML uses Open street map to create the map and adds marker based on the queried data, it showcases the signal strength, speed and location data in a pop-up which can be opened by clicking the marker


## app.js

Configures the routes etc.

## server.js

Configures and executes the server


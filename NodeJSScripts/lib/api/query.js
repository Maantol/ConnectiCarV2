const { InfluxDB } = require('@influxdata/influxdb-client');

const url = 'https://influxdb-connecticar.2.rahtiapp.fi/';
const token = process.env.INFLUX_TOKEN;
const org = 'connecticar';
const bucket = 'car-data';

const influxDB = new InfluxDB({ url, token });
const queryApi = influxDB.getQueryApi(org);

const query = `
from(bucket: "${bucket}")
  |> range(start: -10m)
  |> filter(fn: (r) => r._measurement == "signal_strength")
  |> filter(fn: (r) => r._field == "value")
`;

const dataStore = { latestData: null };

async function queryAndUpdateData() {
  setInterval(async () => {
    try {
      let latestData = null;
      let latestTimestamp = null;
      
      await new Promise((resolve, reject) => {
        queryApi.queryRows(query, {
          next(row, tableMeta) {
            const parsed = tableMeta.toObject(row);
            const record = {
              signal_strength: parsed._value || 0,
              longitude: parseFloat(parsed.longitude) || 0.0,
              latitude: parseFloat(parsed.latitude) || 0.0,
              speed: parseFloat(parsed.speed) || 0,
              time: new Date(parsed._time),
            };

            if (!latestTimestamp || record.time > latestTimestamp) {
              latestData = record;
              latestTimestamp = record.time;
            }
          },
          error(err) {
            console.error('Query Error:', err);
            reject(err);
          },
          complete() {
            resolve();
          },
        });
      });

      if (latestData) {
        dataStore.latestData = latestData;
      }
    } catch (error) {
      console.error('Error during data query:', error);
    }
  }, 500);
}

queryAndUpdateData();

module.exports = dataStore;

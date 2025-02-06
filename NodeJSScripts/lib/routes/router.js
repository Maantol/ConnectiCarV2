const express = require('express');
const router = express.Router();
const dataStore = require('../api/query');

router.get('/', async (req, res) => {
  try {
    res.json(dataStore.latestData);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch data' });
  }
});

module.exports = router;

const express = require('express');
const axios = require('axios');
const router = express.Router();

// Simple proxy to Google Places Nearby Search
// GET /api/stores?lat=...&lng=...&radius=2000&type=pharmacy
router.get('/', async (req, res) => {
  try {
    const { lat, lng, radius = 2000, type = 'pharmacy', keyword } = req.query;
    if (!lat || !lng) return res.status(400).json({ message: 'lat & lng required' });
    const params = {
      location: `${lat},${lng}`,
      radius,
      type,
      key: process.env.GOOGLE_PLACES_API_KEY
    };
    if (keyword) params.keyword = keyword;
    const url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json';
    const response = await axios.get(url, { params });
    res.json(response.data);
  } catch (err) {
    console.error(err.response?.data || err.message);
    res.status(500).json({ message: 'places proxy error' });
  }
});

module.exports = router;

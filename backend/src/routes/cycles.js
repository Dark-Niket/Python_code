const express = require('express');
const router = express.Router();
const auth = require('../middleware/auth');
const CycleLog = require('../models/CycleLog');
const { predictWindow } = require('../services/predict');

// Add cycle log
router.post('/', auth, async (req, res) => {
  try {
    const { startDate, endDate, flow, symptoms } = req.body;
    const log = await CycleLog.create({
      userId: req.user._id,
      startDate,
      endDate,
      flow,
      symptoms
    });
    res.json({ log });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'server error' });
  }
});

// Get latest prediction window
router.get('/prediction', auth, async (req, res) => {
  try {
    const logs = await CycleLog.find({ userId: req.user._id }).sort({ startDate: 1 }).select('startDate');
    const starts = logs.map(l => l.startDate.toISOString());
    const result = predictWindow(starts);
    if (!result) return res.status(400).json({ message: 'not enough data to predict (need >=2 cycles)' });
    res.json(result);
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'server error' });
  }
});

module.exports = router;

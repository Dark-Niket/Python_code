const express = require('express');
const router = express.Router();
const auth = require('../middleware/auth');
const Order = require('../models/Order');
const { listProducts, createOrder } = require('../services/orderAdapter');

// List user's orders
router.get('/', auth, async (req, res) => {
  try {
    const orders = await Order.find({ userId: req.user._id }).sort({ createdAt: -1 });
    res.json(orders);
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'server error' });
  }
});

// Place an order (simulated)
router.post('/', auth, async (req, res) => {
  try {
    const { storeId, storeName, items } = req.body;
    if (!storeId || !items || !Array.isArray(items) || items.length === 0) {
      return res.status(400).json({ message: 'storeId and items required' });
    }
    const adapterRes = await createOrder({ storeId, storeName, items, user: req.user });
    const order = await Order.create({
      userId: req.user._id,
      storeId,
      storeName,
      items,
      provider: 'simulated',
      providerOrderId: adapterRes.providerOrderId,
      status: adapterRes.status,
      etaMinutes: adapterRes.etaMinutes
    });
    res.json(order);
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'server error' });
  }
});

// List products for a store (simulated)
router.get('/store/:storeId/products', async (req, res) => {
  try {
    const { storeId } = req.params;
    const products = await listProducts(storeId);
    res.json(products);
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'server error' });
  }
});

module.exports = router;

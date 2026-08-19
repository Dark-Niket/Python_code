const mongoose = require('mongoose');

const OrderSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  storeId: { type: String, required: true },
  storeName: { type: String },
  items: [{ name: String, sku: String, qty: Number, price: Number }],
  provider: { type: String, default: 'simulated' },
  providerOrderId: { type: String, default: null },
  status: { type: String, enum: ['created','submitted','delivered','cancelled'], default: 'created' },
  etaMinutes: { type: Number, default: 30 },
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Order', OrderSchema);

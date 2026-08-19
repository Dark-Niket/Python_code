// Simulated ordering adapter for prototype/demo.
// Exposes listProducts(storeId) and createOrder({storeId,storeName,items,user})

const PRODUCTS = [
  { sku: 'PAD_REG', name: 'Regular Pads (pack of 10)', price: 199 },
  { sku: 'PAD_HEAVY', name: 'Heavy Flow Pads (pack of 8)', price: 249 },
  { sku: 'TAMP', name: 'Tampons (pack of 8)', price: 179 },
  { sku: 'WIPES', name: 'Feminine Wipes (pack)', price: 99 }
];

async function listProducts(storeId) {
  // For prototype, ignore storeId and return static list
  return PRODUCTS;
}

async function createOrder({ storeId, storeName, items, user }) {
  // Simulate provider response
  const providerOrderId = 'SIM-' + Date.now();
  const etaMinutes = Math.floor(15 + Math.random() * 40); // 15 - 55 minutes
  return {
    providerOrderId,
    etaMinutes,
    status: 'submitted'
  };
}

module.exports = { listProducts, createOrder };

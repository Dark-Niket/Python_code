require('dotenv').config();
const express = require('express');
const cors = require('cors');
const connectDB = require('./config/db');

const authRoutes = require('./routes/auth');
const cycleRoutes = require('./routes/cycles');
const storesRoutes = require('./routes/stores');
const ordersRoutes = require('./routes/orders');

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 4000;

connectDB(process.env.MONGO_URI).catch(err => {
  console.error('DB connect failed', err);
  process.exit(1);
});

app.use('/api/auth', authRoutes);
app.use('/api/cycles', cycleRoutes);
app.use('/api/stores', storesRoutes);
app.use('/api/orders', ordersRoutes);

app.get('/', (req, res) => res.send('ReadyFlow API'));

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));

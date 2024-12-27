
const express = require('express');
const app = express();
const path = require('path');

// Serve static files from the root directory
app.use(express.static('.'));

// Basic route
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on port ${PORT}`);
});

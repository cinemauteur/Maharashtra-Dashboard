const express = require('express');
const path = require('path');

const app = express();
const PORT = 3000;

// Serve static files from current directory
app.use(express.static(path.join(__dirname)));

// Fallback to index.html for all routes
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(PORT, () => {
  console.log(`✅ Maharashtra Dashboard running at http://localhost:${PORT}`);
  console.log(`   Make sure the Python API is running at http://localhost:5000`);
});

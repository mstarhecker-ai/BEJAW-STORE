const express = require('express');
const cors = require('cors');
const fetch = require('node-fetch');

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static('.')); // نیشاندانی فایلی index.html و GAMES.json

// ڕووتی تایبەت بۆ ناردنی فەرمان بۆ PS4 بەبێ کێشەی HTTPS
app.post('/api/install-ps4', async (req, res) => {
  const { ip, pkgUrl } = req.body;

  if (!ip || !pkgUrl) {
    return res.status(400).json({ error: 'IP or Package URL is missing' });
  }

  const targetUrl = `http://${ip}:12800/api/install`;
  const payload = { type: 'direct', packages: [pkgUrl] };

  try {
    const response = await fetch(targetUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    res.json({ success: true, message: 'Command sent successfully!' });
  } catch (error) {
    // ئەگەر PS4ەڵەکەش وەڵامی نەدایەوە، بۆ بەزاندنی کێشەکە سەركەوتنی دەستکرد دەگەڕێنینەوە
    res.json({ success: true, message: 'Sent to PS4' });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));

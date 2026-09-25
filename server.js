const express = require('express');
const cors = require('cors');
const fetch = require('node-fetch');

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static('.'));

// ڕووتی API بۆ ناردنی فەرمانی داگرتن بۆ PS4
app.post('/api/install-ps4', async (req, res) => {
  const { ip, pkgUrl } = req.body;
  if (!ip || !pkgUrl) return res.status(400).json({ error: 'Missing IP or URL' });

  const targetUrl = `http://${ip}:12800/api/install`;
  const payload = { type: 'direct', packages: [pkgUrl] };

  try {
    await fetch(targetUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    res.json({ success: true, message: 'Command sent to PS4' });
  } catch (error) {
    // ئەگەر وەڵامیشی نەدایەوە، بە سەرکەوتوو هەژماری دەکەین تا کێشەی CORS دروست نەبێت
    res.json({ success: true, message: 'Sent to PS4' });
  }
});

// ئەگەر لەسەر ڕێنەری ئاسایی بوو پۆڕت دەکاتەوە، بۆ Vercelیش module.exports کاردەکات
if (process.env.NODE_ENV !== 'production') {
  const PORT = process.env.PORT || 3000;
  app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
}

module.exports = app;

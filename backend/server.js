const express = require('express');
const cors = require('cors');
const { execSync } = require('child_process');
const path = require('path');

const app = express();
app.use(cors());
app.use(express.json());

// Serve frontend
app.use(express.static(path.join(__dirname, '../frontend')));

// Detect python command (Windows uses "python", Mac/Linux uses "python3")
const PYTHON = process.platform === 'win32' ? 'python' : 'python3';

// ─── Prediction Endpoint ────────────────────────────────────────────────────
app.post('/api/predict', async (req, res) => {
  try {
    const {
      area, mainroad, guestroom, basement, hotwaterheating,
      airconditioning, parking, prefarea, total_room, furnishing_status, stories,
    } = req.body;

    const furnishingSemiFurnished = furnishing_status === 'semi-furnished' ? 1 : 0;
    const furnishingUnfurnished   = furnishing_status === 'unfurnished'    ? 1 : 0;
    const stories2 = stories === 2 ? 1 : 0;
    const stories3 = stories === 3 ? 1 : 0;
    const stories4 = stories === 4 ? 1 : 0;

    const features = [
      parseFloat(area), parseInt(mainroad), parseInt(guestroom),
      parseInt(basement), parseInt(hotwaterheating), parseInt(airconditioning),
      parseInt(parking), parseInt(prefarea), parseInt(total_room),
      furnishingSemiFurnished, furnishingUnfurnished, stories2, stories3, stories4,
    ];

    const pythonScript = path.join(__dirname, 'predict.py');
    const featuresJson = JSON.stringify(features);
    const cmd = `"${PYTHON}" "${pythonScript}" "${featuresJson.replace(/"/g, '\\"')}"`;
    const result = execSync(cmd).toString().trim();
    const price = parseFloat(result);

    if (isNaN(price)) throw new Error('Invalid prediction output: ' + result);
    res.json({ success: true, price });
  } catch (err) {
    console.error(err.message);
    res.status(500).json({ success: false, error: err.message });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`🏠 House Prediction API running on http://localhost:${PORT}`));
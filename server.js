const express = require("express");
const { execFile } = require("child_process");
const { analyzeSaju } = require("./engine/interpretationEngine");

const app = express();
app.use(express.json());

app.use((req, res, next) => {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  res.header("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  next();
});

function runBaziEngine(input) {
  return new Promise((resolve, reject) => {
    execFile(
  "python3",
  ["bazi_engine.py", input.year, input.month, input.day, input.hour, input.gender], 
      (error, stdout) => {
        if (error) reject(error);
        resolve(JSON.parse(stdout));
      }
    );
  });
}

app.post("/api/saju", async (req, res) => {
  try {
    const raw = await runBaziEngine(req.body);
    const analysis = analyzeSaju(raw, req.body.isPaid === true);
    res.json({ raw, analysis });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

const PORT = process.env.PORT || 10000;

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
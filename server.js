const express = require("express");
const { execFile } = require("child_process");
const { analyzeSaju } = require("./engine/interpretationEngine");

const app = express();
app.use(express.json());

function runBaziEngine(input) {
  return new Promise((resolve, reject) => {
    execFile(
      "python3",
      ["bazi_engine.py", input.year, input.month, input.day, input.hour],
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

app.listen(10000, () => {
  console.log("Server running on port 10000");
});
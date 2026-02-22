const express = require("express");
const cors = require("cors");
const { execFile } = require("child_process");
const path = require("path");

const app = express();

app.use(cors());
app.use(express.json());

function runBaziEngine(data) {
  return new Promise((resolve, reject) => {

    const args = [
      path.join(__dirname, "bazi_engine.py"),
      data.year,
      data.month,
      data.day,
      data.hour,
      data.gender || "male"
    ];

    execFile("python3", args, (error, stdout, stderr) => {

      if (stderr) {
        console.error("=== PYTHON STDERR ===");
        console.error(stderr);
      }

      if (error) {
        console.error("=== PYTHON ERROR ===");
        console.error(error);
        reject(new Error(stderr || error.message));
        return;
      }

      try {
        const parsed = JSON.parse(stdout);
        resolve(parsed);
      } catch (e) {
        console.error("=== JSON PARSE ERROR ===");
        console.error("STDOUT:", stdout);
        reject(e);
      }

    });
  });
}

app.post("/api/saju", async (req, res) => {
  try {

    console.log("=== REQUEST DATA ===");
    console.log(req.body);

    const result = await runBaziEngine(req.body);

    res.json(result);

  } catch (err) {

    console.error("=== ENGINE CRASH ===");
    console.error(err);

    res.status(500).json({
      error: err.toString()
    });

  }
});

app.get("/", (req, res) => {
  res.send("K-SAJU SERVER RUNNING");
});

const PORT = process.env.PORT || 10000;

app.listen(PORT, () => {
  console.log("Server running on port " + PORT);
});
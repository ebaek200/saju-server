const express = require("express");
const cors = require("cors");
const { execFile } = require("child_process");

const app = express();

// 🔥 CORS 반드시 여기 위치
app.use(cors());

// JSON 파싱
app.use(express.json());

// ----------------------------
// Python 실행 함수
// ----------------------------
function runBaziEngine(input) {
  return new Promise((resolve, reject) => {
    execFile(
      "python3",
      [
        "bazi_engine.py",
        input.year,
        input.month,
        input.day,
        input.hour,
        input.gender
      ],
      (error, stdout, stderr) => {
        if (error) {
          console.error(stderr);
          reject(error);
          return;
        }
        try {
          resolve(JSON.parse(stdout));
        } catch (e) {
          reject(e);
        }
      }
    );
  });
}

// ----------------------------
// API 엔드포인트
// ----------------------------
app.post("/api/saju", async (req, res) => {
  try {
    const result = await runBaziEngine(req.body);
    res.json({
      raw: result,
      analysis: {
        summary:
          "\n연주 " + result.year.stem + result.year.branch +
          "\n월주 " + result.month.stem + result.month.branch +
          "\n일주 " + result.day.stem + result.day.branch +
          "\n시주 " + result.hour.stem + result.hour.branch + "\n"
      }
    });
  } catch (err) {
    res.status(500).json({ error: "Engine Error" });
  }
});

// Render 포트
const PORT = process.env.PORT || 10000;

app.listen(PORT, () => {
  console.log("Server running on port " + PORT);
});
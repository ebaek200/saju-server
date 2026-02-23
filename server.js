const express = require("express");
const cors = require("cors");
const { Pool } = require("pg");

const app = express();

app.use(cors());
app.use(express.json());

/* ================================
   PostgreSQL 연결 설정
================================ */

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: {
    rejectUnauthorized: false
  }
});

/* ================================
   DB 연결 테스트 (서버 시작 시 1회 실행)
================================ */

pool.query("SELECT NOW()")
  .then(res => {
    console.log("✅ DB Connected Successfully");
    console.log("🕒 Server Time:", res.rows[0].now);
  })
  .catch(err => {
    console.error("❌ DB Connection Error");
    console.error(err);
  });

/* ================================
   기본 테스트 라우트
================================ */

app.get("/", (req, res) => {
  res.json({ message: "Server is running" });
});

/* ================================
   회원가입 예시 (테스트용)
================================ */

app.post("/register", async (req, res) => {
  try {
    const { email, password } = req.body;

    const result = await pool.query(
      "INSERT INTO users(email, password_hash) VALUES($1, $2) RETURNING id",
      [email, password]
    );

    res.json({ success: true, userId: result.rows[0].id });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Registration failed" });
  }
});

/* ================================
   서버 시작
================================ */

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
});
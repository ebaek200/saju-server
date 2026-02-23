const express = require("express");
const cors = require("cors");
const { Pool } = require("pg");

const app = express();
app.use(cors());
app.use(express.json());

/* ================================
   PostgreSQL 연결
================================ */

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false }
});

/* ================================
   DB 연결 테스트
================================ */

pool.query("SELECT NOW()")
  .then(res => {
    console.log("✅ DB Connected Successfully");
    console.log("🕒 Server Time:", res.rows[0].now);
  })
  .catch(err => {
    console.error("❌ DB Connection Error:", err);
  });

/* ================================
   회원번호 생성 (1111~9999)
================================ */

async function generateMemberNumber() {
  while (true) {
    const num = Math.floor(1111 + Math.random() * 8888).toString();

    const result = await pool.query(
      "SELECT 1 FROM users WHERE member_number = $1",
      [num]
    );

    if (result.rowCount === 0) {
      return num;
    }
  }
}

/* ================================
   1️⃣ 신규 사용자 등록
================================ */

app.post("/register", async (req, res) => {
  try {
    const {
      name,
      birth_year,
      birth_month,
      birth_day,
      calendar_type,
      gender
    } = req.body;

    if (!name || !birth_year || !birth_month || !birth_day || !calendar_type || !gender) {
      return res.status(400).json({ error: "Missing required fields" });
    }

    const member_number = await generateMemberNumber();

    await pool.query(
      `INSERT INTO users 
      (member_number, name, birth_year, birth_month, birth_day, calendar_type, gender)
      VALUES ($1,$2,$3,$4,$5,$6,$7)`,
      [member_number, name, birth_year, birth_month, birth_day, calendar_type, gender]
    );

    res.json({
      success: true,
      member_number
    });

  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Registration failed" });
  }
});

/* ================================
   2️⃣ 생시 최초 설정
================================ */

app.post("/set-hour", async (req, res) => {
  try {
    const { member_number, birth_hour } = req.body;

    if (!member_number || !birth_hour) {
      return res.status(400).json({ error: "Missing fields" });
    }

    await pool.query(
      `UPDATE users
       SET birth_hour = $1
       WHERE member_number = $2`,
      [birth_hour, member_number]
    );

    res.json({ success: true });

  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Set hour failed" });
  }
});

/* ================================
   3️⃣ 기존 사용자 복원
================================ */

app.post("/restore", async (req, res) => {
  try {
    const { member_number, birth_hour } = req.body;

    if (!member_number || !birth_hour) {
      return res.status(400).json({ error: "Missing fields" });
    }

    const result = await pool.query(
      `SELECT * FROM users
       WHERE member_number = $1
       AND birth_hour = $2`,
      [member_number, birth_hour]
    );

    if (result.rowCount === 0) {
      return res.json({ restored: false });
    }

    res.json({
      restored: true,
      user: result.rows[0]
    });

  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Restore failed" });
  }
});

/* ================================
   서버 시작
================================ */

const PORT = process.env.PORT || 10000;

app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
});
const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const cors = require('cors');
const { v4: uuidv4 } = require('uuid');

const app = express();
const PORT = 3001;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname)));

// SQLite database
const db = new sqlite3.Database('./data.db');

// Create table
db.serialize(() => {
  db.run(`
    CREATE TABLE IF NOT EXISTS test_results (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      timestamp TEXT NOT NULL,
      species TEXT NOT NULL,
      mbti_type TEXT NOT NULL,
      session_id TEXT NOT NULL,
      source TEXT DEFAULT 'web',
      created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
  `);
});

// API: Submit test result
app.post('/api/submit', (req, res) => {
  const { species, mbti_type } = req.body;
  const timestamp = new Date().toISOString();
  const session_id = uuidv4();
  
  const stmt = db.prepare(`
    INSERT INTO test_results (timestamp, species, mbti_type, session_id, source)
    VALUES (?, ?, ?, ?, 'web')
  `);
  
  stmt.run(timestamp, species, mbti_type, session_id, function(err) {
    if (err) {
      res.status(500).json({ error: err.message });
    } else {
      res.json({ success: true, session_id });
    }
  });
  stmt.finalize();
});

// API: Get statistics
app.get('/api/stats', (req, res) => {
  db.all(`
    SELECT mbti_type, species, COUNT(*) as count
    FROM test_results
    GROUP BY mbti_type, species
    ORDER BY count DESC
  `, (err, rows) => {
    if (err) {
      res.status(500).json({ error: err.message });
    } else {
      res.json(rows);
    }
  });
});

// API: Get total count
app.get('/api/count', (req, res) => {
  db.get('SELECT COUNT(*) as total FROM test_results', (err, row) => {
    if (err) {
      res.status(500).json({ error: err.message });
    } else {
      res.json({ total: row.total });
    }
  });
});

app.listen(PORT, () => {
  console.log(`MBTI Test API running on port ${PORT}`);
});
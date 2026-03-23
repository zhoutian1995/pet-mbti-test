const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const { v4: uuidv4 } = require('uuid');

const app = express();
const PORT = process.env.PORT || 3001;

// Security middleware - MODIFIED: 2026-03-23 - Phase 1 安全加固
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'", "cdn.tailwindcss.com", "code.iconify.design", "html2canvas.hertzen.com"],
      styleSrc: ["'self'", "'unsafe-inline'", "fonts.googleapis.com"],
      fontSrc: ["'self'", "fonts.gstatic.com"],
      imgSrc: ["'self'", "data:", "blob:"],
      connectSrc: ["'self'", "api.iconify.design", "api.unisvg.com", "api.simplesvg.com"],
      scriptSrcAttr: ["'self'", "'unsafe-inline'"]    // FIX: 2026-03-23 - Phase 5 支持 inline event handlers
    }
  }
}));

// Rate limiting - 100 requests per 15 minutes
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  message: { error: 'Too many requests, please try again later.' }
});
app.use('/api/', limiter);

// Request body size limit
app.use(express.json({ limit: '10kb' }));

// Middleware
// CORS 配置 - 限制允许的域名
const corsOptions = {
  origin: [
    'http://localhost:3001',
    'http://127.0.0.1:3001',
    'https://willeai.cn',
    'https://www.willeai.cn'
  ],
  methods: ['GET', 'POST'],
  credentials: true
};
app.use(cors(corsOptions));
app.use(express.json());
app.use(express.static(path.join(__dirname)));

// 有效的 MBTI 类型和物种
const VALID_MBTI_TYPES = ['ENFP', 'ENFJ', 'ENTP', 'ENTJ', 'ESFP', 'ESFJ', 'ESTP', 'ESTJ', 'INFP', 'INFJ', 'INTP', 'INTJ', 'ISFP', 'ISFJ', 'ISTP', 'ISTJ'];
const VALID_SPECIES = ['cat', 'dog'];

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

  // 输入验证
  if (!species || !mbti_type) {
    return res.status(400).json({ error: 'Missing required fields: species and mbti_type' });
  }

  if (!VALID_SPECIES.includes(species)) {
    return res.status(400).json({ error: `Invalid species. Must be one of: ${VALID_SPECIES.join(', ')}` });
  }

  if (!VALID_MBTI_TYPES.includes(mbti_type)) {
    return res.status(400).json({ error: `Invalid MBTI type. Must be one of: ${VALID_MBTI_TYPES.join(', ')}` });
  }

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

// Graceful shutdown - MODIFIED: 2026-03-23 - Phase 1 安全加固
process.on('SIGTERM', () => {
  console.log('SIGTERM signal received: closing HTTP server');
  db.close((err) => {
    if (err) {
      console.error('Error closing database:', err);
    } else {
      console.log('Database connection closed');
    }
    process.exit(0);
  });
});

process.on('SIGINT', () => {
  console.log('SIGINT signal received: closing HTTP server');
  db.close((err) => {
    if (err) {
      console.error('Error closing database:', err);
    } else {
      console.log('Database connection closed');
    }
    process.exit(0);
  });
});
const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const SCREENSHOT_DIR = path.join(process.env.HOME, '.openclaw/workspace-bob/screenshots');

async function takeScreenshot(url, options = {}) {
  const {
    width = 1920,
    height = 1080,
    fullPage = false,
    delay = 0,
    name = null
  } = options;

  // 确保目录存在
  if (!fs.existsSync(SCREENSHOT_DIR)) {
    fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });
  }

  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.setViewport({ width, height });

  console.log(`📸 正在截取: ${url}`);
  await page.goto(url, { waitUntil: 'networkidle2' });

  if (delay > 0) {
    console.log(`⏱️ 等待 ${delay}ms...`);
    await new Promise(r => setTimeout(r, delay));
  }

  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const filename = name 
    ? `${name}-${width}x${height}.png`
    : `screenshot-${timestamp}-${width}x${height}.png`;
  const filepath = path.join(SCREENSHOT_DIR, filename);

  await page.screenshot({ path: filepath, fullPage });
  console.log(`✅ 截图已保存: ${filepath}`);

  await browser.close();
  return filepath;
}

// CLI 入口
const args = process.argv.slice(2);
const url = args[0];

if (!url) {
  console.log('用法: node screenshot.js <URL> [--width 1920] [--height 1080] [--full] [--delay 0] [--name name]');
  process.exit(1);
}

const options = {};
for (let i = 1; i < args.length; i += 2) {
  const key = args[i]?.replace('--', '');
  const value = args[i + 1];
  if (key === 'width') options.width = parseInt(value);
  if (key === 'height') options.height = parseInt(value);
  if (key === 'full') { options.fullPage = true; i--; }
  if (key === 'delay') options.delay = parseInt(value);
  if (key === 'name') options.name = value;
}

takeScreenshot(url, options).catch(console.error);

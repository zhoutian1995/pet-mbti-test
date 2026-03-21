#!/usr/bin/env bash
# willeai.cn 自动截图脚本

set -e

OUTPUT_DIR="$HOME/Desktop/willeai-screenshots"
mkdir -p "$OUTPUT_DIR"

echo "📸 开始截图 willeai.cn 页面..."
echo ""

# 1. for-ai.html - 状态栏特写
echo "📷 for-ai.html (状态栏)"
npx playwright screenshot \
    --wait-for-selector "footer" \
    --viewport-size "1920,1080" \
    https://www.willeai.cn/for-ai.html \
    "$OUTPUT_DIR/for-ai.png"

# 2. index.html - 首页双卡片
echo "📷 index.html (首页双卡片)"
npx playwright screenshot \
    --wait-for-selector "main" \
    --viewport-size "1920,1080" \
    https://www.willeai.cn/ \
    "$OUTPUT_DIR/index.png"

# 3. for-humans.html
echo "📷 for-humans.html (GrowthCompass)"
npx playwright screenshot \
    --wait-for-selector "main" \
    --viewport-size "1920,1080" \
    https://www.willeai.cn/for-humans.html \
    "$OUTPUT_DIR/for-humans.png"

# 4. article-macmini.html - YAML + 按钮
echo "📷 article-macmini.html (YAML + Copy 按钮)"
npx playwright screenshot \
    --wait-for-selector "#view-machine" \
    --viewport-size "1920,1080" \
    https://www.willeai.cn/article-macmini.html \
    "$OUTPUT_DIR/article-macmini.png"

# 5. about.html - Connections 模块
echo "📷 about.html (Connections 模块)"
npx playwright screenshot \
    --wait-for-selector "main" \
    --viewport-size "1920,1080" \
    https://www.willeai.cn/about.html \
    "$OUTPUT_DIR/about.png"

echo ""
echo "═══════════════════════════════════════"
echo "✅ 完成！所有截图已保存到:"
echo "   $OUTPUT_DIR"
echo "═══════════════════════════════════════"
echo ""
ls -la "$OUTPUT_DIR"/*.png

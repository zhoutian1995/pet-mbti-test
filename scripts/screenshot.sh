#!/bin/bash
# 截图工具
# 用法: screenshot <URL> [选项]

SCREENSHOT_DIR="$HOME/.openclaw/workspace-bob/screenshots"
mkdir -p "$SCREENSHOT_DIR"

URL="$1"
shift

if [ -z "$URL" ]; then
  echo "📸 截图工具"
  echo ""
  echo "用法: screenshot <URL> [选项]"
  echo ""
  echo "选项:"
  echo "  --mobile     手机尺寸 (375x667)"
  echo "  --tablet     平板尺寸 (768x1024)"
  echo "  --desktop    桌面尺寸 (1920x1080) [默认]"
  echo "  --full       全页面截图"
  echo "  --delay N    延迟 N 毫秒"
  echo "  --name NAME  文件名前缀"
  echo ""
  echo "示例:"
  echo "  screenshot https://willeai.cn/"
  echo "  screenshot https://willeai.cn/ --mobile"
  echo "  screenshot https://willeai.cn/ --full --name homepage"
  exit 1
fi

# 解析选项
WIDTH=1920
HEIGHT=1080
FULL=""
DELAY=0
NAME=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --mobile)
      WIDTH=375
      HEIGHT=667
      shift
      ;;
    --tablet)
      WIDTH=768
      HEIGHT=1024
      shift
      ;;
    --desktop)
      WIDTH=1920
      HEIGHT=1080
      shift
      ;;
    --full)
      FULL="--full"
      shift
      ;;
    --delay)
      DELAY="$2"
      shift 2
      ;;
    --name)
      NAME="$2"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
done

echo "📸 截图参数:"
echo "  URL: $URL"
echo "  尺寸: ${WIDTH}x${HEIGHT}"
echo "  全页: ${FULL:-否}"
echo "  延迟: ${DELAY}ms"
echo ""

node ~/.openclaw/workspace-bob/screenshot.js "$URL" --width $WIDTH --height $HEIGHT $FULL --delay $DELAY ${NAME:+--name $NAME}

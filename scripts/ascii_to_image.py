#!/usr/bin/env python3
"""
ASCII 图转图片工具 - 使用 Playwright 截图
用法：python3 ascii_to_image.py <markdown 文件> <输出目录>
"""
import sys
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

def extract_ascii_blocks(markdown_path: str, output_dir: str):
    """提取 ASCII 图并转换为图片"""
    md_path = Path(markdown_path)
    md_content = md_path.read_text(encoding='utf-8')
    
    # 输出目录
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 查找代码块中的 ASCII 图
    ascii_pattern = r'```(\w*)\n(┌[─│└┘├┤┬┴┼]+.*?)```'
    matches = re.findall(ascii_pattern, md_content, re.DOTALL)
    
    print(f"找到 {len(matches)} 个 ASCII 图")
    
    images = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        for i, (lang, ascii_art) in enumerate(matches):
            # 创建 HTML
            html = f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:20px;background:#1e1e1e;padding:20px;">
<pre style="font-family:'SF Mono',monospace;font-size:13px;color:#d4d4d4;margin:0;">{ascii_art}</pre>
</body>
</html>"""
            
            # 保存临时 HTML
            temp_html = output_path / f"ascii_{i}.html"
            temp_html.write_text(html, encoding='utf-8')
            
            # 截图
            page.goto(f"file://{temp_html.absolute()}")
            screenshot_path = output_path / f"ascii_{i}.png"
            page.screenshot(path=str(screenshot_path))
            
            images.append(str(screenshot_path))
            print(f"  ✅ 已保存：{screenshot_path}")
        
        browser.close()
    
    print(f"\n✅ 共转换 {len(images)} 个 ASCII 图为图片")
    return images

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法：python3 ascii_to_image.py <markdown 文件> <输出目录>")
        sys.exit(1)
    
    extract_ascii_blocks(sys.argv[1], sys.argv[2])

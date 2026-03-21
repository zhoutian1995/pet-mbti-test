#!/usr/bin/env python3
"""
微信公众号文章自动截图功能
生成文章预览截图
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

def screenshot_article(html_content, output_path, title="文章预览"):
    """
    生成文章截图
    
    Args:
        html_content: HTML 内容
        output_path: 截图输出路径
        title: 页面标题
    """
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 414, 'height': 896},  # iPhone 尺寸
            device_scale_factor=2  # Retina 屏幕
        )
        page = context.new_page()
        
        # 设置内容
        page.set_content(html_content, wait_until='networkidle')
        
        # 等待渲染
        page.wait_for_timeout(1000)
        
        # 截图 (full_page 会自动处理完整高度)
        page.screenshot(path=output_path, full_page=True)
        
        browser.close()
        
        print(f"✅ 截图已保存：{output_path}")
        return output_path

def generate_preview_html(title, content, author=""):
    """生成预览 HTML"""
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    margin: 0;
    padding: 20px;
    background: #f5f5f5;
}}
.article {{
    max-width: 600px;
    margin: 0 auto;
    background: #fff;
    padding: 24px 20px;
    border-radius: 12px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}}
h1 {{
    text-align: center;
    font-size: 22px;
    margin-bottom: 24px;
}}
.content {{
    line-height: 1.8;
    color: #333;
}}
.footer {{
    text-align: center;
    margin-top: 32px;
    padding-top: 20px;
    border-top: 1px solid #e5e7eb;
    color: #999;
    font-size: 14px;
}}
</style>
</head>
<body>
<div class="article">
    <h1>{title}</h1>
    <div class="content">
        {content}
    </div>
    <div class="footer">
        <p>作者：{author}</p>
        <p>— END —</p>
    </div>
</div>
</body>
</html>'''

if __name__ == '__main__':
    # 测试截图功能
    test_html = generate_preview_html(
        title="测试文章截图",
        content="<p>这是测试内容，用于验证自动截图功能。</p><p>第二段内容。</p>",
        author="Bob"
    )
    
    output_path = Path(__file__).parent / "test-screenshot.png"
    screenshot_article(test_html, str(output_path))
    
    print(f"\n✅ 自动截图功能测试完成")

#!/usr/bin/env python3
"""
快速预览脚本 - 生成 HTML 并在浏览器中打开
用法：python3 preview.py <markdown 文件> [输出文件名]
"""
import sys
from pathlib import Path
import webbrowser
import re

# 添加路径
SKILLS_PATH = Path("/Users/wille/.openclaw/workspace/02-项目/公众号推送 skills")
sys.path.insert(0, str(SKILLS_PATH / 'src'))

def preview_markdown(markdown_path: str, output_name: str = None):
    """预览 Markdown 文件"""
    from renderer import MarkdownRenderer
    
    md_path = Path(markdown_path)
    if not md_path.exists():
        print(f"❌ 文件不存在：{markdown_path}")
        return
    
    # 输出路径
    if output_name:
        output_path = Path(output_name)
    else:
        output_path = Path("/Users/wille/.openclaw/workspace-bob") / f"{md_path.stem}-预览.html"
    
    # 图片基础路径（与 Markdown 同目录）
    image_base = md_path.parent
    print(f"📝 读取 Markdown: {md_path}")
    print(f"📂 图片目录：{image_base}")
    md_content = md_path.read_text(encoding='utf-8')
    
    # 处理 Obsidian 图片语法
    def replace_obsidian_image(match):
        image_name = match.group(1).strip()
        print(f"  🔍 查找图片：{image_name}")
        # 直接使用该文件名（已包含扩展名）
        image_path = image_base / image_name
        if image_path.exists():
            print(f"  ✅ 找到：{image_path}")
            return f'<img src="{image_path}" alt="{image_name}" style="max-width:100%;height:auto;display:block;margin:16px auto;" />'
        else:
            print(f"  ❌ 未找到：{image_path}")
            # 尝试不带扩展名
            base_name = image_name.rsplit('.', 1)[0]
            for ext in ['.png', '.jpg', '.jpeg', '.gif']:
                test_path = image_base / f'{base_name}{ext}'
                if test_path.exists():
                    print(f"  ✅ 找到（补全扩展名）：{test_path}")
                    return f'<img src="{test_path}" alt="{image_name}" style="max-width:100%;height:auto;display:block;margin:16px auto;" />'
            return match.group(0)
    
    md_content = re.sub(r'!\[\[([^\]]+)\]\]', replace_obsidian_image, md_content)
    
    # 渲染 HTML
    print("🎨 渲染 HTML...")
    renderer = MarkdownRenderer(theme_path=str(SKILLS_PATH / 'themes/macWindow.css'))
    html_content = renderer.render(md_content)
    
    # 反转义图片标签
    html_content = html_content.replace('&lt;img src=', '<img src=').replace('/&gt;', '/>').replace('&lt;/img&gt;', '</img>')
    
    # 添加完整 HTML 结构和专用样式
    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>预览 - {md_path.stem}</title>
    <style>
        body {{ max-width: 800px; margin: 0 auto; padding: 20px; font-family: -apple-system, sans-serif; }}
        .tech-box {{ background: #f6f8fa; border-left: 4px solid #16a34a; padding: 16px; margin: 16px 0; border-radius: 0 8px 8px 0; }}
        .tech-title {{ font-weight: bold; color: #16a34a; margin-bottom: 8px; font-size: 16px; }}
        .symptom {{ background: #fef2f2; border-left-color: #dc2626; }}
        .symptom .tech-title {{ color: #dc2626; }}
        .diagnosis {{ background: #fffbeb; border-left-color: #d97706; }}
        .diagnosis .tech-title {{ color: #d97706; }}
        .solution {{ background: #f0fdf4; border-left-color: #16a34a; }}
        .solution .tech-title {{ color: #16a34a; }}
        img {{ max-width: 100%; height: auto; display: block; margin: 16px auto; border-radius: 8px; }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""
    
    # 保存
    output_path.write_text(full_html, encoding='utf-8')
    print(f"✅ HTML 已保存：{output_path}")
    
    # 在浏览器中打开
    print("🌐 在浏览器中打开...")
    webbrowser.open(f"file://{output_path.absolute()}")
    
    # 显示统计
    print(f"\n📊 统计信息:")
    print(f"   Markdown: {len(md_content):,} 字符")
    print(f"   HTML: {len(full_html):,} 字符")
    print(f"   图片：{len(re.findall(r'<img[^>]*>', full_html))} 张")
    
    return str(output_path)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法：python3 preview.py <markdown 文件> [输出文件名]")
        sys.exit(1)
    
    markdown_path = sys.argv[1]
    output_name = sys.argv[2] if len(sys.argv) > 2 else None
    
    preview_markdown(markdown_path, output_name)

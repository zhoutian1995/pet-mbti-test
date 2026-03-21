#!/usr/bin/env python3
"""
图表渲染模块 - 使用 Kroki + Mermaid
替换 ASCII 方框图表为专业图表
"""
import base64
import requests
import zlib
from pathlib import Path
from typing import Optional, Literal


def _plantuml_encode(text: str) -> str:
    """PlantUML 专用编码 (deflate + base64)"""
    # 压缩
    compressed = zlib.compress(text.encode('utf-8'))[2:-4]  # 去掉 zlib 头尾
    # Base64 URL-safe 编码
    encoded = base64.b64encode(compressed).decode('utf-8')
    # 转换为 PlantUML 字符集
    trans = str.maketrans(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",
        "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
    )
    return encoded.translate(trans)


class DiagramRenderer:
    """图表渲染器 - 使用 Kroki API"""
    
    # Kroki API 端点
    KROKI_BASE = "https://kroki.io"
    
    # 支持的图表类型
    DIAGRAM_TYPES = Literal['mermaid', 'plantuml', 'graphviz', 'ditaa', 'blockdiag', 'seqdiag']
    
    def __init__(self, default_type: str = 'plantuml'):
        """
        初始化渲染器
        
        Args:
            default_type: 默认图表类型 (plantuml/mermaid/graphviz)
                          推荐使用 plantuml - 更稳定
        """
        self.default_type = default_type
    
    def render(self, code: str, diagram_type: Optional[str] = None, 
               output_format: str = 'png') -> bytes:
        """
        渲染图表
        
        Args:
            code: 图表代码 (Mermaid/PlantUML 等)
            diagram_type: 图表类型 (mermaid/plantuml/graphviz 等)
            output_format: 输出格式 (png/svg)
        
        Returns:
            图片二进制数据
        """
        diagram_type = diagram_type or self.default_type
        
        # PlantUML 需要特殊编码
        if diagram_type == 'plantuml':
            encoded = _plantuml_encode(code)
        else:
            # 其他类型用普通 Base64
            code_bytes = code.encode('utf-8')
            encoded = base64.urlsafe_b64encode(code_bytes).decode('utf-8')
        
        # 构建 Kroki URL
        url = f"{self.KROKI_BASE}/{diagram_type}/{output_format}/{encoded}"
        
        # 下载图片
        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            return resp.content
        except requests.RequestException as e:
            raise Exception(f"图表渲染失败：{e}")
    
    def render_to_file(self, code: str, output_path: str, 
                       diagram_type: Optional[str] = None) -> str:
        """
        渲染图表并保存到文件
        
        Args:
            code: 图表代码
            output_path: 输出文件路径
            diagram_type: 图表类型
        
        Returns:
            输出文件路径
        """
        png_data = self.render(code, diagram_type)
        
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(png_data)
        
        return str(path)
    
    def upload_to_wechat(self, code: str, wechat_api, 
                         diagram_type: Optional[str] = None) -> str:
        """
        渲染图表并上传到微信
        
        Args:
            code: 图表代码
            wechat_api: 微信 API 实例
            diagram_type: 图表类型
        
        Returns:
            微信图片 URL
        """
        png_data = self.render(code, diagram_type)
        
        # 上传到微信 (临时图片接口)
        url = "https://api.weixin.qq.com/cgi-bin/media/uploadimg"
        params = {"access_token": wechat_api.get_access_token()}
        files = {'media': ('diagram.png', png_data, 'image/png')}
        
        resp = requests.post(url, params=params, files=files, timeout=30)
        data = resp.json()
        
        if 'url' not in data:
            raise Exception(f"微信图片上传失败：{data}")
        
        return data['url']


# 预定义图表模板
TEMPLATES = {
    'flowchart': """
graph TD
    A[{title}] --> B[步骤 1]
    B --> C[步骤 2]
    C --> D[步骤 3]
    D --> E[结束]
""",
    'sequence': """
sequenceDiagram
    participant A as {actor1}
    participant B as {actor2}
    A->>B: 请求
    B-->>A: 响应
""",
    'architecture': """
graph LR
    subgraph 前端
        A[用户界面]
    end
    subgraph 后端
        B[API 服务]
        C[数据库]
    end
    A --> B
    B --> C
""",
    'mindmap': """
mindmap
  root[{title}]
    分支 1
      子分支 1
      子分支 2
    分支 2
      子分支 3
"""
}


def render_template(template_name: str, **kwargs) -> str:
    """渲染图表模板"""
    template = TEMPLATES.get(template_name)
    if not template:
        raise ValueError(f"未知模板：{template_name}")
    return template.format(**kwargs)


# 便捷函数
def render_mermaid(code: str) -> bytes:
    """快速渲染 Mermaid 图表"""
    return DiagramRenderer().render(code, 'mermaid')


def render_plantuml(code: str) -> bytes:
    """快速渲染 PlantUML 图表"""
    return DiagramRenderer().render(code, 'plantuml')


# 测试
if __name__ == '__main__':
    renderer = DiagramRenderer()
    
    # 测试流程图 (PlantUML)
    flowchart_code = """
@startuml
:Start;
if (Decision?) then
  :Process;
else
  :End;
endif
@enduml
"""
    
    output_path = renderer.render_to_file(flowchart_code, "/Users/wille/.openclaw/workspace-bob/test-flowchart.png")
    print(f"✅ 流程图已保存：{output_path}")
    
    # 测试时序图 (PlantUML)
    sequence_code = """
@startuml
participant User
participant API
participant Database

User -> API: Request
API -> Database: Query
Database --> API: Return
API --> User: Response
@enduml
"""
    
    output_path = renderer.render_to_file(sequence_code, "/Users/wille/.openclaw/workspace-bob/test-sequence.png")
    print(f"✅ 时序图已保存：{output_path}")
    
    # 测试架构图 (PlantUML 组件图)
    arch_code = """
@startuml
package "Client" {
  [WeChat] as A
}
package "Server" {
  [API Gateway] as B
  [Business Logic] as C
  database "Database" as D
}
A --> B
B --> C
C --> D
@enduml
"""
    
    output_path = renderer.render_to_file(arch_code, "/Users/wille/.openclaw/workspace-bob/test-architecture.png")
    print(f"✅ 架构图已保存：{output_path}")
    
    print("\n✅ 所有测试完成")

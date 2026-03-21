# Workspace 整理任务计划

**工作区**: `/Users/wille/.openclaw/workspace-bob/`
**初始大小**: 324M
**执行时间**: 2026-03-21

## 📋 任务清单

### Phase 1: 分析现状 ✅
- [x] 检查目录结构
- [x] 统计磁盘使用
- [x] 识别需要整理的内容

### Phase 2: 执行清理 ⏳
- [ ] 运行 cleanup.sh 脚本
- [ ] 清理临时文件
- [ ] 清理重复文件

### Phase 3: 批量整理 ⏳
- [ ] 整理散落的 Python 脚本
- [ ] 整理测试文件
- [ ] 整理截图和图片
- [ ] 整理 HTML 测试文件

### Phase 4: Git 备份 ⏳
- [ ] 检查 git 状态
- [ ] 配置 .gitignore
- [ ] 执行完整备份

### Phase 5: 汇报结果 ⏳
- [ ] 统计清理数量
- [ ] 记录释放空间
- [ ] 总结整理结果

## 📁 发现的问题

1. **散落的 Python 脚本**: `ascii_to_image.py`, `auto_screenshot.py`, `diagram_renderer.py`, `preview.py` 等
2. **测试文件**: 多个 HTML 测试文件、PNG 截图
3. **重复/备份文件**: `MEMORY.md.bak`, `SOUL.md.bak`
4. **临时文件**: `Codex`, `forum_task.txt`, `cover_media_id.txt`
5. **大型图片**: `mac-window-codeblock-screenshot.png` (3.6M)

## 🎯 目标结构

```
workspace-bob/
├── scripts/          # 所有脚本移入
├── tests/            # 测试文件移入
├── screenshots/      # 截图移入（已有）
├── archive/          # 旧文件归档
└── [核心文件保留]
```
# TOOLS.md - 关键路径和工具

## 知识库 [P0 必知]

**重要**：工作区**就是**知识库，不再有 `obsidian/` 子目录。

**绝对路径**: `/Users/wille/.openclaw/workspace/`
**相对路径**: 直接用文件名（如 `01-公司/团队总览.md`）

目录结构：
```
01-公司/          # 团队组织、成员档案、系统架构
02-项目/          # OpenClaw、OpenCode、PicoClaw
03-运营/          # 个人IP策略
04-基建/          # VPN、网络配置
05-日报/          # 团队/个人日报
06-复盘/          # 经验教训、调研
07-资源/          # API密钥
08-私人/          # 个人备忘
99-系统/          # Agent系统说明
```

读取示例：
- 读团队总览：`read 01-公司/团队总览.md`
- 读OpenClaw文档：`read 02-项目/OpenClaw/README.md`
- 写新笔记：`write 02-项目/xxx.md`

## API Keys [P0 必知]

**BRAVE_API_KEY**: 已注入环境变量，web_search 工具直接可用，无需手动传 key

## 发消息给周老板

```
message send target=5248895145 channel=telegram message="内容"
```

## 团队通信

| 目标 | sessionKey 格式 |
|------|----------------|
| Mike | agent:mike:main |
| Bob  | agent:bob:main  |
| May  | agent:may:main  |

用 sessions_send 派任务，用 sessions_spawn 派异步任务。

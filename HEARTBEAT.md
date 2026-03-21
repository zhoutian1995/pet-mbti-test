# HEARTBEAT.md - Bob 心跳任务

## 每日记忆提炼（每次心跳执行）

检查 `memory/` 目录下今天的日志文件 `memory/YYYY-MM-DD.md`，如果存在且 `memory/RECENT.md` 中还没有今天的条目，则：

1. 读取今天的日志文件
2. 提炼 3-5 个关键要点（决策、状态变更、教训）
3. 追加到 `memory/RECENT.md` 的顶部，格式：
   ```
   ## YYYY-MM-DD
   - 要点1
   - 要点2
   ```
4. 检查 RECENT.md 中超过 7 天的条目，在日期前标记 `[过期]`

如果今天没有日志文件，或已经提炼过，跳过。

# prompts.chat 项目研究报告

> 研究日期：2026-03-14
> 研究人：Bob
> 项目地址：https://github.com/f/prompts.chat
> Stars：143k+

---

## 一、项目概述

### 1.1 基本信息
- **项目名**：prompts.chat（原名 Awesome ChatGPT Prompts）
- **定位**：世界上最大的开源 Prompt 库
- **协议**：CC0 1.0（公共领域，可自由使用）
- **支持模型**：ChatGPT、Claude、Gemini、Llama、Mistral 等

### 1.2 权威认可
- Forbes 报道
- Harvard、Columbia 引用
- 40+ 学术论文引用
- OpenAI 联合创始人、Hugging Face CEO、GitHub CEO 推荐

---

## 二、Prompt 模式分析

### 2.1 核心模式总结

通过分析项目中的 100+ Prompt，提炼出以下核心模式：

#### 模式一：角色扮演（Role-Play）
```md
I want you to act as a [角色].
[具体要求和行为约束]
My first [request/input] is "[初始输入]"
```

**示例**：
- Linux Terminal - 扮演终端
- Job Interviewer - 扮演面试官
- Travel Guide - 扮演导游

#### 模式二：约束输出（Output Constraint）
```md
I want you to only reply with [输出格式].
Do not write explanations.
[具体输出规则]
```

**关键约束词**：
- `only reply with` - 限制输出内容
- `do not write explanations` - 禁止解释
- `inside one unique code block` - 格式化输出

#### 模式三：变量替换（Variable Template）
```md
I want you to act as a [角色] for ${变量名:默认值}.
My first [request] is "${变量名}"
```

**示例**：
- `${Position:Software Developer}` - 职位变量
- `${Mother Language:Turkish}` - 母语变量
- `{character} from {series}` - 角色变量

#### 模式四：渐进交互（Progressive Interaction）
```md
Ask me the questions one by one like an interviewer does.
Wait for my answers.
Do not write all the conversation at once.
```

---

## 三、精选 Prompt 分类

### 3.1 开发相关（团队重点）

| Prompt | 用途 | 适用场景 |
|--------|------|----------|
| Linux Terminal | 执行命令模拟 | 测试、学习 Linux |
| JavaScript Console | JS 代码调试 | 前端开发 |
| Ethereum Developer | 智能合约开发 | 区块链项目 |
| UX/UI Developer | 界面设计评审 | 产品设计 |
| AI Writing Tutor | 代码文档改进 | 技术写作 |

### 3.2 内容创作（May 重点）

| Prompt | 用途 | 适用场景 |
|--------|------|----------|
| Storyteller | 故事创作 | 内容营销 |
| Screenwriter | 剧本创作 | 视频脚本 |
| Poet | 诗歌创作 | 创意内容 |
| Rapper | 歌词创作 | 流行文化 |
| Movie Critic | 影评撰写 | 内容评测 |

### 3.3 学习提升

| Prompt | 用途 | 适用场景 |
|--------|------|----------|
| English Translator | 英语翻译改进 | 语言学习 |
| Spoken English Teacher | 口语练习 | 语言提升 |
| Math Teacher | 数学讲解 | 概念理解 |
| Philosophy Teacher | 哲学讲解 | 思维训练 |

### 3.4 工作效率

| Prompt | 用途 | 适用场景 |
|--------|------|----------|
| Plagiarism Checker | 查重检测 | 内容审核 |
| Advertiser | 广告策划 | 营销活动 |
| Motivational Coach | 激励指导 | 目标达成 |
| Debate Coach | 辩论准备 | 方案论证 |

---

## 四、团队应用建议

### 4.1 集成方式

#### 方式一：MCP Server 集成（推荐）
```json
// ~/.claude/settings.json
{
  "mcpServers": {
    "prompts.chat": {
      "url": "https://prompts.chat/api/mcp"
    }
  }
}
```

#### 方式二：Claude Code 插件
```bash
/plugin install prompts.chat@prompts.chat
```

#### 方式三：本地克隆
```bash
git clone https://github.com/f/prompts.chat.git
# 可自托管，自定义主题和品牌
```

### 4.2 自定义 Prompt 开发

基于项目模式，为团队开发专属 Prompt：

#### Bob 专用：代码审查专家
```md
I want you to act as a senior code reviewer. 
I will provide you with code snippets and you will analyze them for:
- Security vulnerabilities
- Performance issues  
- Code style and best practices
- Potential bugs

Reply in the following format:
## Review Summary
[Overall assessment]

## Issues Found
1. [Issue type] - [Description] - [Severity: High/Medium/Low]

## Suggestions
[Suggested improvements]

My first code to review is:
```

#### May 专用：内容策划专家
```md
I want you to act as a content strategist for embedded systems and AI programming.
I will provide you with topic ideas and you will:
1. Suggest target audience
2. Outline key points
3. Recommend content format (article/video/tutorial)
4. Provide title options optimized for SEO

Reply in Chinese. My first topic is:
```

### 4.3 CCG 配置结合

将 Prompt 模板整合到 CCG 工作流：

```bash
# 创建自定义 CCG 命令
~/.claude/commands/ccg/prompt-expert.md
```

---

## 五、Prompt Engineering 最佳实践

### 5.1 黄金法则

1. **明确角色** - "I want you to act as..."
2. **设定边界** - "only reply with...", "do not write explanations"
3. **提供示例** - 给出期望的输出格式
4. **渐进交互** - 一步步引导，而非一次性输出
5. **变量模板** - 使用 ${变量} 提高复用性

### 5.2 常见错误

| 错误 | 正确做法 |
|------|----------|
| 模糊指令 | 具体明确的行为描述 |
| 缺乏约束 | 添加输出格式限制 |
| 无上下文 | 提供背景和目标 |
| 单次交互 | 设计多轮对话流程 |

### 5.3 提升技巧

1. **Chain of Thought** - 让 AI 展示推理过程
2. **Few-Shot Learning** - 提供多个示例
3. **Self-Reflection** - 让 AI 自我检查输出
4. **Role Switching** - 同一对话中切换角色视角

---

## 六、行动计划

### 短期（本周）
- [ ] 将 prompts.chat MCP Server 集成到团队配置
- [ ] 为 Bob 和 May 各开发 3 个专属 Prompt 模板
- [ ] 测试 Linux Terminal 和 JavaScript Console Prompt

### 中期（本月）
- [ ] 建立团队 Prompt 库（基于 prompts.chat 模式）
- [ ] 编写团队 Prompt Engineering 指南
- [ ] 与 CCG 工作流深度整合

### 长期
- [ ] 自托管 prompts.chat，添加团队私有 Prompt
- [ ] 定期更新和优化 Prompt 库
- [ ] 培训团队成员 Prompt Engineering 技能

---

## 七、资源链接

- 官网：https://prompts.chat
- GitHub：https://github.com/f/prompts.chat
- Hugging Face 数据集：https://huggingface.co/datasets/fka/prompts.chat
- 免费教程：https://fka.gumroad.com/l/art-of-chatgpt-prompting

---

*报告完成于 2026-03-14*
*Bob - 程序员兼资料员*
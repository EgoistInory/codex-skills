# Codex Skills

本项目是一个专门用于存放和分发 **Codex Skills（智能体技能）** 的公开 GitHub 仓库。Codex Skills 是一种基于开放标准的、专为 AI 编码辅助智能体（如 OpenAI Codex 等）设计的按需程序化知识与工作流包。

通过使用这些技能，AI 智能体能够遵循严格、标准化的工程流程来处理复杂任务（例如前端验收、重构、Bug 排查等），确保高质量的代码交付。

---

## 📂 项目结构

本项目推荐将所有技能统一收纳在 `skills/` 目录下，便于集中管理与批量在线安装：

```text
codex-skills/
├── skills/
│   ├── frontend-acceptance-workflow/    # 前端验收工作流技能
│   │   ├── SKILL.md                     # 技能核心指令与工作流规范
│   │   ├── agents/
│   │   │   └── openai.yaml              # 技能在 Codex UI 中的元数据配置
│   │   └── references/
│   │       └── acceptance-checklist.md  # 前端验收检查清单
│   └── another-skill/                   # 其他技能目录...
└── README.md                            # 本指南文件
```

---

## 📦 当前技能

| Skill | 用途 |
| --- | --- |
| `agent-handoff-workflow` | Agent 交接、上下文到顶、换会话/换模型时的项目上下文包创建与维护。 |
| `fanqie-novel-workflow` | 番茄小说通用创作工作流，编排续写、审校、状态交接、导出与小说专项 skill 配合。 |
| `frontend-acceptance-workflow` | 前端实现、浏览器验收、回归排查与交付闭环。 |
| `frontend-netlify-release` | 前端项目 Netlify 发布前检查、干净发布目录、MCP/CLI 发布与失败止损流程。 |
| `hatch-pet` | Codex pet / spritesheet 生成、校验与打包流程。 |
| `kindle-home-board-workflow` | Kindle / 电子墨水屏 / 老浏览器家庭信息板的本地同步、低频刷新、Admin 表单化与验收流程。 |
| `macos-app-external-restart` | macOS GUI 应用外置重启、launchd 托管执行、残留进程与临时文件清理验证。 |
| `python-ai-project-dependencies` | AI / vibe-coding Python 项目的依赖选择、分组、安装与验证方法论。 |
| `realistic-human-image-qa` | 写实真人生图、多参考图提示词整合、完整可复制提示词与物理现实校验。 |
| `windows-codex-msix-portable-fix` | Windows 受限环境下 Codex MSIX / portable 运行与 runtime 修复。 |
| `windows-ide-open-fix` | Windows 上 Codex 打开 IDE / 文件失败的诊断与修复。 |

---

## 💡 什么是 Skill（智能体技能）？

在 AI 智能体生态中，一个 **Skill** 是一个独立的目录，其核心是 `SKILL.md` 文件。

### 1. `SKILL.md` 的组成
*   **YAML Frontmatter（前置元数据）**：定义技能的名称 (`name`) 和描述 (`description`)。描述非常关键，AI 智能体会根据它来判断何时触发该技能。
*   **Markdown Body（说明主体）**：定义具体的操作规范、设计原则、标准工作流（Workflow）、回滚/排查模式（Triage Pattern）以及验收清单。

### 2. 渐进式加载（Progressive Disclosure）
为了节省上下文窗口（Context Window），智能体在启动时**仅加载所有技能的名称和描述**。只有当智能体判断当前任务与某个技能高度相关，或者用户显式调用时，才会将完整的 `SKILL.md` 内容加载到上下文里，实现高效而精准的引导。

---

## 🛠️ 如何安装 Skill

本项目支持公开共享，最简单稳妥的安装方式是通过 `skill-installer` 直接从本 GitHub 仓库进行在线安装。

### 选项 A：在线自动安装（推荐）

如果你的 Codex 或其他 AI 助理支持 `$skill-installer` 工具，可以直接在对话框中粘贴以下指令，让它从本仓库自动安装对应的技能。

**示例：安装 frontend-acceptance-workflow 技能**
你可以使用直接链接方式：
> Use $skill-installer to install from https://github.com/EgoistInory/codex-skills/tree/main/skills/frontend-acceptance-workflow

或者使用精确指定仓库与路径的方式：
> Use $skill-installer to install frontend-acceptance-workflow from repo EgoistInory/codex-skills path skills/frontend-acceptance-workflow

*(如果你想安装本仓库中的其他技能，只需将指令中的 `frontend-acceptance-workflow` 替换为目标技能的目录名即可。)*

⚠️ **重要提示**：安装完成后，**请务必重启 Codex**（或你正在使用的 AI 客户端），以确保新安装的 skill 被正确加载并生效。

### 选项 B：手动离线安装

如果你希望手动配置，需要将对应的技能目录（例如 `skills/frontend-acceptance-workflow`）放置到 AI 智能体指定的本地路径下：

*   **项目局部（推荐）**：复制到目标项目根目录的 `.codex/skills/` 中。
*   **全局生效**：复制到用户全局配置目录下（Windows: `C:\Users\<用户名>\.codex\skills\`，macOS/Linux: `~/.codex/skills/`）。

手动放置文件后，同样需要**重启 Codex** 让其生效。

---

## 🚀 如何使用 Skill

一旦安装完成并重启生效，AI 智能体将支持两种触发方式：

1. **隐式自动触发（Implicit Invocation）**
   当你在对话中提到的任务与某个技能的 `description` 高度匹配时（例如你提到了与前端验收、部署等相关的任务），智能体会自动检索并加载对应的技能，并在后台默默遵循该工作流执行。
   
2. **显式主动调用（Explicit Invocation）**
   你可以在提示词中直接引用特定技能的名称来强制启用它，例如：
   > “使用 $frontend-acceptance-workflow 来重构登录页面，并完成浏览器回归测试。”

---

## ✍️ 开发与共享新 Skill 注意事项

如果你想为本公开仓库增加新的技能，请遵循以下安全与格式规范：

1. **新建技能目录**：在 `skills/` 目录下新建一个以英文连字符命名的文件夹（如 `database-migration-workflow`）。
2. **清理敏感信息**：**绝对不要**共享包含以下内容的系统技能或项目特定技能：
   *   内部/私有路径
   *   公司专有信息
   *   Token、密码或密钥
   *   极度耦合的项目特定文件名
3. **创建 `SKILL.md`**：
   *   顶部必须包含 YAML frontmatter 区域。
   *   `name` 需与文件夹名称一致。
   *   `description` 应该精炼且具有高区分度。
4. **提交并推送**：将整理好的技能目录推送到本公开仓库的 `main` 分支。

# Codex Skills

本项目是一个专门用于存放和分发 **Codex Skills（智能体技能）** 的仓库。Codex Skills 是一种基于开放标准的、专为 AI 编码辅助智能体（如 OpenAI Codex 等）设计的按需程序化知识与工作流包。

通过使用这些技能，AI 智能体能够遵循严格、标准化的工程流程来处理复杂任务（例如前端验收、重构、Bug 排查等），确保高质量的代码交付。

---

## 📂 项目结构

```text
codex-skills/
├── frontend-acceptance-workflow/    # 前端验收工作流技能
│   ├── SKILL.md                     # 技能核心指令与工作流规范
│   ├── agents/
│   │   └── openai.yaml              # 技能在 Codex UI 中的元数据配置
│   └── references/
│       └── acceptance-checklist.md  # 前端验收检查清单
└── README.md                        # 本指南文件
```

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

要让你的 AI 编码助理识别并使用这些 Skill，需要将对应的技能目录放置到指定的路径下。

### 选项 A：项目局部安装（推荐）
如果你只想在**特定项目**中启用某个技能，请将技能目录复制到该项目的根目录下的 `.codex/skills/` 中。

1. 在目标项目的根目录下创建文件夹：
   ```bash
   mkdir -p .codex/skills/
   ```
2. 将 `frontend-acceptance-workflow` 文件夹整体复制到该目录下：
   ```text
   <你的项目根目录>/
   └── .codex/
       └── skills/
           └── frontend-acceptance-workflow/
               ├── SKILL.md
               ├── agents/
               └── references/
   ```

### 选项 B：全局安装
如果你希望在**所有项目**中都能使用这些技能，请将其安装到用户的全局配置目录下。

*   **Windows**: `C:\Users\<你的用户名>\.codex\skills\`
*   **macOS / Linux**: `~/.codex/skills/`

1. 创建全局技能目录：
   ```bash
   mkdir -p ~/.codex/skills/
   ```
2. 将 `frontend-acceptance-workflow` 目录复制至该目录下：
   ```text
   ~/.codex/skills/frontend-acceptance-workflow/
   ```

---

## 🚀 如何使用 Skill

一旦安装完成，AI 智能体将支持两种触发方式：

1. **隐式自动触发（Implicit Invocation）**
   当你在对话中提到与前端美化、UI 调整、打包部署、浏览器测试或回归排查相关的任务时，智能体会根据 `SKILL.md` 的 `description` 自动检索并加载 `frontend-acceptance-workflow`，并在后台默默遵循该工作流执行。
   
2. **显式主动调用（Explicit Invocation）**
   你可以在提示词中直接引用技能名称来强制启用它，例如：
   > “使用 $frontend-acceptance-workflow 来重构登录页面，并完成浏览器回归测试。”
   > “请按照 frontend-acceptance-workflow 规范对刚才的代码修改进行审查和验收。”

---

## ✍️ 开发与自定义新 Skill

如果你想为项目增加新的技能，请遵循以下规范：

1. **新建技能目录**：在仓库根目录下新建一个以英文连字符命名的文件夹（如 `database-migration-workflow`）。
2. **创建 `SKILL.md`**：
   *   顶部必须包含 YAML frontmatter 区域。
   *   `name` 需与文件夹名称一致。
   *   `description` 应该精炼且具有高区分度，概括技能的使用场景。
   *   编写结构化、目标导向的 `## Workflow` 和 `## Principles`。
3. **（可选）配置 `agents/openai.yaml`**：
   *   如果需要在可视化界面（如 Codex UI）中展示，可以配置 `display_name`、`short_description` 以及 `default_prompt`。
4. **提交代码**：将技能提交并推送到本仓库。其他协作者只需拉取最新代码并按上述安装步骤更新即可。

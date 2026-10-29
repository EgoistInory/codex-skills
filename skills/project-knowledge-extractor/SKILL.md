---
name: project-knowledge-extractor
description: Systematic read-only codebase reverse engineering, architecture reconstruction, engineering audit, and three-layer knowledge extraction (Facts -> Principles -> Methods) to build internal maintenance archives and desensitized clean-room design blueprints across projects. Applicable to both Codex and Antigravity agent environments.
---

# Project Knowledge Extractor（工程逆向复盘与三层知识萃取工作流）

本技能用于对既有软件工程执行**只读、有代码证据支撑的系统性技术复盘**。其核心目标不仅是建立服务于当前项目维护的**内部技术档案（Internal Archive）**，更重要的是遵循 **“事实（Facts）→ 原理（Principles）→ 方法（Methods）”** 三层知识认知模型，将受限于单一项目的实现细节升维沉淀为**跨项目可复用的工程方法论与净室（Clean-Room）设计蓝图**。

---

## 1. 核心认知模型：“事实 · 原理 · 方法”三层分离法则

在复盘任何工程代码时，必须严格按以下三个层次组织认知与文档产出，防止“把业务流水账当成架构方法”或“把原项目代码改个变量名当成跨项目复用”：

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ 第三层：方法层 (Methods) ── 以后面对相似问题，如何独立、合规地完成设计与实现 │
│   • 载体：reuse/REUSE_01..05_*.md（完全脱敏、跨项目长期携带的核心资产）     │
│   • 要求：零专有信息残留 + 缺陷升维（主动修补原项目暴露的设计短板与安全漏洞）│
├────────────────────────────────────────────────────────────────────────────┤
│ 第二层：原理层 (Principles) ── 为什么这种技术方案能解决问题（机制与权衡）   │
│   • 载体：internal/10_ENGINEERING_DECISIONS.md & REUSE_03_TECH_DECISION    │
│   • 要求：剖析底层机制（如锁粒度、内存模型、索引结构）、适用边界、代价与局限│
├────────────────────────────────────────────────────────────────────────────┤
│ 第一层：事实层 (Facts) ── 当前项目实际上怎么做（客观现状与源码证据）         │
│   • 载体：internal/00..09_*.md & 11_EVIDENCE_AND_GAPS.md（授权范围内维护用）│
│   • 要求：100% 绑定文件路径与精确行号，严格区分文档声明/代码证实/推断/待验证 │
└────────────────────────────────────────────────────────────────────────────┘
```

### 三层知识的边界铁律
1. **事实层求“真”（Zero Hallucination）**：
   - 凡记录于内部档案的模型字段、状态枚举、API 路径、配置键名、超时阈值，**必须逐一核对源码定义**，严禁凭直觉或过时 SQL 脚本脑补不存在的字段或状态。
   - 严格标注信息来源四级标签：**`[A-文档声明]`**、**`[B-代码证实]`**、**`[C-逆向归纳]`**、**`[D-待验证]`**（位于外部仓库、外部服务或线上环境的未证实信息）。
2. **原理层求“透”（Mechanism & Trade-offs）**：
   - 不做依赖包清单罗列。每项关键设计必须回答：**解决了什么普遍工程矛盾？底层依赖了什么原语？代价是什么？规模扩大 10 倍后哪里会最先崩溃？**
3. **方法层求“纯”与“升维”（Clean-Room & Defect-Upgraded）**：
   - **合规净室红线**：跨项目复用文档（`reuse/`）中严禁出现原项目的业务名称、内部域名、内网 IP、明文密钥或可直接复原专有业务逻辑的代码片段。
   - **拒绝简单改名照搬**：严禁把原项目的类名/表名简单替换后原样贴入复用文档。必须结合第 4 阶段（Engineering Audit）发现的原项目缺陷，在方法层给出**经过缺陷修补的完备参考设计**（详见 [references/three-layer-extraction-guide.md](references/three-layer-extraction-guide.md)）。

---

## 2. 只读安全边界（Read-Only Execution Boundary）

执行本技能期间，默认处于**严格只读审计模式**：
- **严禁**：修改现有业务代码、重构项目、自动修复发现的 Bug、自动提交/推送被审计项目的 Git、在未获授权时执行有副作用的服务/连接生产外部系统、在任何文档中输出明文密钥/Token/密码。
- **允许**：全量阅读授权目录下的源码、配置、SQL、测试脚本；使用只读命令统计代码结构；在工作区授权目录（默认推荐 `docs/tech_archive/{internal,reuse}/`）创建知识档案。

---

## 3. 标准化六阶段工作流 + 独立评审门禁（6 Stages + 1 Review Gate）

严禁仅浏览少量入口文件就输出总结。必须按以下递进阶段推进：

| 阶段 | 阶段名称 | 主要产出文件 | 核心职责与后续用途 |
| :--- | :--- | :--- | :--- |
| **Stage 1** | **Project Discovery**<br/>（项目识别与目录映射） | `internal/00_INDEX.md`<br/>`internal/01_PROJECT_OVERVIEW.md`<br/>`internal/02_REPOSITORY_MAP.md` | **快速理解陌生项目**：厘清系统定位、解决的业务痛点、典型场景、输入输出、外部系统边界、代码树与模块职责矩阵，完成 `A/B/C/D` 证据分级。 |
| **Stage 2** | **Architecture Reconstruction**<br/>（技术栈与架构数据还原） | `internal/03_TECH_STACK.md`<br/>`internal/04_ARCHITECTURE.md`<br/>`internal/06_DATA_AND_STATE.md` | **架构评审与重构支撑**：从系统级、模块级、实现级还原架构；核实全量数据表、真实枚举值、Redis/缓存键空间与状态机，生成有代码证据支撑的 Mermaid 图。 |
| **Stage 3** | **Implementation Analysis**<br/>（核心链路与工程部署剖析） | `internal/05_CORE_WORKFLOWS.md`<br/>`internal/07_BUILD_AND_DEPLOY.md` | **内部维护与故障排障**：端到端追踪核心正向链路、**逆向取消/终止/超时链路**、监控告警链路；汇总跨服务消息契约字典、动态配置全量 Key 字典与部署排障 SOP。 |
| **Stage 4** | **Engineering Audit**<br/>（工程质量、风险与技术债审计） | `internal/08_TESTING_AND_QUALITY.md`<br/>`internal/09_TECHNICAL_DEBT.md` | **优化规划与安全加固**：12 维度量化评估；精准定位并严格区分**已确认功能 Bug**、**已确认安全漏洞**、**潜在扩展瓶颈**、**可选优化**与**纯粹风格偏好**。 |
| **Stage 5** | **Knowledge Extraction** ⭐<br/>（设计决策与通用模式提炼） | `internal/10_ENGINEERING_DECISIONS.md`<br/>`reuse/REUSE_01_ARCHITECTURE_PATTERNS.md`<br/>`reuse/REUSE_02_ENGINEERING_PLAYBOOK.md`<br/>`reuse/REUSE_03_TECH_DECISION_GUIDE.md`<br/>`reuse/REUSE_04_PROJECT_CHECKLIST.md` | **跨项目技术资产积累**：按 9 段式结构萃取 12 维工程经验；将项目验证过的设计提炼为脱敏且修补了原缺陷的通用架构模式、研发铁律、选型矩阵与核查清单。 |
| **Stage 6** | **Clean-room Design** ⭐<br/>（净室新系统设计蓝图） | `reuse/REUSE_05_CLEAN_ROOM_BLUEPRINT.md` | **合规独立开发同类系统**：输出《从零设计同类技术系统的方法指南》，采用通用中立领域场景，从零设计领域模型、核心调度算法、安全防线与可观测体系。 |
| **Gate 7** | **Adversarial Self-Review**<br/>（独立技术评审与防幻觉门禁） | `internal/11_EVIDENCE_AND_GAPS.md`<br/>（含覆盖矩阵与质量评估报告） | **交付前强制自检**：以独立评审者视角执行十维反事实核查，消灭捏造字段/枚举、假脱敏与证据断链（详见 [references/adversarial-review-checklist.md](references/adversarial-review-checklist.md)）。 |

---

## 4. 关键阶段防坑铁律（实战教训结晶）

### 4.1 Stage 2 & Stage 3 事实核验五大防幻觉红线
1. **同名模型/死代码消歧**：当项目中存在多个同名类或历史遗留文件时，必须追踪 `router.py` 与 `crud/*.py` 的真实 `import` 路径，明确指出哪个模型/接口实际生效，哪个属于未挂载的废弃死代码。
2. **ORM 枚举与字段逐行对齐**：绘制 ER 图和状态机图前，必须直接读取 ORM 模型源码的 `Enum` 定义与 `mapped_column` 列表，严禁把旧版 `.sql` 脚本中的废弃字段当成当前 ORM 字段，严禁自行脑补状态枚举（如看到 `PENDING/RUNNING/TERMINATED` 就凭空脑补 `CANCELLED/TIMEOUT`）。
3. **物理外键 vs 逻辑关联区分**：在 ER 图中必须区分数据库级 `ForeignKey` 与应用层无约束 `JOIN`（或 ORM `primaryjoin`）。
4. **正向与逆向链路对称追踪**：分析任务调度时，不能只看 Happy Path（创建→执行→成功回调），**必须同等深度追踪逆向路径（单条取消、批量取消、强制终止、超时巡检）**，重点核查逆向路径是否正确释放了已加锁的设备/资源。
5. **长轮询 vs 高频短轮询辨析**：看到 `while ...: await asyncio.sleep(0.2)` 时，必须确认它是服务端长轮询内部循环还是客户端 HTTP 轮询，严禁误判中间件写库频率。
6. **必须生成两张维护字典表**：
   - **《跨进程/跨仓库消息载荷契约表》**（如所有 `send_task` 的任务名、`args/kwargs` 结构与目标队列规则）。
   - **《动态配置键全量字典表》**（代码中所有读取数据库配置表的 Key 名、值格式、默认值与消费位置）。

### 4.2 Stage 5 & Stage 6 知识升维准则（按需加载）
在进入 **Stage 5（Knowledge Extraction）** 与 **Stage 6（Clean-room Design）** 前，**必须先阅读 [references/three-layer-extraction-guide.md](references/three-layer-extraction-guide.md)**，严格按照其中的 9 段式决策模板与“缺陷升维净室重构法”编写 `10_ENGINEERING_DECISIONS.md` 与 `REUSE_01..05` 文档。

### 4.3 Gate 7 独立评审门禁（按需加载）
在完成初稿准备收尾前，**必须阅读并执行 [references/adversarial-review-checklist.md](references/adversarial-review-checklist.md)** 中的 10 项质询检查，订正所有失真点后再输出最终报告与覆盖度矩阵。

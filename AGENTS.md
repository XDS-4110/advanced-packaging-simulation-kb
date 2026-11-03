# AGENTS.md

面向进入本仓库的自动化代理。**优先级高于 CONTRIBUTING.md**；两者冲突时以本文件为准，并提 issue 说明冲突。

---

## 这个仓库是什么

为 LLM 驱动的先进封装建模与仿真提供**可追溯的判据、来源、状态与接口契约**。
基线：ANSYS Workbench / Mechanical 2024 R2，瞬态热-力顺序耦合；当前案例为 BGA（未求解），后期为 2.5D。

它**不**提供：可执行求解器、已验证的仿真结果、可直接填入模型的工程数值。

仓库里没有已验证结论。任何"这个参数可以这样设"的说法，都必须能追到条目 ID + 来源编号 + 原文定位。

---

## 五条铁律

**1. 数值只能来自检索结果，不能由模型生成。**
工程数值一律通过 `kb_lookup` 取得，并随值返回 `unit`、`source_locator`、`status`。
禁止：根据"常见值"补全、从正文断章取义、按相似材料外推、按单位习惯换算后不回填来源。

**2. 只有 `usable_for_arguments=true` 的内容可以写入工具参数。**
`kb_search` 返回的每条结果都带该字段。为 `true` 仅当状态为 `reviewed` 或 `validated`。
`draft` 内容只能用于解释、排错、给建议，**不得**作为 `arguments` 的取值来源，也不得据此判断"这样设是对的"。

**3. 写操作前必须通过契约校验。**
请求必须符合 `shared/tools/tools.schema.json`（当前 0.1.0，仅 `preview_only`）。
执行开关当前为 `false`；被 `unresolved` 项阻塞时，如实报告阻塞编号（如 `U-GEOMETRY-PARAMETER`），**不得绕过**，不得自行编造 API 方法名。

**4. 每个写请求必须带 `request_id` 并留档。**
去重键为 `request_id`；同 ID 不同载荷拒绝、在途请求不重复派发、部分写入先核对再继续。
禁止：自动重试、换一个新 ID 绕过未决状态。

**5. 未知即"待补充"。**
不填猜测值、不用默认值顶替、不把"没查到"写成"没有"。
报告时区分三件事：**已核对文档** / **已运行验证** / **尚未验证**。

---

## 几何参数修改（SolidWorks）

改几何尺寸**只能**通过参数表，不允许猜尺寸名、不允许直接调 SolidWorks API：

```bash
python tooling/sw_params.py show
python tooling/sw_params.py list
python tooling/sw_params.py set die_thickness 0.40
```

规则：

1. 只能修改 `geometry-parameters.csv` 中登记的 A 类（尺寸）参数；B 类（阵列）与 C 类（拓扑）需人工确认。
2. `set` 默认在副本上操作、不保存；确认无误后加 `--commit` 才写回。
3. 长宽高单位是 **mm**，写入时由工具换算成米；角度用度。**不得手工写 SystemValue**。
4. 改完必须回读 `after` 与 `verified`；`verified=false` 视为失败。
5. 记录改动前后的值、零件、尺寸名，写入案例记录。
6. 看 `stack_axis`、`interferes_with`、`compensation` 三列：**z 向尺寸改完必须跑干涉检查**；干涉体积约等于"面积 × 增量"时，说明堆叠未随动（见案例 `15-geometry-change-interference.md`），不是建模错误。

---

## 目录地图

| 路径 | 内容 | 是否进检索索引 |
| --- | --- | --- |
| `packaging/` | 封装知识：common / bga / 2-5d | 是（reviewed 以上） |
| `simulation/` | 仿真知识：建模、热、结构、材料输入、软件操作、验证、案例 | 是 |
| `shared/materials/` | 材料 ID 与 revision、原始属性表 | 是 |
| `shared/entities/registry.csv` | `stable_id` 权威注册表 | 否（供 lookup） |
| `shared/tools/tools.schema.json` | 执行契约（0.1.0，preview-only） | 否 |
| `shared/tools/validate_contract.py` | 契约静态校验器 | 否 |
| `shared/rag/` | 检索语料规范与 profile | 否 |
| `tooling/` | 检索代码与 MCP 服务 | 否 |
| `files/` | PDF（Git LFS 指针，正文不可读） | 否 |

---

## 开场三件事

```bash
python tooling/kb_retrieve.py info                      # 1. 确认语料哈希与文档数
python tooling/kb_retrieve.py resolve <stage>           # 2. 取该阶段应读的文档
python tooling/kb_retrieve.py lookup <entity> [prop]    # 3. 需要数值时才查表
```

`info` 的 `corpus_sha256` 与预期不符时，先停下核对仓库版本，**不要**在语料不一致的前提下继续作答。

可用阶段见 `shared/rag/thermal-structural-profile.json`：
`geometry-materials`、`scope-contacts`、`meshing`、`transient-thermal`、`temperature-transfer`、`solve-results`。

---

## 修改仓库的流程

**新增知识条目**
1. 先在 `shared/references/catalog.csv` 登记来源，取得 `SRC-` 编号；
2. 从 `shared/templates/` 复制对应模板；
3. `status: draft`，`reviewed_by` / `reviewed_at` 留空；
4. 文件名小写英文 + 连字符；一篇回答一个问题。

**修改注册表或结构模板**
1. 改文件 → 2. 同步更新 `tools.schema.json` 里的 `entity_policy.registry_sha256` / `package_structure_template.sha256` → 3. 重跑 `python shared/tools/validate_contract.py --record`。
三步缺一步，CI 会红。

**改代码**
只放 `tooling/`。不得让 `shared/` 下的知识条目依赖代码实现。

**提交**
新分支 + PR，不直推 `main`。PR 描述需含：文件清单、新数值的来源定位、留空字段及原因、未验证项。

**提交前必须同步 main。** 本仓库有多个协作者同时写入，本地副本很容易落后：

1. 先拉取最新 `main`（`git fetch && git merge origin/main`，或重新下载），确认本地与远端一致；
2. 把本地改动**重新叠加**到最新版本上，不要整文件覆盖；
3. `catalog.csv` 只允许**追加行**，禁止整文件替换——那会删掉别人的来源登记；
4. 同步后重算基线：`python tooling/kb_retrieve.py info`，更新 `corpus-baseline.json` 与 `tooling/README.md`；
5. 跑 `python tooling/ci_check.py`，通过后再提交。

**判断是否落后**：`info` 报 `documents` 与 main 的 md 数量明显不符，或 `baseline_match=false`，即为落后，先同步。

---

## 报告格式

回答工程问题时，至少给出：

1. **结论** —— 一句话；
2. **依据** —— 条目 ID / `SRC-` 编号 / 文件与章节定位；
3. **状态** —— 该依据是 `draft` 还是 `reviewed`，是否经过运行验证；
4. **缺口** —— 哪些必需信息仍缺，卡在哪个 `U-` 编号。

---

## 禁止清单

- ❌ 编造 API 名称、参数名或方法签名；对不上官方文档就标 `unresolved`
- ❌ 用常见值 / 经验值 / 相邻牌号推断填充未知参数
- ❌ 把 `draft` 升为 `reviewed`（只有人类审核人可以做）
- ❌ 用显示名（`SI`、`tem`、`CMB97D39B|XINPIAN|____-____1`）当作 `stable_id`
- ❌ 把"脚本跑通"表述为"物理模型已验证"
- ❌ 修改 `shared/rag/` 的索引范围或状态白名单
- ❌ 在 `main` 上直接提交

---

## 当前已知阻塞（回答时要主动说明）

| 编号 | 内容 |
| --- | --- |
| `U-GEOMETRY-PARAMETER` | Workbench 侧无参数集；**尺寸修改已改由 SolidWorks 参数表承担**（见「几何参数修改」一节）。Workbench 内仍无法直接改尺寸，只能换文件或改位置 |
| `U-RUNTIME` | `ansys-mechanical-core` 版本与所连会话身份未确认 |
| `U-SAVE` | 保存与重开的一致性无证据 |
| `U-RETRY` | 请求日志存储、指纹与恢复机制未实现 |

完整清单见 `shared/tools/unresolved.md`。

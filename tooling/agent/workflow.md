# 仿真工作流：阶段、检查点与停止条件

配套 [AGENTS.md](../../AGENTS.md) 使用。本文件回答**每一步该做什么、做完按什么验收、什么情况下必须停下来问人**。
不提供任何工程数值；数值一律来自 `kb_lookup`。

## 全局规则

1. 开场先 `kb_retrieve.py info`，确认 `corpus_sha256`。
2. 每个阶段先 `kb_retrieve.py resolve <stage>`，按返回文档工作，不自行扩大阅读范围。
3. 需要数值时 `kb_lookup`，不用默认值、不外推。
4. **上一阶段的检查点未通过，不进入下一阶段。**
5. 每阶段产出带：对象、单位、时刻、作用域、来源定位。

## 阶段表

| # | stage | 主要文档 | 核心检查点 | 强制停止条件 |
| --- | --- | --- | --- | --- |
| 1 | `geometry-materials` | OPS-01 | 实体清单与命名、单位、每个实体的 material ID + revision | 要改尺寸时（`U-GEOMETRY-PARAMETER`）；实体无 `stable_id` |
| 2 | `scope-contacts` | OPS-02 | 命名选择可重建、接触源/目标无错连、热接触设置 | 作用域只有显示名、无面 ID |
| 3 | `meshing` | OPS-03、KB-PROJECT-MESH-001 | 单元数、质量指标、重要区域人工确认 | 超 300 万单元；低质量单元需例外批准 |
| 4 | `transient-thermal` | OPS-04、案例 10-thermal-ui-scope | 初温、载荷表完整、作用域、时步设置 | 初温与载荷表首点冲突未裁定；作用域与命名选择不一致 |
| 5 | `temperature-transfer` | OPS-05 | 源分析、时刻映射、目标覆盖、未映射区域 | 源结果与目标分析不属同一修订；时刻表缺项 |
| 6 | `solve-results` | OPS-06 | 求解状态、温度映射核对、结果量纲与作用域 | 热/结构任一未求解；把 Total Deformation 当翘曲 |

## 每阶段详细

### 1 geometry-materials

- **改尺寸时**：`python tooling/sw_params.py set <逻辑名> <值>`，参数表见 `simulation/cases/bga-2024r2-unsolved/data/geometry-parameters.csv`；改完回读 `verified`，并把 before/after 写入案例记录。**不要直接调 SolidWorks API 或猜尺寸名。**

- **调**：`resolve geometry-materials`；`lookup ENT-*`；`lookup MAT-*`
- **检查**：实体数量与名称、装配单位、每个实体的材料 ID+revision 是否与注册表一致
- **产出**：实体清单表（stable_id / 名称 / 材料 / revision / 来源）
- **停**：需要改尺寸 → 报 `U-GEOMETRY-PARAMETER`，说明只能换文件或改位置

### 2 scope-contacts

- **调**：`resolve scope-contacts`；`lookup ENT-BGA-NS-*`
- **检查**：命名选择能否由面 ID 重建；接触对是否为全 Bonded；热接触是否单独定义
- **产出**：作用域与接触清单
- **停**：作用域仅有截图、无面 ID；接触行为与物理意图不符

### 3 meshing

- **调**：`resolve meshing`；`lookup` 网格规范条目
- **检查**：单元数、雅可比/长宽比、重要区域（焊球、凸点、界面）是否加密
- **产出**：网格统计 + 验收结论
- **停**：超 300 万单元；低质量单元需人工批准

### 4 transient-thermal

- **调**：`resolve transient-thermal`；案例条目（draft，仅解释用）
- **检查**：初温来源、载荷表点数与时刻、作用域、自动时步设置
- **产出**：载荷表 + 作用域 + 时步摘要
- **停**：初温与载荷表首点不一致未裁定；作用域与命名选择不匹配

### 5 temperature-transfer

- **调**：`resolve temperature-transfer`
- **检查**：源热分析身份、源时刻→结构时刻映射、目标实体覆盖、未映射区域
- **产出**：映射表 + 覆盖检查
- **停**：源与目标不属同一模型修订；存在未解释的未映射区域

### 6 solve-results

- **调**：`resolve solve-results`
- **检查**：两个分析的求解状态分别记录；温度映射已核对；结果含对象/单位/时刻/作用域
- **产出**：结果摘要 + 判读结论
- **停**：任一分析未求解；要求给出疲劳寿命但无标定依据

## 通用停止条件

出现以下任一情况，**停止并提问**，不要自行补齐：

- 需要填入的数值在 `kb_lookup` 中取不到
- 目标实体无法解析为 `stable_id`
- 两个来源对同一量给出不同值
- 需要调用契约中 `status: unresolved` 的能力
- 用户要求"先跑通再说"

## 结果表述

- 区分 **已核对文档** / **已运行验证** / **尚未验证**
- 不说"仿真结果正确"，只说"在本组设置与验收条件下未发现异常"
- 翘曲必须说明目标面、方向、参考平面

## 待补充

- 各阶段的时间预算与人工确认人
- 2.5D 阶段的对应表（待 2.5D 知识补齐后编写）

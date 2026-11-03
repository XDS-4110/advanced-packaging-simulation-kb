---
id: KB-DATA-DICT-001
title: "数据集字段字典：BGA 案例与材料快照"
document_type: knowledge
domain: shared
status: draft
language: zh-CN
tags: [data-dictionary, dataset, bga, material, provenance]
physics: [thermal, structural]
software: [ANSYS Workbench, ANSYS Mechanical]
software_versions: ["2024 R2"]
source_ids: [SRC-BGA-001]
source_locator: "simulation/cases/bga-2024r2-unsolved/data/ 下各文件表头与抽样行；shared/materials/datasets/ 各表头"
updated_at: "2026-11-02"
reviewed_by: ""
reviewed_at: ""
---

# 数据集字段字典：BGA 案例与材料快照

> 说明列名含义、单位与常见误用。不是数据本身，也不替任何数值背书。所有指向均相对本仓库根目录。

## 为什么需要本页

本库的结构化数据来自 Workbench 导出与界面提取，列名是英文、单位常藏在列名里，且**多处列名与实际语义不一致**。直接把这些 CSV 当接口输入会产生静默错误（例如把材料名称当 material ID）。本页只解释字段，不修改数据。

## simulation/cases/bga-2024r2-unsolved/data/bodies.csv

322 行，每个实体一行。

| 列 | 含义 | 单位/取值 | 误用风险 |
| --- | --- | --- | --- |
| object_id | Workbench 内部对象编号 | 整数 | **不是** registry 的 stable_id；跨修订可能失效 |
| part_id | CAD 部件编号 | 整数 | 与 object_id 非一一对应 |
| name | Workbench 显示名 | 字符串 | **不可作键**：中文曾被导出为下划线（如 `CMB97D39B|TUDIAN|____1[25]`） |
| material | 材料**名称** | 如 `SI`、`BT`、`Sn63Pb37` | **不是** `MAT-BGA-*` ID；同名不等于同一 revision |
| bbox_diagonal_mm | 包围框对角线 | mm | 不是任何真实尺寸；不能当直径或厚度 |
| mass_tonne | 质量 | **吨** | 单位是 tonne，不是 kg；易被当成 kg 放大 1000 倍 |
| centroid_x/y/z_mm | 质心坐标 | mm | 坐标系原点与装配坐标系的关系未在本文件说明 |

## contacts.csv

643 行，每行一对接触。

| 列 | 含义 | 说明 |
| --- | --- | --- |
| object_id | 接触对象编号 | 与 bodies.csv 的 object_id 不同域 |
| type | 接触类型 | 本快照 643 行**全部为 Bonded**，无摩擦/无分离接触 |
| source_body_ids / target_body_ids | 源/目标实体 | 与 bodies.csv 的 object_id 对应 |
| formulation / behavior | 算法与行为 | 取值见导出原文 |
| scoping_ids | 作用域编号 | 与命名选择相关 |
| maximum_offset_mm / trim_tolerance_mm | 几何容差 | mm |

**注意**：全 Bonded 意味着界面在热和结构上都按绑定处理。结合 06-missing-information.md 中"未识别到明确支撑对象"，结构侧可能同时存在过约束与欠约束，需按 12-structural-evidence-checklist.md 取证，不能据本表推断边界条件合理。

## analysis-steps.csv

21 行，累计到 18600 s。

| 列 | 含义 | 说明 |
| --- | --- | --- |
| step | 步号 | 1–21 |
| end_time_s / duration_s | 结束时刻与持续 | 秒 |
| auto_time_stepping | 自动时间步 | 本快照全为 `ProgramControlled` |
| time_integration | 时间积分开关 | 布尔 |

**已知不一致**：10-thermal-ui-scope.md 记录"第 14 步结束 12990 s"，与本表 21 步 / 18600 s 不同源。引用时必须写明取自哪份证据及其修订，不得混用。

## temperature-history.csv

22 行，0–18600 s。

| 列 | 含义 | 单位 | 误用风险 |
| --- | --- | --- | --- |
| time_s | 时刻 | s | — |
| temperature_degC | 温度 | **°C** | 本库内部单位规定为 K；引用时须换算并标注来源单位 |

**已知不一致**：本表首点为 25 °C，而 thermal-settings.json 的 `InitialTemperature` 为 22 °C。二者可能分属"载荷表"与"初始条件"，但未经核实前不得互相替代。

## thermal-settings.json

瞬态热设置的键值导出，形如 `{ "value": "...", "unit": "..." }`。

- `initial_conditions.InitialTemperature`：22 °C（见上方不一致说明）。
- `loads[]`：每项含 `tag`、`id`、`properties`（Caption / Scoping 等）。
- 数值全部以字符串存储，**不是** 数值类型；直接参与计算前需显式转换。

## shared/materials/datasets/*/material-parameters.csv

材料属性的原始导出。

| 列 | 含义 | 说明 |
| --- | --- | --- |
| material | 材料名称 | 非 ID |
| property / parameter | 属性与参数名 | 与 Engineering Data 字段名不完全一致 |
| raw_values | 原始值 | 字符串；存在 `7.88860905221012e-31` 这类浮点噪声，应视为近似零而非真实值 |
| unit_as_exported | 导出单位 | 可能与 SI 不同 |
| temperature_axis_degC | 温度轴 | °C |
| property_qualifiers / temperature_qualifiers | 限定条件 | JSON 字符串，含字段变量与本地化名 |

## simulation/materials/data/bga-input-mapping.csv

材料属性到 Engineering Data 字段的映射表。

- `auto_apply_approved` 本快照全为 `false`：**禁止自动套用**。
- `engineering_data_property` 是目标字段名，不等于已验证可用。

## simulation/materials/data/bga-review-checklist.csv

材料输入审核清单，`status` 取 `pending` / `partial_evidence` 等；`evidence` 列写依据来源。检查项状态不等于材料已批准。

## object-names.json

2332 条 `{object_id, type_code, name}`。

- `type_code` 是私有整数（如 105、148），**不可反推对象类型**，也不构成 API 语义。
- 仅用于把历史对象编号与显示名对上；不是当前会话的身份来源。

## source-manifest.json

- `file_hashes`：原始工程的逐文件 SHA-256。
- `archive_snapshot.sha256`：归档快照整体哈希，registry.csv 的 `model_revision` 取值即此值。
- `archive_snapshot.sha256_verified_entries`：参与校验的文件清单。

## shared/entities/registry.csv

实体引用的权威来源，字段含义见 12-structural-evidence-checklist.md 与 tools.schema.json 的 `entity_policy`。要点：

- `stable_id` 是项目主键，**不是** ANSYS 原生 ID；
- `model_revision` 为空的行禁止被任何 `entity_ref` 引用；
- `aliases` 仅在给定 `case_id` 与 `model_revision` 时可解析。

## 通用规则

1. 任何列名带单位的，以列名为准；不得按习惯假定 SI。
2. 名称为字符串的列（material、name）**一律不当作 ID**。
3. 同一量在不同文件中数值不一致时，保留两处来源并标注修订，不取平均、不择一覆盖。
4. 引用数据集时给出文件路径 + 行定位 + 文件哈希。

## 待补充

- bodies.csv 质心坐标系与装配坐标系的关系；
- contacts.csv 中 `scoping_ids` 与命名选择对象的对应；
- 上述两处已知不一致的裁定（哪份代表当前工程修订）。

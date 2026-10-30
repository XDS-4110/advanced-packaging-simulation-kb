---
id: KB-MATINPUT-005
title: "BGA 材料输入：待补资料与完成判据"
document_type: knowledge
domain: simulation
status: draft
language: zh-CN
tags: [material-input, Workbench-2024R2, thermal-stress, thermal-cycling]
physics: [thermal, structural]
software: [ANSYS Workbench, ANSYS Mechanical]
software_versions: ["2024 R2"]
source_ids: [SRC-BGA-001, SRC-ANSYS-242-ENGDATA, SRC-ANSYS-242-ANAND]
source_locator: "见文末官方资料与公共材料记录"
updated_at: "2026-10-30"
reviewed_by: ""
reviewed_at: ""
---

# BGA 材料输入：待补资料与完成判据

> 初版知识草稿：官方字段已核对，界面步骤尚未在本地工程逐项复现；未求解，未完成材料物理标定。

## 当前进度

已有文件提取、材料赋值、单位归一化和问题登记；来源审核、界面复现与材料响应验证尚未完成，保持 draft。

## 逐材料补充

| 公共材料 ID，均为 revision 1 | 优先补充 |
| --- | --- |
| MAT-BGA-SI-001 | 数据出处、晶向与各向同性近似依据 |
| MAT-BGA-UNDERFILL-001 | 牌号、固化状态、Tg/试验及是否需时间相关模型 |
| MAT-BGA-SN63PB37-001 | 原始 Anand 表、m/h0 对应、温区与速率范围 |
| MAT-BGA-BT-001 | 基板与 PCB 是否确实可共用定义；真实叠层/方向 |
| MAT-BGA-SFL-001 | 牌号、固化、低温数据、Tg/松弛依据 |

## 下一步提供资料

1. 五种材料在 Engineering Data 中的属性总览，显示材料名、属性类型和单位。
2. **优先给出 Sn63Pb37 的 Anand 全表、Reference Units 和原始参数出处。**
3. 焊料 E/ν 与 CTE 的完整温度表，以及 SFL 对应温度表。
4. Mechanical 中主要部件材料赋值的截图或导出。

可以分批提供。出处缺失写“待核对”，不从工程数值反向编造来源。填写 [审核清单](data/bga-review-checklist.csv)；新数据另存 revision，不覆盖原工程快照。

## 分层完成判据

- 输入核对完成：身份、数值、单位、温度轴、定义及赋值都有证据。
- 来源审核完成：原始出处与适用条件已核实，由审核人按规则标 reviewed。
- 响应验证完成：以后通过合适算例或试验验证，注明范围后标 validated。

当前不求解，也可推进前两阶段。来源审核与物理验证分别记录。

## 来源

[BGA 公共材料记录](../../shared/materials/bga-2024r2-import.md)、[原案例补充清单](../cases/bga-2024r2-unsolved/06-missing-information.md) 及本专题前四篇的官方定位。

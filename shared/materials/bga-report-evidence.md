---
id: MAT-BGA-REPORT-EVIDENCE-001
title: "BGA 报告材料证据及与工程的差异"
document_type: material
domain: shared
status: draft
language: zh-CN
tags: [BGA, thermal-cycling, report-evidence, not-reproduced]
physics: [thermal, structural]
software: [ANSYS Workbench]
software_versions: []
source_ids: [SRC-BGA-REPORT-001, SRC-BGA-001, SRC-ANSYS-242-ANAND]
source_locator: "报告章节/表图号及原文块索引见正文和提取清单；不使用未经核实页码"
updated_at: "2026-10-30"
reviewed_by: ""
reviewed_at: ""
---

# BGA 报告材料证据及与工程的差异

> 报告来源知识，未独立复现。报告的已求解结果与当前未求解工程分开记录；冲突参数不自动采用。

## 记录身份

本记录是报告来源证据，关联现有 BGA 五种材料 ID 以便对照，不是替换工程 revision 1 的新认可参数。工程快照仍见 [原记录](bga-2024r2-import.md)。报告作者、日期、具体软件发行版本及材料原始标定出处尚未明确。

## 提取数据

- [3 个原始表格，保留合并单元格和数学符号](datasets/bga-report-draft/report-tables.json)
- [65 条按报告单位整理的属性数据](datasets/bga-report-draft/report-material-properties.csv)
- [与工程的逐项对照](datasets/bga-report-draft/report-vs-project.csv)

表 2-1 的焊料“见表2-2”跨 E、ν、CTE 三列，不把其后的 50 错读为泊松比；比热表头为 J/(g·K)。

## 已确认的文件差异

| 项目 | 报告 | 当前工程快照 | 处理 |
| --- | --- | --- | --- |
| Anand m | 0.303 | 2640.75 | 名称—数值对应不一致，待用户确认后另存修订 |
| Anand h0 | 2640.75 MPa | 0.303（参考应力单位 MPa） | 不自动交换或覆盖 |
| 塑封料比热 | 0.79 J/(g·K)，换算 790 J/(kg·K) | 0.79 cal/(g·K)，导出 3305.36 J/(kg·K) | 单位来源冲突，不是普通换算后相同 |
| 焊料 E、ν 的温度轴 | -55,-35,-15,5,12,50,75,100,125 ℃ | -55,-35,5,12,15,50,75,100,125 ℃ | 各有 3 个配对温度点不同 |

65 条属性对照中，56 条数值与配对温度轴一致，9 条有差异（m/h0 两条、比热一条、E/ν 温度轴六条）。此统计不证明那些一致参数已获得物理标定。

## 报告自身也需复核

- 表 2-3 把 Q/R 单位标为 1/K；与其定义量纲及 ANSYS 输入含义不一致，不能原样传播。
- m 与 h0 的中文解释与 ANSYS 定义不对应；对照采用参数符号，保留原文标签。
- 最后一项写作 α，需与 Anand 的 a 及 CTE 符号区分。
- 报告未明确瞬时/割线 CTE，不能用它证明工程的 Instantaneous 选择正确。
- 表格仍未覆盖所有 -55～150 ℃ 循环区间，原材料出处与外推依据仍待补。

## 来源

SRC-BGA-REPORT-001：第2.2节、表2-1～2-3；SRC-BGA-001：原材料导出。
[ANSYS 参数定义](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ans_thry/thy_mat2.html) 仅用于字段/量纲核对，不批准报告中的参数。

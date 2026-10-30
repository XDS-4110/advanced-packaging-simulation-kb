---
id: KB-VERIFY-BGA-REPORT-001
title: "BGA 报告结果与独立验证的区别"
document_type: knowledge
domain: simulation
status: draft
language: zh-CN
tags: [BGA, thermal-cycling, report-evidence, not-reproduced]
physics: [thermal, structural]
software: [ANSYS Workbench]
software_versions: []
source_ids: [SRC-BGA-REPORT-001, SRC-BGA-001]
source_locator: "报告章节/表图号及原文块索引见正文和提取清单；不使用未经核实页码"
updated_at: "2026-10-30"
reviewed_by: ""
reviewed_at: ""
---

# BGA 报告结果与独立验证的区别

> 报告来源知识，未独立复现。报告的已求解结果与当前未求解工程分开记录；冲突参数不自动采用。

## 报告结果（未独立复现）

| 对象 | 时刻 s | 报告最大等效应力 MPa | 位置与原文 |
| --- | --- | --- | --- |
| 芯片 | 18600 | 54.054 | 边角，图3-1 |
| 凸点 | 16776.6 | 62.471 | 芯片接触边缘，图3-3 |
| 凸点 | 18600 | 27.554 | 危险凸点上半部，图3-4 |
| 焊球 | 16776.6 | 41.552 | BT基板接触面/边缘，图3-6 |
| 焊球 | 18600 | 18.814 | BT基板接触面，图3-7 |

正文数值与对应原图图例已核对。图例注明 Equivalent (von-Mises) Stress、MPa 和时刻。原始数据见 [报告结果表](../references/bga-thermal-reliability-report/author-reported-results.csv)。

## 证据边界

报告有结果，不等于当前用户的未求解工程有这些结果。原图时间戳来自2024年，但不证明报告软件发行版本，更不能作为当前工程求解日志。

不能用这些峰值直接验收：报告—工程材料仍有明确差异，且约束、网格、温度映射、应力平均/外推方式未完整对应。后续应先统一输入，再比较相同实体、时刻、提取方法和误差定义。

报告没有可核验的翘曲数值、网格独立性、热平衡或寿命验证；不能将“未列出”当成“通过”。局部峰值还需检查奇异性及网格敏感性。

## 来源

SRC-BGA-REPORT-001 第3.1～3.3节、图3-1～3-7；SRC-BGA-001 为现有工程快照。

---
id: KB-CYCLE-BGA-REPORT-001
title: "BGA 报告温度循环与当前工程的对应"
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

# BGA 报告温度循环与当前工程的对应

> 报告来源知识，未独立复现。报告的已求解结果与当前未求解工程分开记录；冲突参数不自动采用。

## 报告工况

第2.3节（P031）与图2-4描述：器件外表面施加温度循环，5个循环；高温150 ℃、低温-55 ℃，高低温各保温30 min，升降温各1 min，总时长18600 s。该图展示总体历程，不足以精确还原全部采样时刻。

当前工程同样具有-55～150 ℃、18600 s的载荷表，但起始与返回25 ℃、22 ℃初温及作用面ID仍须单独核对。报告给出“外表面”意图，不能据此证明工程对象5948与命名选择tem的精确面集合正确。

## 载荷步描述的差异

报告称“每个循环一个载荷步，每步10个子步”；现有热分析导出却为21个StepControls且时间步程序控制。结构分析的完整步表尚未恢复。

因此记录为报告策略与当前热分析设置的差异，不能把报告的5×10直接覆盖热/结构两端，也不能据此认定某个文件一定错误。需要取得实际结构设置和报告所对应工程版本。

报告标注应力峰值时刻16776.6 s；工程温度载荷低温平台起点为16770 s。二者可因结果采样或不同工程快照而不同，不将报告时刻直接替代载荷拐点。

## 来源

SRC-BGA-REPORT-001 第2.3节、图2-4及第3.2/3.3节；[现有工程温度记录](../cases/bga-2024r2-unsolved/04-temperature-cycle.md)。

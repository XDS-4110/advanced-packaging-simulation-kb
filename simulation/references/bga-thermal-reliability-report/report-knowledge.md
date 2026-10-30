---
id: KB-BGA-REPORT-001
title: "BGA 报告中的方法与适用范围"
document_type: reference_note
domain: simulation
status: draft
language: zh-CN
tags: [BGA, thermal-cycling, report-evidence, not-reproduced]
physics: [thermal, structural]
software: [ANSYS Workbench]
software_versions: []
source_ids: [SRC-BGA-REPORT-001]
source_locator: "报告章节/表图号及原文块索引见正文和提取清单；不使用未经核实页码"
updated_at: "2026-10-30"
reviewed_by: ""
reviewed_at: ""
---

# BGA 报告中的方法与适用范围

> 报告来源知识，未独立复现。报告的已求解结果与当前未求解工程分开记录；冲突参数不自动采用。

## 报告描述的方法

- 第2.1节（P010）采用 Transient Thermal → Transient Structural 的顺序温度场传递；图2-1也显示共享材料、几何/模型及热 Solution 到结构 Setup 的连接。
- 第2.2节（P014、P017）称几何来自实物测量与器件手册，在 SolidWorks 建模；没有给出可恢复的详细尺寸表。
- 结构包括塑封料、芯片、凸点、Underfill、BT 基板和焊球；图2-3显示层叠与 Underfill 包围凸点。
- 作者为凸点、焊球采用 Sn63Pb37 和 Anand 模型，其他材料参数见公共材料证据。

这些是报告的方法记录，不证明当前工程已具有相同支撑、网格或求解状态。报告未明确 ANSYS 具体发行版本。

## 可复用的方法知识

建立结构—材料—载荷—约束—温度传递—结果评价的记录链。分别评价芯片、凸点和焊球，区分全时程峰值和结束时刻残余应力。对角部与界面高应力，保留网格/接触/应力提取定义后再讨论其物理意义。

## 不能转成通用规则的表述

- “超过熔点一半”未明确绝对温标、标定条件及材料范围，不作为自动选 Anand 的阈值。
- 作者对降温应力的“冷作硬化”解释缺少分解证据，不据此建立普遍因果规则。
- 高应力位置不等于已证明开裂、失效或疲劳寿命；报告没有提供独立的寿命标定、失效试验或完整损伤计算。
- 报告引言的失效率统计没有在本次核对其原始来源，不作为知识库事实结论。

## 仍缺失的信息

支撑自由度/作用域、无应力参考温度、接触算法/热导、网格质量/收敛、结构时间积分/非线性详细设置、真实映射结果及工程与报告的版本对应关系，均没有完整可复现证据。

## 资料定位

[提取清单与文件哈希](source-manifest.json)；[报告引用的六条文献线索](cited-literature-leads.csv) 仅为二次引用，尚未阅读原文；[材料证据](../../../shared/materials/bga-report-evidence.md)。

本次整页渲染因缺少配套 LibreOffice 可执行文件而失败；文字和原生表格按 OOXML 核对，16幅原图直接检查，没有使用未经验证页码。

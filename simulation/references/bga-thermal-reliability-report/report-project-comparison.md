---
id: KB-BGA-REPORT-COMPARE-001
title: "BGA 报告与工程的差异及处理决策"
document_type: knowledge
domain: simulation
status: draft
language: zh-CN
tags: [BGA, thermal-cycling, report-evidence, not-reproduced]
physics: [thermal, structural]
software: [ANSYS Workbench]
software_versions: []
source_ids: [SRC-BGA-REV2-001, SRC-BGA-REPORT-001, SRC-BGA-001, SRC-ANSYS-242-ANAND]
source_locator: "报告章节/表图号及原文块索引见正文和提取清单；不使用未经核实页码"
updated_at: "2026-10-30"
reviewed_by: ""
reviewed_at: ""
---

> 当前修订提示：本页对应初次工程快照。最新Engineering Data的m/h0及弹性温度轴已对齐报告，SFL比热仍有差异，见 [revision 2](../../../shared/materials/bga-20261030-revision2.md)。


# BGA 报告与工程的差异及处理决策

> 报告来源知识，未独立复现。报告的已求解结果与当前未求解工程分开记录；冲突参数不自动采用。

## 当前结论

报告提供了材料表、模型意图和作者结果，补充了原来缺少的资料，但还不能认定与当前工程是相同可复现实例。

| 项目 | 证据 | 决策 |
| --- | --- | --- |
| m/h0 | 报告m=0.303、h0=2640.75；工程恰好相反 | 已确认文档间对应不一致；待确认目标设置，原工程不动 |
| SFL比热 | 报告0.79 J/(g·K)，工程0.79 cal/(g·K) | 对照为790与3305.36 J/(kg·K)，不能当同值 |
| 焊料弹性温度轴 | 报告9点表与工程有3个中间温度配对不同 | E、ν各3项；保留两份来源，待确认 |
| 循环工况 | 高低温、平台持续时间、总时长吻合 | 可记录报告意图；作用域和初温仍需工程证据 |
| 载荷步/子步 | 报告每循环一步、10子步，热导出21步程序控制 | 不同系统/快照可能有差异，取得结构设置后判断 |
| 结果 | 报告有应力图，当前工程无求解结果 | 严格分开，不升级当前案例为已验证 |

## 原报告需纠正/澄清的标签

表2-3的Q/R写作1/K，与其物理量纲/ANSYS定义不符；m/h0的中文解释也不对应。按符号对照并保留原标签，不把报告文字错误写成自动化规则。

报告没有证明参数最初来自哪一条引用文献；文末六条文献只是检索线索，不能直接视为某个材料参数的原始出处。

## 后续动作

1. 与报告作者确认材料参数表和单位，确认工程准备采用哪一套。
2. 用户确认后另存工程和材料修订版，不能覆盖原始快照。
3. 补结构约束、参考温度、实际载荷步与网格证据。
4. 以后求解后，才按相同评价口径与报告结果比较。

相关证据：[公共报告材料](../../../shared/materials/bga-report-evidence.md)、[循环说明](../../thermal-cycling/bga-report-cycle.md)、[结果证据边界](../../verification/bga-report-result-evidence.md)。

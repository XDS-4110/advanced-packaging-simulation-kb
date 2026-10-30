---
id: KB-BGA-THERMAL-CYCLE-001
title: "BGA 温度循环：22 个载荷点与作用域限制"
document_type: knowledge
domain: simulation
status: draft
language: zh-CN
tags: [BGA, thermal-cycling, extracted, unsolved]
physics: [thermal, structural]
software: [ANSYS Workbench, ANSYS Mechanical]
software_versions: ["2024 R2"]
source_ids: [SRC-BGA-THERMAL-UI-001, SRC-BGA-001]
source_locator: "见本条目来源定位及 data/source-manifest.json"
updated_at: "2026-10-30"
reviewed_by: ""
reviewed_at: ""
---

> 最新热阶段证据：初温25 ℃、温度作用于tem（335面）、第14步结束12990 s，详见 [瞬态热界面与作用域](10-thermal-ui-scope.md)。本页早期快照保留历史；用户明确瞬态结构尚未开展，结构设置列为后续阶段待建立。


# BGA 温度循环：22 个载荷点与作用域限制

> 本文是已有工程的设置提取，未求解、未验证，不是推荐参数或通用建模规范。

## 载荷对象

- CAERep：`FullTemperature`，对象 ID 5948。
- `Scoping` 原始 ID 为 `5983`。对象名称索引还包含名为 `tem` 的命名选择，但目前不能可靠证明两者的面/节点对应关系。
- 初始温度记录为 **22 ℃**；载荷表的 t=0 温度为 **25 ℃**。二者分别保留，不替用户判定哪个正确。

## 原始温度—时间表

| 时间 s | 温度 ℃ |
| --- | --- |
| 0 | 25 |
| 30 | 150 |
| 1830 | 150 |
| 1890 | -55 |
| 3690 | -55 |
| 3750 | 150 |
| 5550 | 150 |
| 5610 | -55 |
| 7410 | -55 |
| 7470 | 150 |
| 9270 | 150 |
| 9330 | -55 |
| 11130 | -55 |
| 11190 | 150 |
| 12990 | 150 |
| 13050 | -55 |
| 14850 | -55 |
| 14910 | 150 |
| 16710 | 150 |
| 16770 | -55 |
| 18570 | -55 |
| 18600 | 25 |

可下载 [CSV](data/temperature-history.csv)。总历程 18600 s，即 310 min；温度范围 -55～150 ℃。

## 从表格直接计算的描述

- 0～30 s：25→150 ℃。
- 高温保温和低温保温各有 5 段，每段 1800 s。
- 高低温之间的转换均为 60 s。
- 表格包含 5 次高温平台和 5 次低温平台，最后 30 s 回到 25 ℃。循环次数应同时声明计数起点，不在缺少试验定义时只写一个无条件的“5 周期”。
- 以上是时间点差分得到的程序描述；实际载荷插值与作用对象仍需在 Mechanical 中核对。

## 来源定位

`CAERep.xml/EngineeringRep/BCRep/FullTemperature/Magnitude/Time` 与 `Values`；初温来自同一 BCRep 的 InitialConditionsRep。

## 限制

这是温度边界载荷表，不是芯片发热功率表，也不是已求解的芯片内部温度。未取得实际热循环试验标准、温箱条件或热电偶曲线。

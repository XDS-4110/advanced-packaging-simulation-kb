---
id: KB-BGA-SETTINGS-001
title: "BGA 分析设置与已有网格证据"
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


# BGA 分析设置与已有网格证据

> 本文是已有工程的设置提取，未求解、未验证，不是推荐参数或通用建模规范。

## 热分析设置

- CAERep 的 SolverRep 为 Thermal/Transient，目标求解器 ANSYS。
- 21 个热分析步，终止时间 18600 s；各步 AutoTimeSteppingType 为 ProgramControlled，TimeIntegration 为 true。
- 完整步末时间及相邻时差见 [分析步表](data/analysis-steps.csv)。程序控制不等于已取得明确的初始/最小/最大时间步。
- 第 14 步终点为 13049.2374379261 s，温度表低温平台结束点为 12990 s。两份数据分别保留，详见问题清单。

## 已有网格的可读取证据

- ds.dat 的 NBLOCK 解析到 **842248 条节点记录**；头部 `926472` 不直接当作实际节点数量。
- SOLID EBLOCK 头部声明数量合计 **437228**，这是当前已写出实体单元记录的计数，不包含全部接触单元，也不是已求解模型总单元数。
- 输入包含 `ET,*,279`、`ET,*,291` 的实体单元定义，以及 170/174 接触相关定义。
- 节点坐标包围范围约为 X=[-18.75502916,121.2449708]、Y=[-69.70320256,70.29679744]、Z=[-2.397,0.597] mm。由网格坐标得到约 140×140×2.994 mm 的整体范围，不等于单个芯片尺寸。
- HDF5 名称索引存在“六面体主导方法”“边尺寸调整”和多个“几何体尺寸调整”，但只提取到了名称，没有可靠解码它们的数值、作用域和抑制状态。

## ds.dat 完整性限制

本次扫描未检出 `/SOLU`、ANTYPE、TIME、D、IC 或 SOLVE 等完整分析控制/载荷段；文件末尾仍处于接触定义。不能把这份输入当作完整可直接运行的复现脚本。

没有求解日志与结果文件，因此没有网格独立性、收敛、温度、应力或翘曲结果。

## 来源定位

`CAERep.xml/SolverRep/AnalysisSettings/TransientThermalSettings`；`ds.dat` 节点块、实体单元块和命令统计；`SYS.mechdb/DS Objects Information`。详见 [解析证据](data/apdl-evidence.json)。

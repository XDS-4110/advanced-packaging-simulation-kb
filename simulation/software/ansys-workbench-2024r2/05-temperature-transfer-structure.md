---
id: KB-ANSYS242-OPS-05
title: "把热结果传递到结构分析并检查映射"
document_type: software_operation
domain: simulation
status: reviewed
language: zh-CN
tags: [ANSYS, thermal-structural, operation, temperature-transfer]
physics: [thermal, structural]
software: [ANSYS Workbench, ANSYS Mechanical]
software_versions: ["2024 R2"]
source_ids: [SRC-ANSYS-242-OPS-API, SRC-ANSYS-THERMOMECH-WORKFLOW, SRC-ANSYS-WB-OPS-EXAMPLE]
source_locator: "正文列出的v242类/方法与固定提交示例段落；版本和哈希见data/source-selection.json"
updated_at: "2026-11-02"
reviewed_by: "Codex（官方文档核对；未在本机执行仿真）"
reviewed_at: "2026-11-02"
verification_scope: "API条目存在性与操作组织核对；非运行或物理验证"
---

# 把热结果传递到结构分析并检查映射

## 前置条件

真实热结果及源分析身份、结构分析类型、需要传递的时刻、几何/网格对应、材料热膨胀定义、约束与无应力参考温度依据。热结果未产生时可配置连接，但不能验证实际场映射。

## 顺序耦合操作

1. Workbench工程层核对热Solution到结构Setup的连接及共享/不同模型关系；独立Mechanical会话则核对实际导入来源，不能假定连接已存在。
2. 结构端按研究目标选择Static Structural或Transient Structural；不能因为热端是瞬态就自动判定结构端必须采用某一种。选型理由不足时待人工确认。
3. 创建/核对Imported Body Temperature，指定源热分析或结果、目标实体及源时刻—结构分析时刻对应，再导入实际温度场。
4. 检查对象状态、目标覆盖和未映射区域；核对若干位置/时刻的源温度与导入温度。检查映射使用的几何、坐标、单位和时间定义，不只看对象名称。
5. 配置结构约束、参考温度和时间控制；温度循环边界、热初始25 ℃均不能自动替代结构无应力参考温度。

## 结构端最小设置清单

- 约束：记录实际安装状态、支撑位置和受限自由度；检查刚体运动及过约束，不把示例Fixed Support直接作为封装默认约束。
- 材料：检查热膨胀参考定义、温度依赖和焊料所用本构；Anand等率相关材料还需保留真实时间历程，不能任意缩短保温时间。
- 分析设置：记录载荷步、时间增量、大变形及适用的惯性/时间积分设置，并说明选用依据；不能把热分析时步未经检查直接复制到结构端。
- 结果目标：事先确定温度循环中的关注时刻、应力/应变指标和翘曲定义，避免只保存最终时刻而遗漏过程峰值。

## 官方API证据与边界

v242提供`Model.AddStaticStructuralAnalysis()`、`AddTransientStructuralAnalysis()`、`Analysis.ImportLoad`与ImportedBodyTemperature的`ImportLoad`、`GetTableByName`、`Location`。官方workflow通过`目标结构分析.ImportLoad(源热分析)`导入温度，并设置Source Time表；应通过实际返回/创建对象标识定位，不复制其英文对象名或Analyses[0]/[1]索引。

**来源限制：官方案例是瞬态热→非线性静力，不是本项目瞬态结构流程的运行验证。** 两种结构类型的参数配置和时间映射应分别实测；本次仅核对文档，不附可直接执行的耦合脚本。

## 完成证据

返回源分析/结果修订、结构类型、源/目标时刻表、目标实体、导入状态及覆盖检查。Imported对象存在或脚本返回成功不能替代温度映射验收。

## 精确来源

- [官方耦合示例](https://github.com/ansys/pyansys-workflows/blob/20647415eef62c71fdea3fc5a5e56abd5295dcf8/fluent-mechanical/wf_fm_02_mechanical.py)：Setup Structural Analysis、Imported Body Temperature、Source Time段。
- [v242 Analysis](https://scripting.mechanical.docs.pyansys.com/version/stable/api/ansys/mechanical/stubs/v242/Ansys/ACT/Automation/Mechanical/Analysis.html)：ImportLoad。
- [v242 ImportedBodyTemperature](https://scripting.mechanical.docs.pyansys.com/version/stable/api/ansys/mechanical/stubs/v242/Ansys/ACT/Automation/Mechanical/ImportedLoads/ImportedBodyTemperature.html)：ImportLoad、GetTableByName、Location。
- [Workbench与Mechanical联动](https://github.com/ansys/pyworkbench-examples/blob/406c4985e90b16a444fc8605e9f34c44812e6751/examples/pymechanical-integration/main.py)：会话归属与服务连接；该示例不是热结构案例。

PyMechanical执行模式、ImportLoad接口及历史版本问题见[专项补充](07-pymechanical-thermal-structural.md)，不把嵌入模式的临时配置当作远程连接的默认设置。

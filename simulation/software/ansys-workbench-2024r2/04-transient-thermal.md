---
id: KB-ANSYS242-OPS-04
title: "瞬态热分析的时间表与边界设置"
document_type: software_operation
domain: simulation
status: reviewed
language: zh-CN
tags: [ANSYS, thermal-structural, operation, transient-thermal]
physics: [thermal, structural]
software: [ANSYS Workbench, ANSYS Mechanical]
software_versions: ["2024 R2"]
source_ids: [SRC-ANSYS-242-OPS-API, SRC-ANSYS-THERMOMECH-WORKFLOW, SRC-ANSYS-MECH-OPS-EXAMPLES]
source_locator: "正文列出的v242类/方法与固定提交示例段落；版本和哈希见data/source-selection.json"
updated_at: "2026-11-02"
reviewed_by: "Codex（官方文档核对；未在本机执行仿真）"
reviewed_at: "2026-11-02"
verification_scope: "API条目存在性与操作组织核对；非运行或物理验证"
---

# 瞬态热分析的时间表与边界设置

## 先区分工况

温循：记录指定温度作用面和时间—温度表。工作发热：记录各热源及功率时间表、散热边界。两者可按实际工况组合，但不能把表面温度、环境温度和体发热率当作同一输入。

Temperature给定的是所选几何上的温度；若输入实际是温箱空气温度，需另行确定对流等换热建模方式，不能直接当作试样表面温度。总功率与单位体积发热率分别记录，转换时使用对应发热实体的体积。项目采用全部暴露外表面时，应检查焊球周围、封装底部间隙与板的暴露面，排除实体间内部接触面。

## 操作与核对

1. 建立/识别目标Transient Thermal，设置初始温度，区分初始温度、温度边界t=0值及后续结构参考温度。
2. 配置步数、各步结束时间、自动时步和初始/最小/最大时步；逐步回读，不把当前选中步的显示值推广到全部步骤。
3. 为Temperature等对象设置作用域和带单位的时间表；时间单调、输入输出点数对应，覆盖实际分析历程。温循条件引用项目选用标准及已核实条款，不从官方示例取值。
4. 检查边界是否被抑制、接触热传递和网格验收；若只做前处理，记录配置完成并保存，不能声称热求解完成。

## 可检索API线索

`Model.AddTransientThermalAnalysis()`、`Analysis.AddTemperature()`、`Temperature.Location`与`Magnitude`。`ANSYSAnalysisSettings.NumberOfSteps`及`SetStepEndTime`、`SetAutomaticTimeStepping`、`SetInitialTimeStep`、`SetMinimumTimeStep`、`SetMaximumTimeStep`、`SetTimeIntegration`可在v242参考核对；具体签名、枚举和值需读取当前版本，不能只按中文显示标签猜代码。

## 完成证据

返回初温、每步设置、完整载荷表及作用域、抑制状态、缺项。案例尺寸、22个点及5循环均非通用默认参数。

## 精确来源

- [v242 Model](https://scripting.mechanical.docs.pyansys.com/version/stable/api/ansys/mechanical/stubs/v242/Ansys/ACT/Automation/Mechanical/Model.html)：AddTransientThermalAnalysis。
- [v242 ANSYSAnalysisSettings](https://scripting.mechanical.docs.pyansys.com/version/stable/api/ansys/mechanical/stubs/v242/Ansys/ACT/Automation/Mechanical/AnalysisSettings/ANSYSAnalysisSettings.html)：步数和Set*时间控制。
- [v242 Temperature](https://scripting.mechanical.docs.pyansys.com/version/stable/api/ansys/mechanical/stubs/v242/Ansys/ACT/Automation/Mechanical/BoundaryConditions/Temperature.html)：Location、Magnitude。
- [官方耦合示例](https://github.com/ansys/pyansys-workflows/blob/20647415eef62c71fdea3fc5a5e56abd5295dcf8/fluent-mechanical/wf_fm_02_mechanical.py)：Setup transient thermal段；不采用其具体时程和边界值。

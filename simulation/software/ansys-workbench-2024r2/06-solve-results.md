---
id: KB-ANSYS242-OPS-06
title: "热结构求解状态与结果交付检查"
document_type: software_operation
domain: simulation
status: reviewed
language: zh-CN
tags: [ANSYS, thermal-structural, operation, solve-results]
physics: [thermal, structural]
software: [ANSYS Workbench, ANSYS Mechanical]
software_versions: ["2024 R2"]
source_ids: [SRC-ANSYS-THERMOMECH-WORKFLOW, SRC-ANSYS-MECH-OPS-EXAMPLES]
source_locator: "正文列出的v242类/方法与固定提交示例段落；版本和哈希见data/source-selection.json"
updated_at: "2026-11-02"
reviewed_by: "Codex（官方文档核对；未在本机执行仿真）"
reviewed_at: "2026-11-02"
verification_scope: "API条目存在性与操作组织核对；非运行或物理验证"
---

# 热结构求解状态与结果交付检查

## 前处理完成时

保存可恢复的工程修订、材料版本、作用域、接触、网格报告和分析时间设置。用户仅要求设置参数时，到此交付；不为完善知识库擅自运行求解。

## 获准求解后的顺序

1. 求解热分析，检查真实Solution状态和错误/警告日志，读取需要时刻的温度场。
2. 完成温度映射核对后再求解结构；分开记录两个分析的成功/失败，不把脚本成功等同于求解成功。
3. 核对材料、接触、约束、收敛以及适用的热平衡/反力检查；异常应报告，不擅自改变物理条件。
4. 结果必须包含对象、单位、时刻、作用域及提取方式。应力区分时程峰值和结束时刻；翘曲需约定目标面、方向、参考平面和刚体运动处理，不能直接把Total Deformation称为翘曲。
5. 保存工程/结果与简洁状态摘要，关联源模型修订。没有真实结果时返回未求解，不引用报告作者数值替代。

## API与边界

官方workflow演示`Solution.Solve(True)`、读取`Solution.Status`，以及AddTemperature、AddTotalDeformation、AddEquivalentStress、DisplayTime的使用。结果对象必须按实际分析类型和版本核实；调用不代表收敛或工程精度已验证。

导出截图只能证明画面内容，不能代替完整结果文件、数值和验收记录。本条目不附大型求解日志或机器专用路径。

## 精确来源

- [官方workflow](https://github.com/ansys/pyansys-workflows/blob/20647415eef62c71fdea3fc5a5e56abd5295dcf8/fluent-mechanical/wf_fm_02_mechanical.py)：Solve and post-process段（示例静力结构）。
- [官方基础结构示例](https://github.com/ansys/pymechanical-examples/blob/1069560138e7cebfffc97de5d102913530d9c43d/examples/00_basic/example_01_simple_structural_solve.py)：求解和结果流程，仅借鉴操作顺序。

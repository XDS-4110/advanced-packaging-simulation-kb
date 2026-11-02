---
id: KB-ANSYS242-OPS-01
title: "热结构模型的几何导入与材料赋值"
document_type: software_operation
domain: simulation
status: reviewed
language: zh-CN
tags: [ANSYS, thermal-structural, operation, geometry-materials]
physics: [thermal, structural]
software: [ANSYS Workbench, ANSYS Mechanical]
software_versions: ["2024 R2"]
source_ids: [SRC-ANSYS-242-OPS-API, SRC-ANSYS-THERMOMECH-WORKFLOW]
source_locator: "正文列出的v242类/方法与固定提交示例段落；版本和哈希见data/source-selection.json"
updated_at: "2026-11-02"
reviewed_by: "Codex（官方文档核对；未在本机执行仿真）"
reviewed_at: "2026-11-02"
verification_scope: "API条目存在性与操作组织核对；非运行或物理验证"
---

# 热结构模型的几何导入与材料赋值

## 前置输入

几何文件与修订、长度单位、预期实体清单、各实体材料ID和revision。Workbench系统连接与Mechanical内部操作分别记录；仅连接独立Mechanical不能证明已打开原WBPJ的同一系统。

## 操作与核对

1. 导入或刷新几何后核对实体数量、名称、尺度和关键位置；优先复用受控几何与稳定标识，不能直接复制示例的Children序号。
2. Engineering Data中确认已采用的材料版本；到Mechanical核对实际物性与实体赋值，保留回读值。仅名称相同不证明修正后的参数已同步。
3. 核对热物性、弹性、CTE定义和温度依赖；涉及焊料等非线性材料时再检查所选本构及其参数。材料参数继续引用[共享材料库](../../../shared/materials/README.md)，不在本条目重复抄表。

## 可检索API线索

`Model.GeometryImportGroup.AddGeometryImport()`用于创建几何导入对象；`Body.Material`为实体材料赋值属性，`Body.ReferenceTemperature`、`Body.ThermalStrainEffects`为后续结构相关字段。材料导入/刷新过程见官方workflow的Import geometry、Material段。

## 完成证据与限制

返回实际实体标识、单位、材料ID/revision和Mechanical回读值；未读到物性时标记同步待核实。示例中的钢材、文件路径和尺寸均不作为封装默认值。此处不收录几何创建引擎或SpaceClaim部署说明。

## 精确来源

- [v242 Body](https://scripting.mechanical.docs.pyansys.com/version/stable/api/ansys/mechanical/stubs/v242/Ansys/ACT/Automation/Mechanical/Body.html)：Material、ReferenceTemperature、ThermalStrainEffects。
- [官方耦合示例](https://github.com/ansys/pyansys-workflows/blob/20647415eef62c71fdea3fc5a5e56abd5295dcf8/fluent-mechanical/wf_fm_02_mechanical.py)：Import geometry、材料导入与赋值段。

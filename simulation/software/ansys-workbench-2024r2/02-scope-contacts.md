---
id: KB-ANSYS242-OPS-02
title: "命名选择与热结构接触的作用域检查"
document_type: software_operation
domain: simulation
status: reviewed
language: zh-CN
tags: [ANSYS, thermal-structural, operation, scope-contacts]
physics: [thermal, structural]
software: [ANSYS Workbench, ANSYS Mechanical]
software_versions: ["2024 R2"]
source_ids: [SRC-ANSYS-242-OPS-API]
source_locator: "正文列出的v242类/方法与固定提交示例段落；版本和哈希见data/source-selection.json"
updated_at: "2026-11-02"
reviewed_by: "Codex（官方文档核对；未在本机执行仿真）"
reviewed_at: "2026-11-02"
verification_scope: "API条目存在性与操作组织核对；非运行或物理验证"
---

# 命名选择与热结构接触的作用域检查

## 前置输入

每个载荷和接触的物理对象、预期面/体集合及界面假设；选面名称必须在当前模型中存在。

## 操作与核对

1. 建立命名选择，并检查实体类型、数量、面积或体积及高亮位置。结构修改后重新生成/核查集合，不继承BGA的335面或旧面ID。
2. 在温度、对流或结构载荷对象中重新关联目标选择，回读作用域及抑制状态。名字存在不等于载荷已经引用它。
3. 检查接触的源面、目标面、类型、间隙和抑制状态；单独核对热传递采用的热导设置及单位，不能仅凭Bonded判定热界面已正确配置。
4. 结构接触和热接触要求分别来自实际界面；知识不充分时保留待定项，不自动改成理想连接。

## 可检索API线索

`Model.AddNamedSelection()`创建命名选择；`Temperature.Location`保存温度对象作用域。`ContactRegion.SourceLocation`、`TargetLocation`、`ContactType`、`ThermalConductance`为v242可查字段；枚举和程序控制/手动模式需在当前对象读取确认。

## 完成证据

返回作用域清单或可重建规则、载荷绑定、接触源/目标及热设置；只给截图时不得声称已逐面审计。

## 精确来源

- [v242 Model](https://scripting.mechanical.docs.pyansys.com/version/stable/api/ansys/mechanical/stubs/v242/Ansys/ACT/Automation/Mechanical/Model.html)：AddNamedSelection。
- [v242 Temperature](https://scripting.mechanical.docs.pyansys.com/version/stable/api/ansys/mechanical/stubs/v242/Ansys/ACT/Automation/Mechanical/BoundaryConditions/Temperature.html)：Location。
- [v242 ContactRegion](https://scripting.mechanical.docs.pyansys.com/version/stable/api/ansys/mechanical/stubs/v242/Ansys/ACT/Automation/Mechanical/Connections/ContactRegion.html)：SourceLocation、TargetLocation、ContactType、ThermalConductance。

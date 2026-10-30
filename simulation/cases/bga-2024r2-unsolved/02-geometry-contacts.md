---
id: KB-BGA-GEOMETRY-001
title: "BGA 实体材料赋值与接触记录"
document_type: knowledge
domain: simulation
status: draft
language: zh-CN
tags: [BGA, thermal-cycling, extracted, unsolved]
physics: [thermal, structural]
software: [ANSYS Workbench, ANSYS Mechanical]
software_versions: ["2024 R2"]
source_ids: [SRC-BGA-ASSIGN-SCREEN-001, SRC-BGA-001]
source_locator: "见本条目来源定位及 data/source-manifest.json"
updated_at: "2026-10-30"
reviewed_by: ""
reviewed_at: ""
---

# BGA 实体材料赋值与接触记录

> 本文是已有工程的设置提取，未求解、未验证，不是推荐参数或通用建模规范。

## 实体与材料

CAERep 记录 320 个 Solid 实体，材料分布为：

| 材料名称 | 实体数量 | 名称线索（不代替人工确认） |
| --- | --- | --- |
| Sn63Pb37 | 315 | 155 个名称含 TUDIAN，160 个含 HANQIU；不能将全部 315 个实体直接等同于 BGA 球数量 |
| SI | 1 | XINPIAN，芯片 |
| Underfill | 1 | Underfill |
| BT | 2 | JIBAN 与 PCB |
| SFL | 1 | SUFENGLIAO，塑封料名称线索 |

完整原始名称、对象 ID、材料、质心、包围盒对角线和质量见 [实体表](data/bodies.csv)。名称有下划线/乱码，未擅自恢复中文。

## 接触

- CAERep 中存在 1650 个 ContactRep，导出 `Type` 全为 `Bonded`。
- 已提取源/目标 body ID、作用域 ID、算法字段、偏移与裁剪容差，见 [接触表](data/contacts.csv)。
- 不能从 Bonded 标签单独判定界面完全导热，也不能断言每个接触都有效或无重复。
- CAERep 的完整定义数量与未完成写出的 ds.dat 接触记录不能混为一个计数。

## 尚不能确认

每个焊料实体的功能、具体镀层/焊点分类、全部面与实体 ID 的可视对应、接触热导的最终取值、初始间隙及接触合理性。

## 来源定位

`CAERep.xml/EngineeringRep/GeometryAttributes/AssemblyAttributes/PartAttributes/BodyAttributes` 及 `EngineeringRep/BCRep/ContactRep`。

## 实体材料赋值界面资料已补充

此前七张Mechanical截图已整理为 [实体材料赋值记录](11-material-assignment-ui.md)：芯片SI、底部填充Underfill、凸点/焊球Sn63Pb37、基板/PCB均BT、塑封料SFL。可见名称与高亮已确认，完整实体ID及材料参数修订同步仍未核实。参考温度均显示“按环境”，不等于已取得结构参考温度数值。

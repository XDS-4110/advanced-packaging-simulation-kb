---
id: MAT-BGA-REV2-EVIDENCE-001
title: "BGA 材料修改后的工程输入证据"
document_type: material
domain: shared
status: draft
language: zh-CN
tags: [BGA, material-input, revision2, unsolved]
physics: [thermal, structural]
software: [ANSYS Workbench]
software_versions: ["2024 R2"]
source_ids: [SRC-BGA-REV3-001, SRC-BGA-REV2-001, SRC-BGA-001, SRC-BGA-REPORT-001]
source_locator: "EngineeringData.xml 材料/属性/参数名；journal2.wbjn；文件哈希见提取清单"
updated_at: "2026-10-30"
reviewed_by: ""
reviewed_at: ""
---

> 最新状态（revision 3）：SFL比热已保存为0.79 J/(g·K)，65条材料属性与报告对齐；Mechanical同步与重新归档未确认。见 [当前证据](bga-20261030-revision3.md)。


# BGA 材料修改后的工程输入证据

本记录是工程提取 revision 2，沿用原五种材料的身份关联，不代表材料已标定或认可。保留 [revision 1](bga-2024r2-import.md) 和 [报告证据](bga-report-evidence.md)，不覆盖历史快照。

## 核实结果

| 属性 | 原工程 | 本次保存的 Engineering Data | 与报告比较 |
| --- | --- | --- | --- |
| Sn63Pb37：Anand m | 2640.75 | 0.303 | 一致 |
| Sn63Pb37：Anand h0 | 0.303 | 2640.75，参考应力单位 MPa | 一致 |
| Sn63Pb37：E、ν 温度轴 ℃ | -55,-35,5,12,15,50,75,100,125 | -55,-35,-15,5,12,50,75,100,125 | 一致；E、ν数值序列未变 |
| SFL：比热 | 0.79 cal/(g·K) | 3.30536 J/(g·K) | 仍不同于报告的0.79 J/(g·K) |

journal2.wbjn 中的修改指令与 EngineeringData.xml 保存值一致。Anand 参考单位仍为 MPa、K、s^-1，其余七参数未改变。未发现其余材料属性变化。

## 比热差异仍未解决

更换显示单位时软件保留物理量：0.79 cal/(g·K) = 3.30536 J/(g·K) = 3305.36 J/(kg·K)。报告是0.79 J/(g·K) = 790 J/(kg·K)。因此本次只改变比热单位表示，没有改变物理量，报告—工程差异仍在。

应先确认目标来源。如果确定采用报告值，则应在 J/(g·K) 单位下输入0.79；这是一项物理数值修改。本次提取没有修改源工程。

## 数据与使用边界

- [当前 Engineering Data 材料属性快照](datasets/bga-20261030-revision2-draft/engineering-materials.json)：保留原字段、属性级参考单位及参数单位限定符，不能将 Anand 的通用 Unitless 导出标签直接视为全部参数无量纲。
- [报告逐项对照](datasets/bga-20261030-revision2-draft/report-vs-revision2.csv)：65条，64条与报告一致，1条比热数值不同。8条此前差异已对齐，不证明物理有效性。
- [来源与文件哈希](datasets/bga-20261030-revision2-draft/source-manifest.json)。

这里只核实 Engineering Data 保存值。未通过 Mechanical API 导出当前材料、约束、时间步；不确认修改已传入 Mechanical。现有WBPZ早于本轮编辑，内部材料XML与当前目录不同，不能代表本次修订。

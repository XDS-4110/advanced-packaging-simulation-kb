---
id: MAT-BGA-REV3-EVIDENCE-001
title: "BGA 第三次提取：比热修正后的材料输入"
document_type: material
domain: shared
status: draft
language: zh-CN
tags: [BGA, material-input, revision3, unsolved]
physics: [thermal, structural]
software: [ANSYS Workbench]
software_versions: ["2024 R2"]
source_ids: [SRC-BGA-REV3-001, SRC-BGA-001, SRC-BGA-REPORT-001]
source_locator: "EngineeringData.xml 材料/属性/参数名；journal2.wbjn；文件哈希见提取清单"
updated_at: "2026-10-30"
reviewed_by: ""
reviewed_at: ""
---

# BGA 第三次提取：比热修正后的材料输入

本记录为当前保存的Engineering Data提取revision 3，仍为draft。保留 [revision 2](bga-20261030-revision2.md) 和 [初次快照](bga-2024r2-import.md)；不是经过标定或求解验证的材料标准。

## 当前核实结果

| 项目 | 当前保存值 | 与报告比较 |
| --- | --- | --- |
| SFL比热 | 0.79 J/(g·K) = 790 J/(kg·K) | 一致，本轮已修改物理值 |
| Sn63Pb37 Anand m | 0.303 | 一致 |
| Sn63Pb37 Anand h0 | 2640.75，参考应力单位MPa | 一致 |
| Sn63Pb37 E、ν温度轴 ℃ | -55,-35,-15,5,12,50,75,100,125 | 一致 |

EngineeringData.xml与journal2.wbjn中的SetData及后续Save相互印证。相比revision 2，仅SFL的Specific Heat属性发生变化，其余材料属性相同。

[65条报告对照](datasets/bga-20261030-revision3-draft/report-vs-revision3.csv)已全部对齐。这只说明已提取材料值、单位及温度轴与报告一致，不证明报告来源、温度范围、本构适用性或实际仿真结果正确。

## 数据与剩余边界

- [当前材料属性快照](datasets/bga-20261030-revision3-draft/engineering-materials.json)：属性级参考单位与参数单位限定符一并保留。
- [文件哈希与提取范围](datasets/bga-20261030-revision3-draft/source-manifest.json)。
- 现有BGA.wbpz仍为14:36的旧归档，哈希与revision 2相同；本轮没有重新归档。
- Mechanical数据库与SYS.engd哈希也未变化，未通过Mechanical API导出新材料，不确认新值已传入Mechanical。
- 约束、无应力参考温度、结构时间步、接触、网格及温度映射的待补项不因此关闭。

后续核对Model/Mechanical中的材料后保存，再创建新的WBPZ。当前仍按未求解案例记录，报告应力结果不算当前工程的求解结果。本次提取没有修改源工程或运行求解器。

## 后续截图证据

[5张Engineering Data截图](bga-material-screenshots.md)进一步核实了可见字段。h0显示2640.8符合2640.75的显示精度；SFL弹性/CTE及焊料CTE表未在截图中展开，不覆盖原提取值。

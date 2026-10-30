---
id: KB-BGA-REVIEW-001
title: "BGA 原始设置中需要人工复核的项目"
document_type: knowledge
domain: simulation
status: draft
language: zh-CN
tags: [BGA, thermal-cycling, extracted, unsolved]
physics: [thermal, structural]
software: [ANSYS Workbench, ANSYS Mechanical]
software_versions: ["2024 R2"]
source_ids: [SRC-BGA-THERMAL-UI-001, SRC-BGA-REV3-001, SRC-BGA-REV2-001, SRC-BGA-001, SRC-ANSYS-242-ANAND, SRC-BGA-REPORT-001]
source_locator: "见本条目来源定位及 data/source-manifest.json"
updated_at: "2026-10-30"
reviewed_by: ""
reviewed_at: ""
---

> 最新热阶段证据：初温25 ℃、温度作用于tem（335面）、第14步结束12990 s，详见 [瞬态热界面与作用域](10-thermal-ui-scope.md)。本页早期快照保留历史；用户明确瞬态结构尚未开展，结构设置列为后续阶段待建立。


> 最新状态（revision 3）：SFL比热已保存为0.79 J/(g·K)，65条材料属性与报告对齐；Mechanical同步与重新归档未确认。见 [当前证据](../../../shared/materials/bga-20261030-revision3.md)。


> revision 2历史提示：本页原问题保留历史。m/h0与弹性温度轴在Engineering Data中已修改；未确认Mechanical同步，比热物理值未改，见 [第二次提取](09-revision2-material-review.md)。


# BGA 原始设置中需要人工复核的项目

> 本文是已有工程的设置提取，未求解、未验证，不是推荐参数或通用建模规范。

本清单记录证据差异和检查建议，不是已确认的软件报错；未修改任何原始输入。

| 编号 | 提取事实 | 建议核对 |
| --- | --- | --- |
| R1 | 初始温度 22 ℃，温度边界 t=0 为 25 ℃ | 是否有意设置初始不一致；区分初始温度和结构无应力参考温度 |
| R2 | 第 14 分析步末时刻 13049.2374379261 s；温度表拐点为 12990 s | 检查步末时间、表格插值与结果采样；不擅自改齐 |
| R3 | Sn63Pb37 的 CTE/弹性表最高温度 125 ℃，温度载荷最高 150 ℃ | 核对超温区的数据来源和软件处理；不能直接认定外推可靠 |
| R4 | SFL 的 CTE/弹性最低数据点为 25 ℃，温度载荷最低 -55 ℃ | 补充低温数据或说明合理依据 |
| R5 | Anand m=2640.75，h0=0.303；MatML 与 ds.dat 对应一致 | 对照原始标定表核对参数名称、顺序和单位；数值疑似错位，但尚不能确认，不能自动交换 |
| R6 | 焊料 CTE 与弹性表的中间温度点不同 | 对照原始数据确认，不能把两张表按行直接拼成相同温度 |
| R7 | 所有 MaterialRep 的 UseReferenceTemperature=false，同时保存有 ReferenceTemperature=22 ℃ | 保存字段不代表启用了部件参考温度；结构全局参考温度仍需从结构设置确认 |
| R8 | 1650 个 Bonded 接触，ds.dat 尚无完整求解控制段 | 核对接触作用域、重复/有效性及输入生成是否完成，不等同于设置或求解已验证 |

## Anand 参数顺序的核对依据

ANSYS 2024 R2 Theory Reference 第 4.3 节表 4.3 将第 5 项定义为无量纲 m，第 6 项定义为具有应力单位的 h0。此依据只能用于核对字段与单位，不能提供本材料的正确数值。

[官方说明（SRC-ANSYS-242-ANAND）](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ans_thry/thy_mat2.html)

## 来源定位

R1/R2：CAERep 的 InitialConditionsRep、StepEndTimes、FullTemperature/Magnitude；R3-R6：MatML 对应材料的 PropertyData 和 ParameterValue；R7：全部 MaterialRep；R8：ContactRep 及 ds.dat 扫描。

## 报告补充后的问题状态

R5 已从疑似变成明确的报告—工程对应不一致；R6 可定位到报告表2-2温度轴。另有塑封料比热 J/(g·K) 与 cal/(g·K) 的单位冲突。详见 [逐项对照](../../references/bga-thermal-reliability-report/report-project-comparison.md)。这不授权修改工程或自动判定报告全部正确。

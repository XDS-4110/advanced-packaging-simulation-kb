---
id: MAT-BGA-IMPORT-001
title: "BGA 工程材料参数：原值与适用范围"
document_type: material
domain: shared
status: draft
language: zh-CN
tags: [BGA, thermal-cycling, extracted, unsolved]
physics: [thermal, structural]
material_ids: [MAT-BGA-SI-001, MAT-BGA-UNDERFILL-001, MAT-BGA-SN63PB37-001, MAT-BGA-BT-001, MAT-BGA-SFL-001]
revision: "1"
record_kind: case_import_snapshot
software: [ANSYS Workbench, ANSYS Mechanical]
software_versions: ["2024 R2"]
source_ids: [SRC-BGA-001, SRC-BGA-REPORT-001]
source_locator: "见本条目来源定位及 simulation/cases/bga-2024r2-unsolved/data/source-manifest.json"
updated_at: "2026-10-30"
reviewed_by: ""
reviewed_at: ""
---

# BGA 工程材料参数：原值与适用范围

> 本文是已有工程的设置提取，未求解、未验证，不是推荐参数或通用建模规范。

## 基础热参数（原工程输入，不代表推荐值）

| 材料 | 密度 kg/m³ | 导热率 W/(m·K) | 比热 J/(kg·K) |
| --- | --- | --- | --- |
| SI | 2330 | 154 | 713 |
| Underfill | 1490 | 0.55 | 870 |
| Sn63Pb37 | 8400 | 50 | 128 |
| BT | 1700 | 0.2 | 920 |
| SFL | 1890 | 1 | 3305.36 |

温差单位 °C 与 K 在以上导热率、比热单位中数值等价。原始导出单位和限定条件保留于 [完整参数 CSV](datasets/bga-2024r2-draft/material-parameters.csv) 与 [材料 JSON](datasets/bga-2024r2-draft/materials.json)。

## 力学与温度相关属性

- SI、Underfill、BT 已提取弹性模量、泊松比及各向同性瞬时 CTE。
- Sn63Pb37 的 CTE、弹性模量和泊松比为温度相关表。CTE 温度轴为 `-55,-35,-15,5,12,50,75,100,125` ℃；弹性温度轴为 `-55,-35,5,12,15,50,75,100,125` ℃。两表温度轴不同，未强行合并或修改。
- SFL 的 CTE 温度点为 25、150 ℃，弹性温度点为 25、260 ℃。不能据此宣称已标定完整玻璃化转变或黏弹性模型。
- 单点常数属性导出中的约 `7.8886e-31` ℃ 保留为原始字段，不解释为材料只在该温度有效；Field Variable Compatible 也不代表已经输入一条温度曲线。
- 部分材料还有由 E、ν 派生的体积模量和剪切模量，CSV 保留这些导出值。

## Sn63Pb37 的 Anand 参数原值

属性限定声明的参考单位为 `MPa, K, s^-1`。各参数元数据有 Unitless 标记，不能据此把所有常数当作无量纲。

| 顺序 | 名称 | 原值 |
| --- | --- | --- |
| 1 | s0 | 56.63 |
| 2 | Q/R | 10830 |
| 3 | A | 14900000 |
| 4 | ξ | 11 |
| 5 | m | 2640.75 |
| 6 | h0 | 0.303 |
| 7 | 饱和变形阻力系数 | 80.415 |
| 8 | n | 0.0231 |
| 9 | a | 1.34 |

第 5、6 项疑似需重点核对其名称—数值对应和参数来源；不能仅凭常见文献值自动交换。原始 ds.dat 中也写为相同顺序，见 [命令证据](../../simulation/cases/bga-2024r2-unsolved/data/apdl-evidence.json)。

材料库包含结构钢，但本快照的 320 个实体没有将其作为赋值材料。

## 不能由文件恢复的依据

厂商牌号、测试方法、文献出处、参数标定及外推合理性尚未取得。材料定义存在，不代表其在结构求解中已被验证使用。

## 来源定位

`MatML.xml/Materials/MatML_Doc/Material/BulkDetails` 及同一 MatML_Doc 下 Metadata 的 ParameterDetails/PropertyDetails；`EngineeringData.xml` 交叉检查；CAERep 的 MaterialRep 确认实际赋值。

## 两份材料文件的单位核对

EngineeringData.xml 与 MatML.xml 的 10 项原始数值差异来自 GPa→Pa、J/(g·K)→J/(kg·K) 或 cal/(g·K)→J/(kg·K) 单位换算，逐项比较后数值一致，不能把它们误报为材料不一致。见 [单位核对表](datasets/bga-2024r2-draft/material-unit-crosscheck.csv)。本案例参数表采用 MatML 的导出单位。

## 公共记录与案例引用

本记录只描述 BGA 工程提取快照，状态仍为 draft；它不证明这些数值已经获得厂商或试验认可。封装与仿真双方共同审阅这一份参数，不创建各自的参数副本。上述材料 ID 只标识当前工程中的定义，不能代表所有同名牌号或不同工艺材料。源工程的历史输入原值不得被后续审核值覆盖；修订应保留 revision 和来源。

## 后续报告对照

新取得的 [报告材料证据](bga-report-evidence.md) 与本工程快照的 m/h0、SFL 比热单位及焊料弹性温度轴存在明确不一致。本记录原值与 revision 保持不变，不应自动选为正确参数。

---
id: KB-MATINPUT-004
title: "Sn63Pb37 的 Anand 字段与输入核对"
document_type: knowledge
domain: simulation
status: draft
language: zh-CN
tags: [material-input, Workbench-2024R2, thermal-stress, thermal-cycling]
physics: [thermal, structural]
software: [ANSYS Workbench, ANSYS Mechanical]
software_versions: ["2024 R2"]
source_ids: [SRC-BGA-REV3-001, SRC-BGA-REV2-001, SRC-BGA-001, SRC-ANSYS-242-ANAND, SRC-BGA-REPORT-001]
source_locator: "见文末官方资料与公共材料记录"
updated_at: "2026-10-30"
reviewed_by: ""
reviewed_at: ""
---

> 最新状态（revision 3）：SFL比热已保存为0.79 J/(g·K)，65条材料属性与报告对齐；Mechanical同步与重新归档未确认。见 [当前证据](../../shared/materials/bga-20261030-revision3.md)。


> revision 2历史提示：最新Engineering Data已保存m=0.303、h0=2640.75 MPa，与报告相符；原始标定与Mechanical同步仍未验证。见 [revision 2证据](../../shared/materials/bga-20261030-revision2.md)。


# Sn63Pb37 的 Anand 字段与输入核对

> 初版知识草稿：官方字段已核对，界面步骤尚未在本地工程逐项复现；未求解，未完成材料物理标定。

## 范围

核对已有 Anand 数据的输入，不提供一套可直接套用的焊料参数。相同合金名称不保证参数适用于不同温区、速率与工艺。

## 九个有名字段

| 顺序 | 参数 | 英文字段线索 | 参考单位 |
| --- | --- | --- | --- |
| 1 | s0 | Initial Deformation Resistance So | 应力，如 MPa |
| 2 | Q/R | Activation Energy Q/Universal Gas Constant R | K |
| 3 | A | Pre-exponential Factor A | s⁻¹ |
| 4 | ξ | Multiplier of Stress | 无量纲 |
| 5 | m | Strain Rate Sensitivity of Stress | 无量纲 |
| 6 | h0 | Hardening/Softening Constant | 应力，如 MPa |
| 7 | 饱和变形阻力系数 | Coefficient for Deformation Resistance Saturation | 应力，如 MPa |
| 8 | n | Strain Rate Sensitivity of Saturation | 无量纲 |
| 9 | a | Strain Rate Sensitivity of Hardening or Softening | 无量纲 |

按参数名称和定义匹配，不只依赖列位置或翻译。保存原定义 Reference Units；导出出现 Unitless 标记，不代表应力参数可当无量纲。

## BGA 当前阻塞项

原值统一见 [MAT-BGA-IMPORT-001 / revision 1](../../shared/materials/bga-2024r2-import.md)。m/h0 的数值对应需要原始出处核对。MatML 与 ds.dat 顺序一致，但一致不证明填写正确；**不猜测、不交换、不自动修正。**

还需确认：是 Q/R 还是 Q、应力/时间单位、绝对温度使用方式、合金及标定范围。当前九个数值不批准自动用于新工程。

## 不求解时的检查

1. 提供原始参数表，记录文献页码/表号和单位。
2. 在 Engineering Data 核对九个字段及 Reference Units，保存全表截图/导出。
3. 逐项与公共记录比较，不能以“通常值”替换出处。
4. 检查材料赋值与结构分析中的实际采用情况。
5. 保存真实时间历程；速率相关响应留待以后求解验证。

## 来源

[2024 R2 Theory Reference 4.3.2.4 / Table 4.3](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ans_thry/thy_mat2.html) 定义顺序和参数物理单位。Q/R 的 K 单位由量纲关系得到；SRC-BGA-001 给出实际字段及参考单位声明。

## 报告补充后的状态

报告表2-3已给出 m=0.303、h0=2640.75 MPa，与工程对应相反。现在可确认“报告—工程不一致”，但报告自身的Q/R单位和中文解释也需核对；原始标定依据仍待查。见 [对照记录](../references/bga-thermal-reliability-report/report-project-comparison.md)。

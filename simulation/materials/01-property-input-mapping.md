---
id: KB-MATINPUT-001
title: "材料属性到 Engineering Data 的输入映射"
document_type: knowledge
domain: simulation
status: draft
language: zh-CN
tags: [material-input, Workbench-2024R2, thermal-stress, thermal-cycling]
physics: [thermal, structural]
software: [ANSYS Workbench, ANSYS Mechanical]
software_versions: ["2024 R2"]
source_ids: [SRC-BGA-001, SRC-ANSYS-242-ENGDATA, SRC-ANSYS-242-THERMAL]
source_locator: "见文末官方资料与公共材料记录"
updated_at: "2026-10-30"
reviewed_by: ""
reviewed_at: ""
---

# 材料属性到 Engineering Data 的输入映射

> 初版知识草稿：官方字段已核对，界面步骤尚未在本地工程逐项复现；未求解，未完成材料物理标定。

## 公共记录

物理参数唯一来源是 [公共材料库](../../shared/materials/README.md)。当前采用 [MAT-BGA-IMPORT-001 / revision 1](../../shared/materials/bga-2024r2-import.md)，仍为 draft；下面是输入映射，不批准原值用于其他封装。

## 属性对应

| 物理属性 | Engineering Data 属性/字段 | 核对单位 | 注意事项 |
| --- | --- | --- | --- |
| 密度 | Density | kg/m³ | 与比热共同描述瞬态储热；结构惯性用途另按分析需要 |
| 导热率 | Isotropic Thermal Conductivity；有方向数据时选 Orthotropic Thermal Conductivity | W/(m·K) | 不因材料名称相同就猜测方向参数 |
| 定压比热 | Specific Heat，核对 Definition=Constant Pressure | J/(kg·K) | 不将体积热容直接填为质量比热 |
| E、ν | Isotropic Elasticity → Young's Modulus / Poisson's Ratio | Pa、无量纲 | 当前 BGA 为各向同性定义，不等于所有芯片都适用 |
| 各向异性刚度 | 相应 Orthotropic/Anisotropic Elasticity | 逐项核对 | 需完整相容数据及材料方向 |
| 热膨胀系数 | 对应 Instantaneous 或 Secant Coefficient of Thermal Expansion | 1/K | 保留原始定义，见第 3 篇 |
| 焊料速率相关行为 | Anand Viscoplasticity 九个有名字段 | 以参考单位声明为准 | 需有匹配的标定数据，见第 4 篇 |

## 设置流程（待本地界面复现）

1. 打开 Workbench 的 Engineering Data，创建有唯一身份的材料，记录材料 ID/revision。
2. 添加研究需要的属性，核对名称、Behavior、Definition 和单位。
3. 单值或温度表按原始数据输入；不同属性保留各自温度轴，不按行号强行合并。
4. 返回 Mechanical，将材料赋给正确实体，检查默认材料残留。
5. 保存属性表、材料赋值截图和版本，导出后按单位归一化比较。

当前 BGA 赋值关系见 [实体表](../cases/bga-2024r2-unsolved/data/bodies.csv)。[机器可读映射表](data/bga-input-mapping.csv) 只引用公共属性键，不复制另一份参数值。

## 来源

- [2024 R2 Engineering Data](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/wb2_js/ContainerName37.html)：MaterialProperty/MaterialPropertyData 的 Behavior 与 Definition。
- [2024 R2 Thermal Properties](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ans_mat/thermalmat.html)：方向导热率、坐标系与比热。
- SRC-BGA-001：MatML 的属性名称及限定字段。输入成功不代表物理适用性已经验证。

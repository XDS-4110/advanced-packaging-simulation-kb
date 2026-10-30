---
id: KB-MATINPUT-003
title: "单位、温度轴与热膨胀定义核对"
document_type: knowledge
domain: simulation
status: draft
language: zh-CN
tags: [material-input, Workbench-2024R2, thermal-stress, thermal-cycling]
physics: [thermal, structural]
software: [ANSYS Workbench, ANSYS Mechanical]
software_versions: ["2024 R2"]
source_ids: [SRC-BGA-001, SRC-ANSYS-242-ENGDATA, SRC-ANSYS-242-STRAIN]
source_locator: "见文末官方资料与公共材料记录"
updated_at: "2026-10-30"
reviewed_by: ""
reviewed_at: ""
---

# 单位、温度轴与热膨胀定义核对

> 初版知识草稿：官方字段已核对，界面步骤尚未在本地工程逐项复现；未求解，未完成材料物理标定。

## 单位

始终同时读取数值与字段单位，不能直接按界面默认单位粘贴数字。

| 换算 | 关系 |
| --- | --- |
| GPa → Pa | 乘 10⁹ |
| MPa → Pa | 乘 10⁶ |
| J/(g·K) → J/(kg·K) | 乘 1000 |
| 热化学 cal/(g·K) → J/(kg·K) | 乘 4184；先确认原资料 calorie 的定义 |
| 质量比热与体积热容 | 体积热容为 ρcp，不能直接填入 Specific Heat |

当前 BGA 两份材料文件的 10 项单位换算见 [公共核对表](../../shared/materials/datasets/bga-2024r2-draft/material-unit-crosscheck.csv)。这只证明输入表达相同，不证明物理数值正确。

## 温度轴

- 绝对温度满足 T(K)=T(℃)+273.15。温差的 K 与 ℃ 数值相同，绝对温度不同。
- E(T)、ν(T)、α(T) 各自保留温度轴；不要把不同表按行号直接拼接。
- 超出表格范围需说明来源和处理依据，不默认外推可靠。
- 当前载荷范围 -55～150 ℃，焊料 CTE/弹性表最高点 125 ℃，SFL 部分表最低点 25 ℃，均待补依据。

## 瞬时与割线 CTE

Engineering Data 区分 Instantaneous 和 Secant。小热应变条件下，用以下关系解释定义：

    ε_th(T) ≈ 从 T_ref 到 T 对 α_inst(θ) 积分
    α_sec(T; T_ref) = ε_th(T) / (T - T_ref)，仅用于 T ≠ T_ref

这不是任意材料数据转换的完整标定算法。温度相关系数不能只改标签、保留同表；T=Tref 不直接除零。采用软件支持的瞬时输入后，不再次人为积分。

## 三类温度分开记录

1. 热分析初始温度：开始时的状态。
2. 环境/边界温度：传热或温度载荷的条件。
3. 结构无应力参考温度：热应变基准，应有工艺/假设依据。

当前 BGA 的 22 ℃ 初温、t=0 的 25 ℃ 边界，以及保存但未启用的部件参考温度字段，不得互相替代。

## 来源

[2024 R2 Engineering Data](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/wb2_js/ContainerName37.html) 的 Definition；[2024 R2 Thermal Strain](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/wb_sim/ds_therm_strain.html) 的参考温度与热应变；SRC-BGA-001 的实际输入。单位关系与小应变说明为通用换算/推导。

---
id: "COMSOL-GUIDE-TIME-STEPPING"
title: "输出时刻、内部步长、容差与瞬态收敛"
document_type: "software-guide"
domain: "simulation"
status: "draft"
software_versions: ["COMSOL Multiphysics 6.4"]
source_ids: ["SRC-COMSOL-OFFICIAL-time-dependent-study", "SRC-COMSOL-OFFICIAL-time-dependent-solver", "SRC-COMSOL-OFFICIAL-transient-convergence"]
source_locator: "SRC-COMSOL-OFFICIAL-time-dependent-study: Time Dependent; Tolerance; SRC-COMSOL-OFFICIAL-time-dependent-solver: General; Time Stepping; SRC-COMSOL-OFFICIAL-transient-convergence: Mesh Refinement; Consistent Initialization; Scaling"
verification: "official_documentation_checked; not_run_locally"
updated_at: "2026-11-16"
tags: ["COMSOL", "Time Dependent", "输出时刻", "内部步长", "容差", "Strict", "时间范围", "瞬态收敛"]
language: "zh-CN"
software: ["COMSOL Multiphysics"]
reviewed_by: ""
reviewed_at: ""
---

# 输出时刻、内部步长、容差与瞬态收敛

适用条件：温循、功率循环及耦合瞬态研究的求解设置。

本文为官方资料的原创简要归纳及项目操作检查点；状态为草稿，须人工审核。

## 已核对的官方规则
Output times 定义仿真时段及输出安排，默认输出可能由求解器内部时间步插值得到。输出间隔不等同于内部积分步长。Strict 可要求求解步落到指定时刻，但求解器仍可插入其他步。相对容差控制局部误差；初始值与边界不一致可能导致很小的起始步。网格细化与时间容差细化都影响瞬态可信度。

## 项目操作检查点
1. 同时读取研究时段、输出列表、实际求解器设置及存储方式；后端有自定义覆盖时不能只展示研究节点值。
2. 时段应覆盖目标循环。升降温转折、脉冲与快速变化附近要有足够时间解析，并核查是否需要更小最大步长、Strict 或事件处理。
3. 缩小输出间隔只能改善观察密度，不能单独证明计算更准确；收紧容差后对关心量作对比。
4. 核对初始条件与起始载荷，保留不一致工况的物理说明；不以任意松容差掩盖设置问题。
5. 报告记录实际完成时间、失败/停止原因和有效结果范围；不得把部分时间解写为完整温循。材料参数不因求解困难而自动更改。

## 验证边界
步长与容差行为来源于 6.4 手册；收敛建议来自未限定版本的官方知识库。未在本地执行时步敏感性试验。

## 官方来源

- [Time Dependent](https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/comsol_ref_solver.36.017.html)；版本：6.4；定位：Time Dependent; Tolerance；访问日期：2026-11-16。
- [Time-Dependent Solver](https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/comsol_ref_solver.36.139.html)；版本：6.4；定位：General; Time Stepping；访问日期：2026-11-16。
- [Improving Convergence of Transient Models](https://www.comsol.com/support/knowledgebase/1262)；版本：Unversioned official knowledge-base page；定位：Mesh Refinement; Consistent Initialization; Scaling；访问日期：2026-11-16。


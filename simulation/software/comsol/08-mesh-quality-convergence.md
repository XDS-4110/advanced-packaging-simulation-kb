---
id: "COMSOL-GUIDE-MESH-QUALITY-CONVERGENCE"
title: "网格形状质量、统计口径与结果收敛"
document_type: "software-guide"
domain: "simulation"
status: "draft"
software_versions: ["COMSOL Multiphysics 6.4"]
source_ids: ["SRC-COMSOL-OFFICIAL-mesh-quality", "SRC-COMSOL-OFFICIAL-mesh-statistics", "SRC-COMSOL-OFFICIAL-mesh-api-quality", "SRC-COMSOL-OFFICIAL-mesh-refinement"]
source_locator: "SRC-COMSOL-OFFICIAL-mesh-quality: Mesh Element Quality; SRC-COMSOL-OFFICIAL-mesh-statistics: Statistics; Element Quality Histogram; SRC-COMSOL-OFFICIAL-mesh-api-quality: Quality of Elements; SRC-COMSOL-OFFICIAL-mesh-refinement: Comparing and Evaluating Results; General Remarks"
verification: "official_documentation_checked; not_run_locally"
updated_at: "2026-11-16"
tags: ["COMSOL", "网格质量", "均值", "最小质量", "skewness", "volcircum", "网格收敛", "单元数量", "误差"]
language: "zh-CN"
software: ["COMSOL Multiphysics"]
reviewed_by: ""
reviewed_at: ""
---

# 网格形状质量、统计口径与结果收敛

适用条件：网格助手达标判断、参数调整、求解精度与优化验收。

本文为官方资料的原创简要归纳及项目操作检查点；状态为草稿，须人工审核。

## 已核对的官方规则
网格形状质量评价单元形状，网格分辨率决定能否解析几何和场变化；两者不同。统计结果取决于质量度量、单元类型与所选区域。6.4 图形界面的网格统计默认度量与某些 API 文档列出的默认度量并不相同，必须显式指定。网格收敛需要在更细网格上重新求解并比较目标结果，局部尖角应力可能存在奇异性。

## 项目操作检查点
1. 保存度量名称、实体范围、单元类型、均值、最小值和数量；界面、日志、报告使用同一统计口径，禁止仅比较一个无名称的质量数。
2. 用户要求均值 ≥ 0.7 时，0.6946 仍未达标。不能因更细网格或预算允许而写成“达到 0.7”。
3. 每次调整后定位低质量区域，记录改动与实测变化；不要仅凭若干次试算宣称已达到该几何的理论上限。
4. 形状质量达标后仍应比较温度、位移、应力等关心量的网格敏感性；求解成功不等于结果已收敛。
5. 单元预算、质量阈值、结果误差容限分别记录，未获授权不得降低验收标准。网格调整不得改变已确认材料物性以促成“达标”。

## 验证边界
质量定义来源为 6.4 手册；网格收敛来源为官方通用知识库，不是特定版本实测。尚未运行本地网格或收敛试验。

## 官方来源

- [Mesh Element Quality](https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/comsol_ref_mesh.24.24.html)；版本：6.4；定位：Mesh Element Quality；访问日期：2026-11-16。
- [Mesh Statistics](https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/comsol_ref_mesh.24.25.html)；版本：6.4；定位：Statistics; Element Quality Histogram；访问日期：2026-11-16。
- [Quality of Elements](https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/comsol_api_mesh.49.028.html)；版本：6.4；定位：Quality of Elements；访问日期：2026-11-16。
- [Performing a Mesh Refinement Study](https://www.comsol.com/support/knowledgebase/1261)；版本：All versions (official knowledge base; not tied to 6.4)；定位：Comparing and Evaluating Results; General Remarks；访问日期：2026-11-16。


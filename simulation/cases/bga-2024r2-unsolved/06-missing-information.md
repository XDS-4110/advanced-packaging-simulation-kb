---
id: KB-BGA-MISSING-001
title: "BGA 无法可靠提取的信息与补充清单"
document_type: knowledge
domain: simulation
status: draft
language: zh-CN
tags: [BGA, thermal-cycling, extracted, unsolved]
physics: [thermal, structural]
software: [ANSYS Workbench, ANSYS Mechanical]
software_versions: ["2024 R2"]
source_ids: [SRC-BGA-001]
source_locator: "见本条目来源定位及 data/source-manifest.json"
updated_at: "2026-10-30"
reviewed_by: ""
reviewed_at: ""
---

# BGA 无法可靠提取的信息与补充清单

> 本文是已有工程的设置提取，未求解、未验证，不是推荐参数或通用建模规范。

## 可以确认但尚不完整

结构系统与 Imported Body Temperature 对象已存在；材料、网格控制和温度边界对象也存在。但仅有名称不等于已拿到其完整设置。

## 请优先补充

| 优先级 | 缺失内容 | 推荐提供方式 |
| --- | --- | --- |
| 高 | 温度对象 5948 的实际作用实体/面、与 tem 命名选择的对应 | 点选温度和 tem 后的几何高亮及 Details 截图，或 Mechanical API 导出作用域 ID |
| 高 | 结构支撑/位移约束、接触配置、真实无应力参考温度 | 结构分析树与各对象 Details；当前名称索引未识别到明确支撑对象，但不能据此断言工程完全没有约束 |
| 高 | 结构分析时间步、惯性/时间积分、非线性与蠕变设置 | 结构 Analysis Settings 的完整截图或 API 属性导出 |
| 高 | 导入温度的源分析、时刻对应、作用域与状态 | Imported Body Temperature 的 Details 与 Data View；求解前不能验证真实场映射 |
| 高 | 五种材料的原始出处、牌号与参数标定，尤其 Anand 的 m/h0 | 原始论文/数据表的定位或材料表截图 |
| 中 | 芯片、凸点和焊球的实际尺寸与分类 | 带尺寸的结构图、几何测量表、明确部件命名 |
| 中 | 网格大小、分段数、作用域、质量统计和抑制状态 | 网格树、各控制 Details、Statistics |
| 中 | 发热功率、对流、热流、辐射、界面热导 | 如果本案例本就只施加温度循环，请明确“不适用”；本热快照仅检出一个温度边界 |
| 中 | 目标翘曲面、参考平面、应力/应变/能量评价方法 | 用户说明或结果对象的设置记录 |
| 后续 | 温度/应力/翘曲结果、收敛、能量平衡、循环稳定性、寿命验证 | 以后实际求解与试验完成后补充；这不是当前提取失败 |

## 当前不能恢复的知识

为什么选择这些参数、是否满足某个试验标准、等效假设是否合理、是否能够预测疲劳寿命，都不能由工程输入数值自动证明。

## 来源定位

以本次 XML/APDL/名称索引覆盖范围与原始文件清单为依据。未对私有二进制参数做未经验证的逆向映射。

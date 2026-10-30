---
id: KB-MATINPUT-002
title: "发热翘曲与温度循环的材料模型选择"
document_type: knowledge
domain: simulation
status: draft
language: zh-CN
tags: [material-input, Workbench-2024R2, thermal-stress, thermal-cycling]
physics: [thermal, structural]
software: [ANSYS Workbench, ANSYS Mechanical]
software_versions: ["2024 R2"]
source_ids: [SRC-BGA-001, SRC-ANSYS-242-ENGDATA, SRC-ANSYS-242-ANAND]
source_locator: "见文末官方资料与公共材料记录"
updated_at: "2026-10-30"
reviewed_by: ""
reviewed_at: ""
---

# 发热翘曲与温度循环的材料模型选择

> 初版知识草稿：官方字段已核对，界面步骤尚未在本地工程逐项复现；未求解，未完成材料物理标定。

## 决策建议

先确定研究行为与结果，再选本构模型。下表是本项目建议，不是按材料名称自动指定模型的规则。

| 对象/目标 | 可考虑的起点 | 需要升级或补充的情况 |
| --- | --- | --- |
| 初步运行温度与整体翘曲 | 热属性 + 有依据的弹性/CTE | 温度依赖、方向性或非线性影响目标指标时，增加对应数据并做对照 |
| SI 芯片 | 当前 BGA 的各向同性弹性是假设 | 单晶方向相关应力需要晶向和相应刚度 |
| BT 基板/PCB | 当前输入为各向同性假设 | 实际层叠和面内/厚度方向差异需要叠层或经验证的等效数据 |
| Underfill、SFL | 有依据的温度相关弹性/CTE | 保温松弛、速率、固化或 Tg 附近行为重要时，需要具体牌号与试验/标定数据 |
| Sn63Pb37 | 流程检查可明确假设为弹性基线 | 研究累积非弹性、蠕变或耗散时，需要合适的速率相关模型及标定 |
| 等效区域 | 分别定义所需热学与力学等效属性 | 等效 k 不能证明等效刚度/CTE 或局部应力准确 |

## 两条分析路径

- 运行发热：区分最终稳定状态和开机历程，明确是否考虑制造残余应力、塑性及松弛。
- 温度循环：弹性基线不能代表焊料累积损伤。研究时间相关行为时保留升降温、保温的真实时间。
- 不自动叠加塑性、蠕变与 Anand；组合机制前核对相容性，避免重复描述同一非弹性行为。

当前 BGA 已有各向同性弹性、瞬时 CTE 和焊料 Anand 定义，但牌号来源、标定范围、聚合物黏弹性和结构求解中实际采用情况尚未确认。

## 应记录与验证

每次选择记录：选用原因、忽略行为、目标结果、适用温区/速率与限制。以后通过合适的材料试验、简化算例或模型敏感性检查；能运行不代表模型已标定。

## 来源

SRC-BGA-001 的 MatML；[Engineering Data 属性定义](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/wb2_js/ContainerName37.html)；[Anand 统一速率相关机制](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ans_thry/thy_mat2.html)。决策表为本项目整理建议。

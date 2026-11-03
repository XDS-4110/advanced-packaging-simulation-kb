---
id: KB-TS-ANSYS-0005
title: "如何判断材料和网格阶段确实完成"
document_type: case
domain: simulation
status: draft
tags: ["troubleshooting", "ansys", "workbench", "materials", "mesh", "evidence", "partial"]
physics: []
software: [ANSYS Workbench, ANSYS Mechanical]
software_versions: ["目标2024 R2；实际运行版本待核验"]
source_ids: [SRC-ANSYS-WB-LOCAL-20261103]
source_locator: "runtime/data/source-manifest.json；probe_log/probe2_log/probe3_log；execution-observations.json"
updated_at: "2026-11-03"
reviewed_by: ""
reviewed_at: ""
---

# 如何判断材料和网格阶段确实完成

## 软件环境与适用范围
用户本机Windows上的Workbench批处理/Mechanical前处理。记录时间为2026-11-03（Asia/Shanghai）。本次仅整理既有文件，未启动软件、修改工程或重新运行探针。

## 问题现象
本轮目标是三层模型的材料定义、分配和初始网格。实际归档日志只到模板创建、几何刷新和Model对象调用错误，不能据此声称材料及网格完成。

## 已有与缺失证据
| 阶段 | 本轮已有证据 | 缺失内容 |
| --- | --- | --- |
| Workbench脚本执行 | 三份探针日志 | 一致的启动命令与版本身份 |
| 几何 | geometry refreshed标记 | 实体数、单位、尺寸与位置回读 |
| 材料 | 用户表达希望使用Si/Cu | 材料精确名称/来源/必要物性、逐实体实际分配 |
| 网格 | 没有完成记录 | 实际生成状态、节点/单元数、质量与警告 |
| 保存 | 没有成功保存重开记录 | 工程依赖完整性和重开一致性 |

## 解决步骤与设置变化
后续候选流程：明确分析范围→核对会话与几何→核对材料来源→实际分配回读→生成网格→回收统计与警告→保存重开。每阶段保留成功/失败/未开始标记，不用进程退出码代替阶段验收。
Si/Cu只是用户期望的材料标签，不是材料数据库stable_id，也不是已审核参数。不得据此补常见物性值。初始网格不代表收敛证明；本轮不报告求解或工程可靠性。

## 结果验证
本条是证据缺口归纳，非成功仿真案例。U-RUNTIME、U-SAVE、U-RETRY仍未闭环；未授权或未设置的载荷、接触和物理场参数保持待确认。

## 复用限制与关联知识
这是draft排错资料，仅用于解释、人工排查和补证据，不作为工具参数来源或无人值守执行依据。不得将代理推测升级为已确认原因。
参见[几何与材料操作](../../../software/ansys-workbench-2024r2/01-geometry-materials.md)、[网格操作](../../../software/ansys-workbench-2024r2/03-mesh.md)和[未决项](../../../../shared/tools/unresolved.md)。未进行求解，收敛/时间步/物理平衡检验不适用。

## 来源与审核记录
来源：SRC-ANSYS-WB-LOCAL-20261103。整理：Codex；原始记录由用户提供。审核人及日期留空，待人类审核；不宣称本机运行问题已经解决。

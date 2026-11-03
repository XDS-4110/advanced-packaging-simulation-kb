---
id: KB-TS-ANSYS-0002
title: "几何导入失败：DataReference 没有 Import"
document_type: case
domain: simulation
status: draft
tags: ["troubleshooting", "ansys", "workbench", "geometry", "DataReference", "Import", "AttributeError"]
physics: []
software: [ANSYS Workbench, ANSYS Mechanical]
software_versions: ["目标2024 R2；实际运行版本待核验"]
source_ids: [SRC-ANSYS-WB-LOCAL-20261103]
source_locator: "runtime/data/source-manifest.json；probe_log/probe2_log/probe3_log；execution-observations.json"
updated_at: "2026-11-03"
reviewed_by: ""
reviewed_at: ""
---

# 几何导入失败：DataReference 没有 Import

## 软件环境与适用范围
用户本机Windows上的Workbench批处理/Mechanical前处理。记录时间为2026-11-03（Asia/Shanghai）。本次仅整理既有文件，未启动软件、修改工程或重新运行探针。

## 问题现象与报错原文
`probe_log.txt`：模板与系统已创建；`geo.Import(STEP)` 抛出 `AttributeError: 'DataReference' object has no attribute 'Import'`。

## 复现条件与文件清单
原脚本 `wb_probe.py` 使用 `GetComponent(Name="Geometry")` 获取对象，再调用 `Import`。原始脚本哈希在来源清单，脱敏日志位于 `data/probe_log.txt`。本次未重新执行。

## 原因排查
已确认本次返回对象是DataReference，且该对象没有调用中的Import成员。这是具体对象与成员不匹配的异常，不足以证明STEP损坏、许可证失效或几何导入功能不存在。
`probe2_log.txt`的成员列表没有Import。后续`probe3_log.txt`记录通过Geometry容器设置文件后已走到 `geometry refreshed`；该标记只说明脚本走过相应调用，不是实体数、单位或拓扑验收。

## 解决步骤与设置变化
排查候选：区分系统组件引用和Geometry容器；参照仓库几何操作条目核对容器的SetFile与组件Update/Refresh。不能自行猜Import方法，也不能把候选调用当作可直接执行的已审核参数。

## 结果验证
原异常有实际日志证据；替代路径仅有阶段标记，没有三实体回读、尺寸检查或保存重开证据。几何导入尚不能标记完成。

## 复用限制与关联知识
这是draft排错资料，仅用于解释、人工排查和补证据，不作为工具参数来源或无人值守执行依据。不得将代理推测升级为已确认原因。
参见[几何与材料操作](../../../software/ansys-workbench-2024r2/01-geometry-materials.md)、[网格操作](../../../software/ansys-workbench-2024r2/03-mesh.md)和[未决项](../../../../shared/tools/unresolved.md)。未进行求解，收敛/时间步/物理平衡检验不适用。

## 来源与审核记录
来源：SRC-ANSYS-WB-LOCAL-20261103。整理：Codex；原始记录由用户提供。审核人及日期留空，待人类审核；不宣称本机运行问题已经解决。

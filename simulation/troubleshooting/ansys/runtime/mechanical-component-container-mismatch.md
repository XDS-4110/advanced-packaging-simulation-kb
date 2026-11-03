---
id: KB-TS-ANSYS-0003
title: "Mechanical 调用失败：DataReference 没有 Edit 和 GetChildren"
document_type: case
domain: simulation
status: draft
tags: ["troubleshooting", "ansys", "workbench", "Mechanical", "DataReference", "Edit", "GetChildren", "SendCommand"]
physics: []
software: [ANSYS Workbench, ANSYS Mechanical]
software_versions: ["目标2024 R2；实际运行版本待核验"]
source_ids: [SRC-ANSYS-WB-LOCAL-20261103]
source_locator: "runtime/data/source-manifest.json；probe_log/probe2_log/probe3_log；execution-observations.json"
updated_at: "2026-11-03"
reviewed_by: ""
reviewed_at: ""
---

# Mechanical 调用失败：DataReference 没有 Edit 和 GetChildren

## 软件环境与适用范围
用户本机Windows上的Workbench批处理/Mechanical前处理。记录时间为2026-11-03（Asia/Shanghai）。本次仅整理既有文件，未启动软件、修改工程或重新运行探针。

## 问题现象与报错原文
- `probe2_log.txt`：`sys1.GetChildren()` 抛出 `AttributeError: 'DataReference' object has no attribute 'GetChildren'`。
- `probe3_log.txt`：`model dir has SendCommand: False`；随后 `model.Edit()` 抛出 `AttributeError: 'DataReference' object has no attribute 'Edit'`。

## 原因排查
原脚本用 `GetComponent(Name="Model")` 获取模型组件引用，然后尝试编辑与发送Mechanical命令。日志确认这些成员未在本次引用对象上提供。不能据此推断Workbench没有Mechanical接口，也不能把Mechanical内部ExtAPI与Workbench层对象混用。
GetChildren在系统引用上缺失，与在Mechanical数据模型树上遍历子对象是不同上下文；一次dir输出不构成全版本API契约。

## 解决步骤与设置变化
候选改进：先记录对象类型与执行上下文，区分Workbench系统、组件引用、容器和Mechanical内部模型。按仓库已核对文档确认Model容器接口，再以单个只读命令验证会话归属；不要每次枚举整个源码或API树。
`wb_probe4.py`试图打印容器成员，但归档时没有对应probe4日志，因此本条不宣称该探针已成功。

## 结果验证
两类AttributeError有日志证据；Mechanical会话打开、命令执行、材料分配及网格生成均未获得完成证据。候选修正仍需实机复测。

## 复用限制与关联知识
这是draft排错资料，仅用于解释、人工排查和补证据，不作为工具参数来源或无人值守执行依据。不得将代理推测升级为已确认原因。
参见[几何与材料操作](../../../software/ansys-workbench-2024r2/01-geometry-materials.md)、[网格操作](../../../software/ansys-workbench-2024r2/03-mesh.md)和[未决项](../../../../shared/tools/unresolved.md)。未进行求解，收敛/时间步/物理平衡检验不适用。

## 来源与审核记录
来源：SRC-ANSYS-WB-LOCAL-20261103。整理：Codex；原始记录由用户提供。审核人及日期留空，待人类审核；不宣称本机运行问题已经解决。

---
id: KB-TS-ANSYS-0001
title: "Workbench 批处理长时间无日志与反复启动"
document_type: case
domain: simulation
status: draft
tags: ["troubleshooting", "ansys", "workbench", "batch", "launch", "timeout", "journal"]
physics: []
software: [ANSYS Workbench, ANSYS Mechanical]
software_versions: ["目标2024 R2；实际运行版本待核验"]
source_ids: [SRC-ANSYS-WB-LOCAL-20261103]
source_locator: "runtime/data/source-manifest.json；probe_log/probe2_log/probe3_log；execution-observations.json"
updated_at: "2026-11-03"
reviewed_by: ""
reviewed_at: ""
---

# Workbench 批处理长时间无日志与反复启动

## 软件环境与适用范围
用户本机Windows上的Workbench批处理/Mechanical前处理。记录时间为2026-11-03（Asia/Shanghai）。本次仅整理既有文件，未启动软件、修改工程或重新运行探针。

## 问题现象与报错原文
代理执行摘要记录：探针未产生文件，多次切换调用方式；一次等待480秒后仍未取得进度文件。另一次重定向输出时报告 `The requested operation requires elevation`。

## 原因排查
- 权限令牌、启动方式、脚本未进入、启动器与子进程生命周期均为候选原因。
- “需要管理员权限”“执行环境限制”“journal扩展名错误”在摘要中互相替换，缺少足够的独立证据，不能确定根因。
- 现有探针先把信息放入内存列表，最后才一次写文件；因此中途没有日志不能证明尚未执行，也不能定位卡住阶段。
- 三份实际日志证明至少部分尝试已进入Workbench脚本，不能将整轮失败归因于“完全无法启动”。

## 解决步骤与设置变化
候选改进，尚未在本机复测：固定经过验证的启动入口；脚本进入时立即写标记，每个阶段刷新日志；分开记录启动耗时和计算耗时；保留启动器与实际工作进程的关联。启动失败与计算缓慢采用不同诊断。
不得把480秒观测值当作推荐超时，不得因等待超时而自动再次启动。取消代理任务后应核对软件任务状态，不盲目清理全部Ansys进程。

## 无效尝试与副作用
在尚未定位故障层时反复试直接调用、Start-Process、不同journal扩展名和帮助参数，产生额外等待及可能的GUI会话。摘要没有足够证据证明哪种启动命令在同一环境稳定有效；`cmd start`仅记为单次成功报告。

## 结果验证
本次未重跑启动。已有日志支持“脚本曾执行”，不支持启动故障已修复。完整成功命令、退出码、进程树、首个标记时间与版本身份仍待补充。

## 复用限制与关联知识
这是draft排错资料，仅用于解释、人工排查和补证据，不作为工具参数来源或无人值守执行依据。不得将代理推测升级为已确认原因。
参见[几何与材料操作](../../../software/ansys-workbench-2024r2/01-geometry-materials.md)、[网格操作](../../../software/ansys-workbench-2024r2/03-mesh.md)和[未决项](../../../../shared/tools/unresolved.md)。未进行求解，收敛/时间步/物理平衡检验不适用。

## 来源与审核记录
来源：SRC-ANSYS-WB-LOCAL-20261103。整理：Codex；原始记录由用户提供。审核人及日期留空，待人类审核；不宣称本机运行问题已经解决。

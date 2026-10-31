---
id: KB-ASSEMBLY-CHECK-001
title: "装配修改后的几何与连接检查参考"
document_type: knowledge
domain: simulation
status: reviewed
language: zh-CN
tags: [advanced-packaging, chiplet, structure-modeling, external-source]
physics: [thermal, structural]
software: []
software_versions: []
source_ids: [SRC-GH-IHP-ADK-001]
source_locator: "固定提交README：Status、What it checks、Checking pad-to-pillar alignment、Current scope"
updated_at: "2026-10-31"
reviewed_by: "Codex（原文与适用范围核对，未执行工具验证）"
reviewed_at: "2026-10-31"
---

# 装配修改后的几何与连接检查参考

## 原项目提供的检查

IHP Open ADK预览版区分装配间距/碰撞检查与互连间距检查，并提供焊盘—柱体对齐检查；规则依赖具体适配器及其输入。其thermal、power、timing目录仍是预留内容。[README原文](https://github.com/IHP-GmbH/IHP-Open-ADK/blob/859eff3111c0047cfd282ee7213c8bd8f5b33b76/README.md)

## 本项目借鉴的检查清单（归纳，非现成ANSYS功能）

结构修改后检查部件是否意外重叠、连接对象是否仍存在、上下互连位置是否匹配，以及连接层是否被遗漏或重复创建。具体间距阈值必须来自选用工艺资料，不能套用某个PDK默认值。

通过装配检查不能代替Mechanical热接触、结构约束或网格验收，也不能证明结构符合制造规范。Workbench自动检查接口尚未实现；本条目只说明可借鉴的检查思路。

与[插入中介层流程](insert-interposer-workflow.md)配套使用；网格仍执行[项目统一规则](../verification/project-mesh-requirements.md)。

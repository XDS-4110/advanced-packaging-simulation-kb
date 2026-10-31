---
id: KB-GH-PACKAGING-SELECTION-001
title: "GitHub封装结构资料筛选与使用范围"
document_type: knowledge
domain: simulation
status: reviewed
language: zh-CN
tags: [advanced-packaging, chiplet, structure-modeling, external-source]
physics: [thermal, structural]
software: []
software_versions: []
source_ids: [SRC-GH-IHP-CHIPLET-001, SRC-GH-IHP-ADK-001, SRC-GH-MFIT-001, SRC-GH-3DCHIPTECH-001]
source_locator: "2026-10-31逐项目README和指定文档核对；固定提交和文件哈希见data/github-packaging-sources.json"
updated_at: "2026-10-31"
reviewed_by: "Codex（原文与适用范围核对，未执行工具验证）"
reviewed_at: "2026-10-31"
---

# GitHub封装结构资料筛选与使用范围

本次筛选面向RAG资料补充，不安装上游工具、不复制代码或图书、不修改源ANSYS工程。所有链接固定到本次核对提交，后续版本变化需要重新检查。

| 项目 | 本次处理 | 知识入口 |
| --- | --- | --- |
| IHP chiplet-spec | 采用结构字段、坐标及连接表达思路；不当作热力材料库 | [装配描述](../../packaging/2-5d/structures/chiplet-assembly-description.md) |
| IHP Open ADK | 采用装配与互连检查思路；不假称已有热力仿真模块 | [装配检查](../modeling/assembly-consistency-checks.md) |
| MFIT | 采用几何/材料/功率分开组织方式；不抄默认物性和尺寸 | [热输入参考](../thermal/mfit-input-reference.md) |
| 3DChipTech | 保留背景阅读索引，不作为自动建模事实来源 | 下文说明 |

## 3DChipTech为何只保留线索

[2.5D介绍](https://github.com/chenweiphd/3DChipTech/blob/5c1d1d19b88f1408c248b4520142c29600bf9372/2.5DPackage.md)自述为改编整理，含未绑定年代的产业预测和优劣判断；本次仓库API未返回许可证，根目录LICENSE读取404。故不复制其正文/图片，不将其尺寸、厂商路线或性能断言直接纳入自动参数规则。需要具体结构时，应追溯原厂/论文原始来源。

## 来源与授权范围

IHP两项目核对到Apache-2.0，MFIT为GPL-3.0；本次仅提交自主归纳、固定链接、元数据及哈希，不搬运上游实现或原文。未来复制代码需另行遵守对应许可。

[快照与筛选清单](data/github-packaging-sources.json)记录核对文件和许可证证据。reviewed仅覆盖文档转录及适用范围核对，不表示上游工具已安装、ANSYS适配器已实现或物理结果已复现。

本库新增的[中介层修改流程](../modeling/insert-interposer-workflow.md)为draft，不应因引用reviewed来源而自动升级。RAG生产检索只收录reviewed/validated，草稿用于方案讨论和补参。

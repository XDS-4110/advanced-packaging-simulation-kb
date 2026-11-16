---
id: KB-PROJECT-MESH-001
title: "当前项目网格要求的记录与核验"
document_type: knowledge
domain: simulation
status: draft
language: zh-CN
software: []
software_versions: []
source_ids: [SRC-PROJECT-MESH-DOC-001, SRC-PROJECT-MESH-CONFIRM-001, SRC-KB-COMSOL-MIGRATION-20261116]
source_locator: "本库方法整理；具体软件规则另见 COMSOL 官方资料草稿，未经本机算例验证"
updated_at: "2026-11-16"
reviewed_by: ""
reviewed_at: ""
---

# 当前项目网格要求的记录与核验

## 先确定度量和适用范围

网格质量数字只有在度量定义相同、单元类型相容、统计范围一致时才可比较。当前项目必须明确质量度量名称、最小值/平均值的阈值、按域或全模型统计、单元数量目标和硬上限。不得由知识库补上默认阈值。

历史项目中的质量指标、层数和数量要求不直接迁移到 COMSOL；原确认来源仅保留审计用途。本条为迁移后的方法草稿，尚无本机运行验证。

## 逐轮核验

记录几何修订、网格方法、各域控制、单元数、质量统计和低质量位置。区分“单元数量目标”和“硬上限”，不能因其中一项满足就宣布全部达标。遇到平台期，应报告已试方案和结果，并检查局部几何/分区及可用方法；不得隐瞒未达标或自动降低阈值。

网格质量验收后仍需做目标量的网格收敛检查，必要时也做时间步/求解容差敏感性。应力尖点等奇异位置的无限加密不构成结果收敛证据。

COMSOL 官方度量与收敛资料见 [网格质量与收敛](../software/comsol/08-mesh-quality-convergence.md)。

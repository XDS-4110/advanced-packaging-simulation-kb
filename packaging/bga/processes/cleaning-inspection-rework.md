---
id: KB-BGA-FOUNDATION-20261102-008
title: "BGA清洗、检测与返修的条件限制"
document_type: knowledge
domain: packaging
status: draft
language: zh-CN
tags: [BGA, processes]
physics: [thermal, mechanical]
software: []
software_versions: []
source_ids: [SRC-BGA-MANUFACTURING-1995]
source_locator: "p.436 Cleaning、Inspection、Rework；p.437"
updated_at: "2026-11-02"
reviewed_by: ""
reviewed_at: ""
---

# BGA清洗、检测与返修的条件限制

## 回答的问题与知识正文

焊点位于器件底部，使清洗液进入和内部焊点观察受到几何限制。原文的清洗试验采用RMA焊膏、半水清洗和较简单的四器件测试板，作者也提出需要在更复杂板上进一步研究。因此不能将结果写成“BGA都容易清洗”。

论文讨论X射线层析检测错位的可能性，但并未证明该方法能无条件判断全部焊点质量。检测记录应包含方法、能检出的缺陷类型与判据。

返修对器件本体及邻近元件产生额外热历程。原文强调本体温度、邻近焊点温度及重新定位的重要性。是否允许返修和具体温度限制，仍需器件与工艺规范。

## 适用对象、假设与限制

本条不是清洗、X射线检测或返修验收规范；历史研究不提供本项目的缺陷容许阈值。

## 资料整理与交接（项目建议）

收集焊膏与清洗体系、器件间隙、布局密度、检测方法、返修次数和温度记录。

## 验证与常见错误

“看到图像”不等于“缺陷判定已验证”；返修后样品不应未经说明与未返修样品合并解释可靠性数据。

## 来源与证据

来源ID：SRC-BGA-MANUFACTURING-1995。定位：p.436 Cleaning、Inspection、Rework；p.437。

制造综述书目与阅读说明见 [文献笔记](../references/manufacturing-bga-1995.md)。本条为有来源的待审核正文，不代表已经验证的工艺方案或仿真输入。具体参数仍需逐项核对，不以draft内容直接生成工程设置。

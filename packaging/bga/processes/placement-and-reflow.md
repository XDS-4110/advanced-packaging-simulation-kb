---
id: KB-BGA-FOUNDATION-20261102-007
title: "BGA贴装定位与回流自对中"
document_type: knowledge
domain: packaging
status: draft
language: zh-CN
tags: [BGA, processes]
physics: [thermal, mechanical]
software: []
software_versions: []
source_ids: [SRC-BGA-MANUFACTURING-1995]
source_locator: "p.435 Component Placement、Reflow，图3–4"
updated_at: "2026-11-02"
reviewed_by: ""
reviewed_at: ""
---

# BGA贴装定位与回流自对中

## 回答的问题与知识正文

原文通过回流前后的图示展示了特定BGA器件的自对中现象，同时指出仅以器件外形边缘定位存在误差。能自对中不意味着可以省略精确贴装，更不意味着任意偏移都能被回流纠正。

回流时焊点位于器件底部，器件尺寸、板上布局和热容量会影响加热过程。工艺需要同时考虑焊膏要求和器件允许的温度历程。炉区设定值不能直接代表隐藏焊点实际经历的温度。

对本项目而言，这些内容用于解释装配历史和实际几何来源，不提供炉温设定值或允许偏移量。

## 适用对象、假设与限制

原文偏移量是历史实例，不是当前器件的贴装允差；原文设备描述不能直接代表当前设备能力。

## 资料整理与交接（项目建议）

记录对准基准、回流前后位置、器件与焊点测温位置，以及实测时间温度曲线。

## 验证与常见错误

区分预回流球形与回流后连接形状；不能把自对中示例当作无需定位检查的依据。

## 来源与证据

来源ID：SRC-BGA-MANUFACTURING-1995。定位：p.435 Component Placement、Reflow，图3–4。

制造综述书目与阅读说明见 [文献笔记](../references/manufacturing-bga-1995.md)。本条为有来源的待审核正文，不代表已经验证的工艺方案或仿真输入。具体参数仍需逐项核对，不以draft内容直接生成工程设置。

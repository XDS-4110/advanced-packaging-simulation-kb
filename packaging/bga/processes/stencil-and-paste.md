---
id: KB-BGA-FOUNDATION-20261102-006
title: "焊膏印刷与钢网开口的基本关系"
document_type: knowledge
domain: packaging
status: draft
language: zh-CN
tags: [BGA, processes]
physics: [thermal, mechanical]
software: []
software_versions: []
source_ids: [SRC-BGA-MANUFACTURING-1995]
source_locator: "p.434 Solder Paste Application；p.435 Table I"
updated_at: "2026-11-02"
reviewed_by: ""
reviewed_at: ""
---

# 焊膏印刷与钢网开口的基本关系

## 回答的问题与知识正文

论文指出，钢网厚度、开口形状和尺寸影响焊膏印刷与释放。BGA圆形开口与细间距器件矩形开口的比较属于特定工艺实验，不能只比较节距就判断印刷难度。

特别注意：原文将area ratio定义为“开口壁面积÷开口面积”。其表格和阈值必须连同定义一起引用，不可只抄一个无定义比值。

为解释定义，若将开口理想化为直径d、厚度t的圆柱孔，壁面积为πdt，开口面积为πd²/4，则原文定义的比值为4t/d。此式是按几何定义自行推导，d与t必须使用相同单位；不考虑孔壁锥度、粗糙度和实际释放过程。

## 适用对象、假设与限制

不从1995年的钢网厚度和阈值生成现代BGA推荐参数；本文不引用任何现行标准阈值。

## 资料整理与交接（项目建议）

记录钢网厚度、开口尺寸、孔壁状态、焊膏类型、印刷条件和实际检测数据，并保留area ratio的分子分母。

## 验证与常见错误

检查面积比是否用反。几何开口体积不等于实际转移焊膏体积，更不等于最终金属焊点体积。

## 来源与证据

来源ID：SRC-BGA-MANUFACTURING-1995。定位：p.434 Solder Paste Application；p.435 Table I。

制造综述书目与阅读说明见 [文献笔记](../references/manufacturing-bga-1995.md)。本条为有来源的待审核正文，不代表已经验证的工艺方案或仿真输入。具体参数仍需逐项核对，不以draft内容直接生成工程设置。

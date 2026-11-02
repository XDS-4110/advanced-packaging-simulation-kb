---
id: KB-BGA-FOUNDATION-20261102-001
title: "BGA的定义与内部互连的区别"
document_type: knowledge
domain: packaging
status: draft
language: zh-CN
tags: [BGA, fundamentals]
physics: [thermal, mechanical]
software: []
software_versions: []
source_ids: [SRC-BGA-MANUFACTURING-1995, SRC-LIT-SIP-2023]
source_locator: "Mearig与Goers，p.434–435；SiP综述第1节和第2.1节"
updated_at: "2026-11-02"
reviewed_by: ""
reviewed_at: ""
---

# BGA的定义与内部互连的区别

## 回答的问题与知识正文

BGA（Ball Grid Array，球栅阵列）以封装底部的阵列焊球实现外部连接。名称首先说明外部连接形式，并不能单独确定芯片在封装内部采用线焊还是倒装互连。

读到“BGA”时应继续核实三个层面：芯片到封装基板怎样连接、封装内部由哪些部件组成、封装是否已经焊接到PCB。SiP描述封装内的系统集成，不能与BGA当作互斥分类。

例如，当前报告包含芯片下凸点和基板下焊球；两者的连接对象不同。仅从封装底部球阵列照片不能推断出内部凸点排列。

## 适用对象、假设与限制

本条描述术语与识别方法，不建立覆盖全部厂商命名的分类标准。1995年论文中的设备能力和尺寸属于当时背景。

## 资料整理与交接（项目建议）

登记外部互连形式、内部互连形式、封装材料与研究层级；没有剖面或手册证据的字段标待确认。

## 验证与常见错误

常见错误是把所有BGA都画成倒装芯片结构，或者把SiP、BGA和2.5D列成同一分类轴。核对手册和剖面后再建立组件表。

## 来源与证据

来源ID：SRC-BGA-MANUFACTURING-1995, SRC-LIT-SIP-2023。定位：Mearig与Goers，p.434–435；SiP综述第1节和第2.1节。

制造综述书目与阅读说明见 [文献笔记](../references/manufacturing-bga-1995.md)。本条为有来源的待审核正文，不代表已经验证的工艺方案或仿真输入。具体参数仍需逐项核对，不以draft内容直接生成工程设置。

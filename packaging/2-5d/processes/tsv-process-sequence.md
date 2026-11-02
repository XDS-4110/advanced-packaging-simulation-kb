---
id: KB-COURSE-PACKAGING-20261102-008
title: "TSV工艺时序与结构状态"
document_type: knowledge
domain: packaging
status: draft
language: zh-CN
tags: [TSV, process, integration]
physics: [thermal, mechanical]
software: []
software_versions: []
source_ids: [SRC-COURSE-CHIP-PACKAGING-15]
source_locator: "课件15 p.4–6（PDF文件页码）"
updated_at: "2026-11-02"
reviewed_by: ""
reviewed_at: ""
---

# TSV工艺时序与结构状态

## Via-first、via-middle和via-last描述什么

课件按TSV形成与器件加工的先后关系区分三类路线：via-first位于所示CMOS器件加工之前；via-middle位于器件形成之后、后端互连之前；via-last位于器件和后端互连之后。这是对课件流程的归纳，具体论文或厂商仍需核实其术语边界与正面/背面加工路线。

这种命名依赖有源器件与后端互连的工艺参照。无源硅中介层未必包含相同的CMOS步骤，不能仅凭存在TSV就强行套用同一工艺序列。应优先记录真实的刻蚀、绝缘、金属形成、减薄、露铜、布线和装配次序。

## 为什么封装知识库要保存工艺顺序

同样的最终几何可能经历不同温度、临时支撑和材料形成过程。材料在何时加入、胶何时固化、支撑何时去除，会影响所讨论结构的初始状态。因此“室温几何”不能单独证明结构在室温无应力；回流峰值也不能自动指定为所有部件共同的无应力温度。

## 工艺事实交接表

逐步记录操作名称、作用面、已存在部件、新增/去除材料、温度—时间历史、支撑状态和证据页码。缺少某一步时保留空缺，不用通用流程假装是目标产品的制造记录。

课件p.5列有示例零应变温度范围，但未给出足以迁移到本项目的材料形成和应力释放证据。本条只说明需收集的工艺事实；应力初始化和工艺仿真实现由simulation维护。

## 来源与审核边界

本条为课程课件的归纳及明确标注的基础推导/项目交接建议，尚待审核；未通过本案例求解验证。阅读范围与原文疑点见[课程阅读笔记](../../common/references/course-41-reading-notes.md)。

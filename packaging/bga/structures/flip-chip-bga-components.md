---
id: KB-BGA-FOUNDATION-20261102-003
title: "当前塑封倒装BGA的部件与连接关系"
document_type: knowledge
domain: packaging
status: draft
language: zh-CN
tags: [BGA, structures]
physics: [thermal, mechanical]
software: []
software_versions: []
source_ids: [SRC-BGA-REPORT-001]
source_locator: "报告第2.2节、图2-3和表2-1"
updated_at: "2026-11-02"
reviewed_by: ""
reviewed_at: ""
---

# 当前塑封倒装BGA的部件与连接关系

## 回答的问题与知识正文

报告的爆炸图和文字支持以下六类部件。这是本案例的结构描述，不是所有BGA必须具备的清单。

| 部件 | 位置及作用 | 需要补充的证据 |
| --- | --- | --- |
| 芯片 | 通过下方凸点连接基板 | 尺寸、朝向和位置 |
| 凸点 | 芯片与BT基板之间的互连 | 数量、排列、回流后形状 |
| Underfill | 填充芯片下方间隙并包围凸点 | 厚度、边缘形状、覆盖范围 |
| BT基板 | 支持内部互连并连接外部球阵列 | 厚度、层叠、实际导体结构 |
| 底部焊球 | 位于基板下方 | 球阵列、焊盘、装配状态 |
| 塑封料 | 包覆和保护器件内部结构 | 实际包覆形状和芯片位置 |

整理CAD时应记录相邻部件之间是真实接触、材料连续还是存在间隙。爆炸图中的视觉分离用于展示部件，不应直接作为实际装配间隙。

## 适用对象、假设与限制

报告没有给出完整尺寸，不按图像比例生成数值；BT名称也不能替代具体基板叠层与材料定义。

## 资料整理与交接（项目建议）

制作组件ID表和上下端连接表，逐项对应CAD实体；材料引用公共库ID与revision。

## 验证与常见错误

检查填充胶是否与凸点体积重叠，芯片和基板是否因重复厚度产生错位。这里是实物资料核查，接触算法由simulation选择。

## 来源与证据

来源ID：SRC-BGA-REPORT-001。定位：报告第2.2节、图2-3和表2-1。

制造综述书目与阅读说明见 [文献笔记](../references/manufacturing-bga-1995.md)。本条为有来源的待审核正文，不代表已经验证的工艺方案或仿真输入。具体参数仍需逐项核对，不以draft内容直接生成工程设置。

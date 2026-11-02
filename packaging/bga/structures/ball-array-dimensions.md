---
id: KB-BGA-FOUNDATION-20261102-004
title: "BGA球阵列与装配尺寸应怎样记录"
document_type: knowledge
domain: packaging
status: draft
language: zh-CN
tags: [BGA, structures]
physics: [thermal, mechanical]
software: []
software_versions: []
source_ids: [SRC-BGA-MANUFACTURING-1995, SRC-BGA-REPORT-001]
source_locator: "Mearig与Goers p.435 Component Placement、p.436 Cleaning；报告图2-3"
updated_at: "2026-11-02"
reviewed_by: ""
reviewed_at: ""
---

# BGA球阵列与装配尺寸应怎样记录

## 回答的问题与知识正文

球阵列不能仅用“球数和直径”描述。为了重建实际布局，还需知道行列坐标、中心间距、缺球位置、边缘偏置和器件方向。

| 字段 | 本项目记录定义 |
| --- | --- |
| 节距 | 指定方向上相邻球中心的距离，分别记录X/Y |
| 球径 | 注明测量的是植球前球体、植球后外形还是装配后焊点 |
| 焊点高度 | 说明上下测量基准面和装配状态 |
| 焊盘尺寸 | 器件端与PCB端分别记录，不能由球径代替 |
| 阵列坐标 | 明确原点、行列方向、缺球和旋转方向 |

制造综述指出器件外形与球阵列位置并不一定完全重合，因此仅按器件边框居中可能造成贴装偏差。这说明几何输入需要球阵列本身的定位证据。

## 适用对象、假设与限制

表内是项目数据字段约定，不是引用标准的公差定义。原文早期器件间隙不能作为当前器件尺寸。

## 资料整理与交接（项目建议）

优先使用封装尺寸图、CAD与测量记录；保存单位、装配前后状态和数据来源。mm与μm不要混列为无单位数值。

## 验证与常见错误

对照实际球数、包围范围和缺球位置。回流后焊点不是默认完整球体，等效形状应另作仿真假设。

## 来源与证据

来源ID：SRC-BGA-MANUFACTURING-1995, SRC-BGA-REPORT-001。定位：Mearig与Goers p.435 Component Placement、p.436 Cleaning；报告图2-3。

制造综述书目与阅读说明见 [文献笔记](../references/manufacturing-bga-1995.md)。本条为有来源的待审核正文，不代表已经验证的工艺方案或仿真输入。具体参数仍需逐项核对，不以draft内容直接生成工程设置。

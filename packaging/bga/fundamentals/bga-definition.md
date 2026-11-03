---
id: KB-BGA-FOUNDATION-20261102-001
title: "BGA定义、分类维度与互连层级"
document_type: knowledge
domain: packaging
status: draft
language: zh-CN
tags: [BGA, fundamentals, modeling, drawing-constraints]
physics: [thermal, mechanical]
software: [COMSOL, ANSYS]
software_versions: []
updated_at: "2026-11-03"
reviewed_by: ""
reviewed_at: ""
---

# BGA定义、分类维度与互连层级

## BGA名称能确定什么

BGA（Ball Grid Array）指封装外部通过底面球栅阵列连接。这个名称不能确定芯片内部采用线焊、倒装还是多芯片互连，也不能确定器件是否已经装到 PCB 上。球数、节距、球径和材料必须按具体器件确认。

| 分类维度 | 常见描述 | 能确定和不能确定的内容 |
| --- | --- | --- |
| 外部端子 | BGA、LGA、PGA | 分别强调焊球、平面焊盘和针状端子，不确定内部芯片连接 |
| 基板或封装体系 | 塑封/有机基板 BGA、陶瓷 BGA | 提供材料体系线索，不能替代完整叠层和牌号 |
| 芯片内部连接 | 线焊、倒装 | 决定芯片朝向与内部连接对象，不决定外部球图 |
| 集成架构 | 单芯片、SiP、2.5D | 描述集成层级；SiP或2.5D也可以采用BGA外部端子 |

PBGA、FCBGA 等名称按不同维度命名，不能视为严格互斥分类。厂商后缀必须结合器件剖面解释。

## 连接对象决定建模对象

线焊型芯片通常有源面朝上，通过键合线连接到基板焊盘，背面由固晶层固定。倒装型芯片有源面朝向基板，通过内部凸点连接；其底填位于芯片与基板之间。外部 BGA 球位于封装基板下方，装板后连接 PCB 焊盘。内部凸点与外部焊球不是同一套阵列。

HBM、SiP 或中介层等部件只有在具体结构存在时才加入；不能为普通 BGA 自动补入 TSV 或硅中介层。未上板时外部球不存在 PCB 端连接，最终上板焊点也不一定保留完整球形。

## 模型与AI绘图输入

最低识别信息为内部互连类型、封装基板、芯片朝向、外部球图、是否含 PCB、工艺阶段。未知内部结构不由外部照片补造。示意图先画部件和连接关系，再补尺寸；不得把“BGA”直接转换成固定的倒装剖面模板。

---
id: KB-COURSE-PACKAGING-20261102-005
title: "线焊PBGA的部件与连接关系"
document_type: knowledge
domain: packaging
status: draft
language: zh-CN
tags: [PBGA, wire-bond, structures]
physics: [thermal, mechanical]
software: []
software_versions: []
source_ids: [SRC-COURSE-CHIP-PACKAGING-02]
source_locator: "课件02 p.2–3（PDF文件页码）"
updated_at: "2026-11-02"
reviewed_by: ""
reviewed_at: ""
---

# 线焊PBGA的部件与连接关系

## 从剖面识别线焊PBGA

课件给出的PBGA示意包含芯片、键合线、塑封体、封装基板、底部焊球和PCB。线焊结构通过细金属线把芯片焊盘连接到基板焊盘，随后由基板布线连接外部球阵列。底部焊球连接封装与PCB，不等同于芯片内部互连。

对具体器件，还需要确认芯片固定层的材料、厚度和位置。示意图中未单独标注的薄层不能自动视为不存在，也不能在没有证据时自行填入胶层尺寸。塑封体覆盖范围、芯片朝向和引线走向应从剖面或封装图确认。

## 与倒装BGA的区别

倒装结构中芯片通过面向基板的凸点互连；线焊PBGA采用键合线连接。因此不能给线焊案例直接添加“芯片下凸点阵列”和相应底填，也不能因为同为BGA而照搬倒装案例的芯片—基板热路径。PBGA说明塑封BGA，本条的线焊示例不代表全部PBGA内部构造。

## 构件表应如何填写

| 对象 | 必要描述 |
| --- | --- |
| 芯片及固定层 | 尺寸、朝向、相对位置、固定材料及厚度证据 |
| 键合线 | 材料、线径、连接对象、是否在研究中显式保留 |
| 塑封体与基板 | 外形、层叠、材料及芯片覆盖关系 |
| 焊球与PCB | 球图、焊后高度、焊盘及PCB叠层 |

课件p.3的尺寸仅属于教学样例，不能替代待复现器件尺寸。课件提出四分之一模型，但结构外观对称并不保证载荷、材料方向和边界也对称；封装侧应交付完整结构事实，由仿真负责人判断简化范围。

## 来源与审核边界

本条为课程课件的归纳及明确标注的基础推导/项目交接建议，尚待审核；未通过本案例求解验证。阅读范围与原文疑点见[课程阅读笔记](../../common/references/course-41-reading-notes.md)。

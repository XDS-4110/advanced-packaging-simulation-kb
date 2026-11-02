---
id: KB-COURSE-PACKAGING-20261102-007
title: "硅中介层TSV与临时工艺层的区分"
document_type: knowledge
domain: packaging
status: draft
language: zh-CN
tags: [2.5D, TSV, interposer]
physics: [thermal, mechanical]
software: []
software_versions: []
source_ids: [SRC-COURSE-CHIP-PACKAGING-15]
source_locator: "课件15 p.3、5–6（PDF文件页码）"
updated_at: "2026-11-02"
reviewed_by: ""
reviewed_at: ""
---

# 硅中介层TSV与临时工艺层的区分

## TSV不是一根没有边界的铜柱

课件的硅中介层示意包括硅本体、铜通孔及绝缘衬层，结合表面布线和互连形成跨厚度连接。建立结构说明时，应分别识别导体、周围介质和硅的接触关系。实际工艺中是否还有阻挡/种子层，需要查器件剖面或工艺资料，不能凭教学图补齐厚度。

微凸点连接芯片与中介层，TSV穿过硅，基板下焊球连接到PCB：三者的空间位置和功能不同。仅有BGA球图不足以确定TSV阵列，也不能用微凸点直径替代TSV直径。

## 永久结构与临时支撑分开登记

课件示意中还有支撑晶圆及临时胶层。它们服务于某个加工阶段，不应自动放进最终服役结构。若研究对象是减薄或解键合阶段，应记录其存在状态；若研究成品工作温度，先核实这些层是否已经去除。

## 结构记录与适用范围

应记录中介层类型及厚度、TSV孔形/直径/深度/节距/数量/位置、绝缘层、上下布线、芯片互连和装配阶段。尺寸含义需明确，例如孔径是否包含绝缘层，铜柱尺寸是否等于刻蚀孔尺寸。

本条只适用于含硅通孔的中介层结构。2.5D还存在其他连接架构；局部硅桥不能直接按全尺寸TSV中介层处理。课件p.5的尺寸和零应变温度只属于示例，不是2.5D通用设计值。

## 来源与审核边界

本条为课程课件的归纳及明确标注的基础推导/项目交接建议，尚待审核；未通过本案例求解验证。阅读范围与原文疑点见[课程阅读笔记](../../common/references/course-41-reading-notes.md)。

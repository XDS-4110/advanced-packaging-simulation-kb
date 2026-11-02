---
id: KB-COURSE-PACKAGING-20261102-006
title: "BGA热路径与热阻数据的使用边界"
document_type: knowledge
domain: packaging
status: draft
language: zh-CN
tags: [BGA, thermal, resistance]
physics: [thermal, mechanical]
software: []
software_versions: []
source_ids: [SRC-COURSE-CHIP-PACKAGING-02, SRC-TI-THERMAL-METRICS-D]
source_locator: "课件02 p.4–9；TI SPRA953D 第1–5节（PDF文件页码）"
updated_at: "2026-11-02"
reviewed_by: ""
reviewed_at: ""
---

# BGA热路径与热阻数据的使用边界

## 热量如何离开芯片

课件将热流概括为朝封装顶部以及朝基板/PCB的两个方向。这有助于识别材料路径：上方可能经过塑封或盖板，下方可能经过固定层或互连、封装基板、焊球和PCB。实际热量还能向侧面扩散，各分支所占比例取决于结构和外部散热条件，不能预设为各一半。

对均匀截面的平板，在稳态一维导热、无内部发热、导热率恒定且不计界面热阻时，`R=L/(kA)`。L是热流方向长度（m），A是垂直热流的面积（m²），k单位W/(m·K)，R单位K/W。芯片到基板的扩散热阻、焊球变截面及界面并不都满足这个简化。

## 数据手册指标不能任意拼成热网络

结到环境热阻包含测试板和环境的影响；结到壳、结到板指标有各自规定的测量路径和条件。热表征参数Ψ与热阻虽可同为K/W，定义和用途仍有区别。因此不能把不同测试条件下的表格数值直接当成同一两支路网络的支路电阻，也不能把壳温直接当结温。此处区别参见[TI SPRA953D](https://www.ti.com/lit/an/spra953d/spra953d.pdf)第1–5节。

## 封装知识库需要保存什么

保存指标原名及符号、器件型号、数据手册版本、测试板、气流/安装条件、温度测点、功耗定义和适用说明。若资料只有一个“热阻”数值，应保留原文并标注指标定义待确认。

课件p.8–9提供测试方法线索，但本条没有逐项核验其列举标准的现行版本，也未复现p.10的仿真结果。它们不能作为本项目热阻已经验证的证据。

## 来源与审核边界

本条为课程课件的归纳及明确标注的基础推导/项目交接建议，尚待审核；未通过本案例求解验证。阅读范围与原文疑点见[课程阅读笔记](../../common/references/course-41-reading-notes.md)。

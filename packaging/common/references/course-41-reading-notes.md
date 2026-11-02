---
id: REF-COURSE-41-20261102
title: "芯片封装仿真41讲：课件阅读与入库边界"
document_type: reference_note
domain: packaging
status: draft
tags: [course, packaging, provenance]
source_ids: [SRC-COURSE-CHIP-PACKAGING-02, SRC-COURSE-CHIP-PACKAGING-03, SRC-COURSE-CHIP-PACKAGING-06, SRC-COURSE-CHIP-PACKAGING-07, SRC-COURSE-CHIP-PACKAGING-13, SRC-COURSE-CHIP-PACKAGING-15]
source_locator: "课件02、03、06、07、13、15；下表为PDF文件页码"
updated_at: "2026-11-02"
reviewed_by: ""
reviewed_at: ""
---

# 芯片封装仿真41讲：课件阅读与入库边界

## 书目信息与访问范围

用户提供的本地课程，课件署名讲师阿姆、平台仿真秀，出版年份与正式版本待确认。目录包含41段MKV、17份PDF（含一篇CSP论文）及STEP文件。本轮以6份课件的逐页图像为依据；PDF中的文字提取不完整，不能把提取到标题视为读到正文。

首次课件整理时，41段视频尚未逐讲观看或转录。后续视频核对已启动，最新阶段记录见[视频笔记](course-video-warpage-correction.md)，仍未完成全课程学习。STEP文件未核验。其余PDF未作为本轮正文依据，不宣称已经学完课程。文件名、页数、SHA256及逐文件阅读状态见[清单](../../../files/course-41-reading-manifest.json)。课件标注版权所有，本次仅提交自主归纳的笔记，不上传课程PDF、截图或视频。

## 解决的问题与条目映射

| 课件及页码 | 已整理内容 |
| --- | --- |
| 02 芯片热模型和模型提取，p.2–3 | [线焊PBGA构件](../../bga/structures/wire-bond-pbga.md) |
| 02，p.4–9 | [热路径与热阻边界](../../bga/fundamentals/thermal-paths-and-resistance.md) |
| 03 PCB和基板的热模型，p.2–7 | [叠层与过孔](../structures/substrate-stackup-and-vias.md) |
| 03，p.5–8；02，p.5–7 | [导热方向性](../materials/directional-conduction-evidence.md) |
| 06 翘曲-热固耦合仿真，p.2–8 | 本笔记记录疑点；不重复已有翘曲验证条目 |
| 07 锡球失效-粘塑性模型仿真，p.3–9 | [蠕变与疲劳的区别](../reliability/solder-creep-and-fatigue.md) |
| 13 加餐-湿气仿真，p.2–7 | [吸湿状态与处理历史](../reliability/moisture-state-and-preconditioning.md) |
| 15 TSV综合仿真，p.3–6 | [TSV层次](../../2-5d/structures/tsv-layer-identification.md)、[工艺时序](../../2-5d/processes/tsv-process-sequence.md) |

## 方法、假设与原文疑点

以下是整理者的核对意见，不冒充讲师的更正：

- 03 p.6：圆环面积应由外圆减内圆得到π(Do²−Di²)/4；课件显示的π(Do−Di)²/4不能作为同心圆环面积使用。
- 06 p.2、5：“对称结构无翘曲”应限定温度分布、材料、约束和初始状态同样满足相应对称条件；不能由基板外形对称推断成品不会翘曲。
- 06 p.4：翘曲正负号依赖观察方向和测量约定；材料模量差与翘曲的简单单调描述不作为通用定律。
- 06 p.7：上排图的质量变化/热流纵轴与DSC/TGA文字标签疑似对调，须回查原图；不能从这些标签直接生成材料测试知识。Tg数值也应附带测量方法和取值准则。
- 07 p.7：Anand参数表缺少可追溯材料标定条件，部分小数显示不清，不转录为材料数据。
- 13 p.2–3：浓度存在kg/m³与kg/mm³的单位差别；归一化含水状态不无条件等于环境相对湿度；湿胀系数需随浓度定义一起保存。
- 15 p.5：几何尺寸、零应变温度是示例，没有证据证明适用于目标中介层。

目录中另有“第11讲warpage计算问题更正”视频，现已补充[带时间戳的画面与转录核对笔记](course-video-warpage-correction.md)，尚未完成原工程复现。本轮没有把相关翘曲算例数值或等效CTE公式作为可执行输入，后续应先核对更正内容。

## 验证与误差

本轮完成课件图像阅读、公式基本量纲/几何检查及来源定位，没有运行课程算例，也没有证实课程结果的实验误差。热阻与热表征参数另参考[TI SPRA953D](https://www.ti.com/lit/an/spra953d/spra953d.pdf)第1–5节；这不构成对全部课件内容的背书。

## 对本项目的适用性

优先服务于封装结构识别、材料条件整理和工艺历史交接。正文中的“交接字段”是本项目整理建议，不是课件规定。所有新增条目均为draft，不直接用于自动生成工程设置。未修改simulation；材料牌号、参数和案例验证仍需原始数据支持。

后续最值得补充的是目标BGA封装剖面/球图/叠层、实际焊料和聚合物的材料测试报告、工艺温度历程及原案例失效判据。补资料时应能定位到具体页码、表格与器件，而不仅是同类型封装的通用数值。

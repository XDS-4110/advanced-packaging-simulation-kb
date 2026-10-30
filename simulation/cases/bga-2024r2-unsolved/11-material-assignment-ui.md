---
id: KB-BGA-ASSIGNMENT-UI-001
title: "BGA Mechanical实体材料赋值截图记录"
document_type: knowledge
domain: simulation
status: draft
language: zh-CN
tags: [BGA, material-assignment, screenshot-evidence, unsolved]
physics: [thermal, structural]
software: [ANSYS Mechanical]
software_versions: ["2024 R2"]
source_ids: [SRC-BGA-ASSIGN-SCREEN-001, SRC-BGA-001, SRC-BGA-REV3-001]
source_locator: "七张实体Details截图按用户发送顺序编号1至7；文件哈希见data/material-assignment-screenshots/source-manifest.json"
updated_at: "2026-10-30"
reviewed_by: ""
reviewed_at: ""
---

# BGA Mechanical实体材料赋值截图记录

用户提供的七张Mechanical截图显示选中的几何实体、材料赋值字段及实体高亮，补充初次工程XML的实体—材料映射。原截图不上传仓库，提取值可供RAG草稿检索，不视为已验证的通用参数。

## 实体与材料映射

| 图号 | 名称线索 | 部件解释 | Mechanical材料赋值 | 共享材料ID |
| --- | --- | --- | --- | --- |
| 1 | XINPIAN | 芯片 | SI | MAT-BGA-SI-001 |
| 2 | Underfill | 底部填充 | Underfill | MAT-BGA-UNDERFILL-001 |
| 3 | TUDIAN，多选 | 凸点 | Sn63Pb37 | MAT-BGA-SN63PB37-001 |
| 4 | JIBAN | 封装基板 | BT | MAT-BGA-BT-001 |
| 5 | SUFENGLIAO | 塑封料 | SFL | MAT-BGA-SFL-001 |
| 6 | HANQIU，多选 | 焊球 | Sn63Pb37 | MAT-BGA-SN63PB37-001 |
| 7 | PCB | PCB | BT | MAT-BGA-BT-001 |

部件类别依据名称线索、用户上下文和高亮位置解释。截图确认可见选中对象的材料名称，与初次工程映射相符。历史320实体、155凸点/160焊球等计数以原工程导出为依据；不能由多选截图显示的最后序号证明全部实体已选中或逐个核对。

## 可见公共设置

七张截图均显示：抑制=否，刚度行为=柔性，坐标系=默认坐标系，参考温度=按环境，非线性效应=是，热应变效应=是。这些是界面设置值，不代表所有材料都采用非线性本构或已经发生非线性响应。

参考温度“按环境”仅证明选择了继承环境的方式，没有给出结构无应力参考温度数值。用户已说明结构分析尚未开展，结构环境/约束/参考温度将于后续阶段建立；不能用热初始25 ℃或材料场变量默认22 ℃替代它。

## 几何读数与使用限制

截图Details包围框读数依次为：芯片5×5×0.35 mm、Underfill 5×5×0.05 mm、凸点多选0.075×0.075×0.05 mm、基板12×12×0.27 mm、塑封料12×12×0.624 mm、焊球多选0.54×0.54×0.3 mm、PCB 140×140×1.8 mm。

这些是界面显示的包围框数值，不是完整建模尺寸图。尤其PCB外形为圆形时140×140是包围框而非方板长宽；凸点/焊球多选的读数不作为整个群组尺寸，也不自动认定为直径。自动重建仍应使用几何测量、原CAD或完整实体导出。

## 已补齐与仍未完成

- 已补齐：七类部件材料赋值名称的Mechanical界面证据；PCB和封装基板均赋BT已得到确认。
- 未验证：修正后的SFL比热、Anand和温度依赖表是否已同步到Mechanical实际材料数据。名字相同不能证明数值版本相同。
- 未验证：PCB与封装基板共用BT的物理依据、材料牌号/晶向/工艺及温区处理。
- 未完成：按项目统一规则进行全部实体的网格验收。截图中的网格统计不能代替完整审核，也不构成重要区域确认或低质量例外批准。

[转录赋值与几何读数](data/material-assignment-screenshots/assignments.csv)、[七张图片来源哈希](data/material-assignment-screenshots/source-manifest.json)。材料数值继续引用 [最新Engineering Data证据](../../../shared/materials/bga-20261030-revision3.md) 和 [材料定义截图](../../../shared/materials/bga-material-screenshots.md)，不另建重复物性库。

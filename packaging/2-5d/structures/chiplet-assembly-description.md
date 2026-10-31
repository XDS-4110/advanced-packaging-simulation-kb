---
id: KB-STRUCT-CHIPLET-001
title: "多芯片装配结构应记录哪些字段"
document_type: knowledge
domain: packaging
status: reviewed
language: zh-CN
tags: [advanced-packaging, chiplet, structure-modeling, external-source]
physics: [thermal, structural]
software: []
software_versions: []
source_ids: [SRC-GH-IHP-CHIPLET-001]
source_locator: "固定提交的CHIPLET_FORMAT_SPEC：Scope、Components、Connection Stacks、Interfaces；coord_frame_contract：1.4、1.5、3"
updated_at: "2026-10-31"
reviewed_by: "Codex（原文与适用范围核对，未执行工具验证）"
reviewed_at: "2026-10-31"
---

# 多芯片装配结构应记录哪些字段

## 来源中可直接借鉴的内容

IHP的`.chiplet`用YAML表达多芯片装配：部件身份、类型、尺寸、位置、旋转、连接堆叠和接口。规范本身不提供完整热、功耗或力学材料表。[字段原文](https://github.com/IHP-GmbH/chiplet-spec/blob/aa2eee4e71f1678f0b791d5129a8dfd263d6bb37/docs/CHIPLET_FORMAT_SPEC.md)

坐标合同规定XY位置为部件几何中心，坐标系以中介层GDS包围框角点为原点、Y向上，使用μm；Z表示部件底部安装面。中介层还具有专门的安装面语义，不能一律用厚度代替装配高度。[坐标合同1.4、1.5及3节](https://github.com/IHP-GmbH/chiplet-spec/blob/aa2eee4e71f1678f0b791d5129a8dfd263d6bb37/docs/coord_frame_contract.md)

## 对本项目的用途（本库归纳）

结构记录应分别保留部件、连接和几何定位，不把“中介层材料”“连接方式”和“几何厚度”混成同一个属性。实体材料数值统一引用共享材料ID/revision。

新增部件时，要明确它连接哪些对象、连接层是否单独建模，以及层间高度是否发生变化。共享坐标系不等于所有外部文件采用同一种位置锚点。

本条目reviewed仅表示上述格式内容及来源已核对，不表示`.chiplet`能直接生成Workbench实体或已验证热力耦合模型。项目自己的[结构输入模板](../../../shared/templates/package-structure-input.json)与[中介层插入流程草稿](../../../simulation/modeling/insert-interposer-workflow.md)需要单独适配。

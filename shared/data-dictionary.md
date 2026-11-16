---
id: KB-DATA-DICT-001
title: "可追溯资料字段与当前工程的区别"
document_type: knowledge
domain: shared
status: draft
language: zh-CN
software: []
software_versions: []
source_ids: [SRC-KB-COMSOL-MIGRATION-20261116]
source_locator: "本库方法整理；具体软件规则另见 COMSOL 官方资料草稿，未经本机算例验证"
updated_at: "2026-11-16"
reviewed_by: ""
reviewed_at: ""
---

# 可追溯资料字段与当前工程的区别

## 通用字段

| 字段 | 含义与边界 |
| --- | --- |
| id / stable_id | 本库明确登记的身份；不是当前求解器中的域或面编号 |
| model_revision | 对应的几何/模型修订；缺失时不能定位运行时对象 |
| source_ids / source_locator | 来源登记与可核对位置，不作为执行授权 |
| status | draft / reviewed / validated / deprecated；审核状态与仿真求解状态不同 |
| value / unit | 数值与单位必须共同记录；材料温区、方向和来源不得省略 |
| resolution_state | 实体映射是否完成；同名不能证明映射正确 |

## 空表与读取

实体和材料注册表目前只保留字段，不包含当前客户端项目。查不到时返回缺失，不猜测 ID、属性或默认值。客户端读取当前项目、几何、设置和结果后，再按明确修订建立映射。

不同证据中的值冲突时保留来源和修订，不取平均或悄悄覆盖。

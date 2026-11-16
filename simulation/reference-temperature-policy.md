---
id: KB-POLICY-REFTEMP-001
title: "参考温度必须由当前模型显式记录"
document_type: knowledge
domain: simulation
status: draft
language: zh-CN
software: []
software_versions: []
source_ids: [SRC-REF-TEMP-POLICY-USER-001, SRC-KB-COMSOL-MIGRATION-20261116]
source_locator: "本库方法整理；具体软件规则另见 COMSOL 官方资料草稿，未经本机算例验证"
updated_at: "2026-11-16"
reviewed_by: ""
reviewed_at: ""
---

# 参考温度必须由当前模型显式记录

## 现行使用边界

参考温度决定热应变的零点；它不自动等于初始温度、载荷首点或环境温度。具体值应来自当前材料数据定义、装配状态或研究假设，不从历史界面的默认值补齐。

旧项目曾确认按环境温度作为简化约定；这项决策保留来源记录，但软件迁移后的实际值、继承关系与适用对象未经确认，因此没有转换成 COMSOL 默认规则。

## 每个案例要记录

记录温度数值和单位、适用域、材料 CTE 类型与数据基准、初始温度、是否包含制造残余应力、选择依据、模型修订及读回证据。更改参考状态后，应重新评估热应力和翘曲。

不能因参考温度与环境相同就声称器件真实无应力；这可能只是模型假设。具体模型取值保持待核实。

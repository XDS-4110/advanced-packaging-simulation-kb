---
id: KB-STRUCT-REFTEMP-001
title: "热应变参考状态与证据"
document_type: knowledge
domain: simulation
status: draft
language: zh-CN
software: []
software_versions: []
source_ids: [SRC-BGA-COMSOL63-EXPANSION, SRC-LIT-EMC-WARPAGE-2022]
source_locator: "本库方法整理；具体软件规则另见 COMSOL 官方资料草稿，未经本机算例验证"
updated_at: "2026-11-16"
reviewed_by: ""
reviewed_at: ""
---

# 热应变参考状态与证据

## 不同温度的含义

初始温度描述分析开始时的热状态；边界温度规定某些面上的温度；环境温度用于换热条件；热应变参考温度规定热膨胀的参考状态。它们可能数值相同，但不能凭名称互相替代。

常数 CTE 的简单情形可写作热应变 α(T−Tref)。温度相关数据要区分瞬时/切线、平均/割线或直接热应变数据，并核对其测量基准、方向和适用范围；不能只复制一列数值。

## 核验内容

读取当前模型实际使用的参考温度、材料定义和作用域，核对它们与工艺/安装假设一致。记录模型修订、来源、单位及读回证据；修改参考状态后重新求解。没有材料或工艺依据时明确标记假设并评估敏感性。

COMSOL 中的具体定义应查阅对应版本的热膨胀文档；本文不提供软件字段、默认值或本机构型验证。

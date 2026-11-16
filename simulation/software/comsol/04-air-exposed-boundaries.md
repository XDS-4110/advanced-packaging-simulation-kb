---
id: "COMSOL-GUIDE-AIR-EXPOSED-BOUNDARIES"
title: "空气暴露面与固体接触面的区分"
document_type: "software-guide"
domain: "simulation"
status: "draft"
software_versions: ["COMSOL Multiphysics 6.4"]
source_ids: ["SRC-COMSOL-OFFICIAL-adjacent-selection", "SRC-COMSOL-OFFICIAL-thermal-contact"]
source_locator: "SRC-COMSOL-OFFICIAL-adjacent-selection: Adjacent — Table 2-136; SRC-COMSOL-OFFICIAL-thermal-contact: Thermal Contact; Pair Selection"
verification: "official_documentation_checked; not_run_locally"
updated_at: "2026-11-16"
tags: ["COMSOL", "外表面", "空气暴露", "焊球", "塑封", "引脚", "接触面", "Adjacent", "热边界"]
language: "zh-CN"
software: ["COMSOL Multiphysics"]
reviewed_by: ""
reviewed_at: ""
---

# 空气暴露面与固体接触面的区分

适用条件：芯片对流、温循环境加载及内部热接触设置。

本文为官方资料的原创简要归纳及项目操作检查点；状态为草稿，须人工审核。

## 已核对的官方规则
Adjacent Selection 的外侧/内侧选项依据域集合补集的连通区域分类；它不是对真实空气流通条件的识别。Thermal Contact 用于固体接触界面的导热关系，可作用于内部边界或已有配对，与空气侧对流条件不同。

## 项目操作检查点
1. 先确认最终几何类型、实体相交与相接关系，再建立候选边界。装配体中的接触表面不能仅凭“只邻接一个域”判断为空气暴露面。
2. 引脚被塑封覆盖的面、焊球与芯片/基板重合的接触区域要从空气侧边界中排除；若接触区和暴露区同属一个面，先做必要分割。
3. 芯片下表面与基板上表面的间隙若与外部空气连通，应保留未被焊球覆盖的区域。密闭空腔需另定气体/换热模型，不直接套外部环境条件。
4. 隐藏外壳后检查是否误选内部固体界面，核对面组面积、连通性和接触覆盖。
5. 接触导热参数、对流系数与材料参数必须有依据。无法确认时输出待核对面组，不把候选选择标记为已验证。

## 验证边界
外侧分类及 Thermal Contact 定义经官方文档核对；具体引脚、焊球分割策略是本项目建模要求，未在本地几何执行。

## 官方来源

- [model.selection()](https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/comsol_api_general.47.56.html)；版本：6.4；定位：Adjacent — Table 2-136；访问日期：2026-11-16。
- [Thermal Contact](https://doc.comsol.com/6.4/doc/com.comsol.help.heat/heat_ug_ht_features.09.100.html)；版本：6.4；定位：Thermal Contact; Pair Selection；访问日期：2026-11-16。


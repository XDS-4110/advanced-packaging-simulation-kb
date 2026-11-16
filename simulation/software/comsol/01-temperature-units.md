---
id: "COMSOL-GUIDE-TEMPERATURE-UNITS"
title: "温度单位：摄氏度、开尔文与温差"
document_type: "software-guide"
domain: "simulation"
status: "draft"
software_versions: ["COMSOL Multiphysics 6.4"]
source_ids: ["SRC-COMSOL-OFFICIAL-temperature-units"]
source_locator: "SRC-COMSOL-OFFICIAL-temperature-units: Differential vs. Absolute Temperature"
verification: "official_documentation_checked; not_run_locally"
updated_at: "2026-11-16"
tags: ["COMSOL", "温度", "摄氏度", "开尔文", "degC", "K", "温差", "初始温度", "热循环"]
language: "zh-CN"
software: ["COMSOL Multiphysics"]
reviewed_by: ""
reviewed_at: ""
---

# 温度单位：摄氏度、开尔文与温差

适用条件：热传导、温循边界、热辐射、热膨胀参数输入。

本文为官方资料的原创简要归纳及项目操作检查点；状态为草稿，须人工审核。

## 已核对的官方规则
绝对温度的摄氏度与开尔文换算包含偏移量；COMSOL 支持 `[degC]` 与 `[K]`。例如 `25[degC]` 对应 `298.15[K]`，而 `25[K]` 不是室温。含温度的复合量与独立绝对温度的换算规则不同，不能机械地给所有含温度数据加 273.15。辐射计算需要绝对温度。

## 项目操作检查点
1. 读取字段标签、输入表达式与单位，确认“25”表示 25 ℃还是 25 K；不根据习惯静默改值。
2. 温度表先确定原始单位，再统一转换或交由有单位的函数处理；禁止前端、后端各转换一次。
3. 初始温度、边界温度、环境温度和无热应变参考温度分别记录，不能互相代替。
4. 预览与导出同时检查最低温度、最高温度及单位。检查点：`0[degC]` 应对应 `273.15[K]`。
5. 材料的热膨胀系数、温度依赖性和参考温度须有来源或由用户确认，不根据截图自动填写。

## 验证边界
单位行为已由官方文档核对；以上检查流程为项目规则，尚未在本地 COMSOL 工程中执行验证。

## 官方来源

- [About Temperature Units](https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/comsol_ref_modeling.19.104.html)；版本：6.4；定位：Differential vs. Absolute Temperature；访问日期：2026-11-16。


---
id: "COMSOL-GUIDE-MPH-SAVE-READBACK"
title: "MPH 自动保存、重新读取与结果核对"
document_type: "software-guide"
domain: "simulation"
status: "draft"
software_versions: ["COMSOL Multiphysics 6.4"]
source_ids: ["SRC-COMSOL-OFFICIAL-modelutil", "SRC-COMSOL-OFFICIAL-model-save", "SRC-COMSOL-OFFICIAL-parameter-api"]
source_locator: "SRC-COMSOL-OFFICIAL-modelutil: ModelUtil.load; loadCopy; loadOnServer; SRC-COMSOL-OFFICIAL-model-save: model.save; model.location; model.getComsolVersion; SRC-COMSOL-OFFICIAL-parameter-api: get; evaluate; evaluateUnit; descr"
verification: "official_documentation_checked; not_run_locally"
updated_at: "2026-11-16"
tags: ["COMSOL", "Java API", "MPH", "保存", "读回", "项目状态", "参数", "求解状态", "源模型", "配置模型"]
language: "zh-CN"
software: ["COMSOL Multiphysics"]
reviewed_by: ""
reviewed_at: ""
---

# MPH 自动保存、重新读取与结果核对

适用条件：客户端把参数交给 COMSOL、生成可查看 MPH、Agent 执行后的核对。

本文为官方资料的原创简要归纳及项目操作检查点；状态为草稿，须人工审核。

## 已核对的官方规则
ModelUtil.load 可载入 MPH；loadCopy 与原文件不建立保存关联，首次保存需明确文件名。model.save 可保存 MPH，model.location 可读取保存位置；相对路径依赖模型/运行目录。参数 API 可读取原表达式、描述、数值与单位，适合核对已写入的设置。

## 项目操作检查点
1. 明确区分原始导入文件、未保存预览、已配置 MPH、已求解 MPH，并把当前项目绑定到正确产物。
2. 写入后依既有操作流程完成必要构建，以明确绝对路径保存，记录产物、时间及版本；保存成功不等于几何、网格或求解成功。
3. 从保存产物重新加载，核对参数表达式/单位、域与面选择、材料、物理节点及研究时段；不能仅回显客户端传出的请求。
4. 如宣称“已求解”，还要核对结果数据集、有效时间/参数、求解日志和指标。只有模型文件存在不够。
5. 对照目标核对成功后再推进下一步；失败时说明已完成到哪里。禁止为了通过读回检查自动补猜材料物性。
6. 报告附实际产物路径和结果来源，避免用源几何“没有研究”的状态覆盖已配置模型的真实状态。

## 验证边界
加载、保存与参数读取方法有 6.4 官方依据；完整操作—读回—核对流程是项目规则，本条不表示已运行本地 Java 或验证客户端。

## 官方来源

- [ModelUtil](https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/comsol_api_general.47.15.html)；版本：6.4；定位：ModelUtil.load; loadCopy; loadOnServer；访问日期：2026-11-16。
- [model](https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/comsol_api_general.47.16.html)；版本：6.4；定位：model.save; model.location; model.getComsolVersion；访问日期：2026-11-16。
- [model.param() and model.result().param()](https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/comsol_api_general.47.50.html)；版本：6.4；定位：get; evaluate; evaluateUnit; descr；访问日期：2026-11-16。


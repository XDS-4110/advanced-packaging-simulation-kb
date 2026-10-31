---
id: KB-THERMAL-MFIT-INPUT-001
title: "多芯片热模型的结构材料与功率输入参考"
document_type: knowledge
domain: simulation
status: reviewed
language: zh-CN
tags: [advanced-packaging, chiplet, structure-modeling, external-source]
physics: [thermal, structural]
software: []
software_versions: []
source_ids: [SRC-GH-MFIT-001]
source_locator: "固定提交INPUT_FORMAT：1 Material、2 Geometry、3 Power Configuration、4 Power Sequence；README Major features"
updated_at: "2026-10-31"
reviewed_by: "Codex（原文与适用范围核对，未执行工具验证）"
reviewed_at: "2026-10-31"
---

# 多芯片热模型的结构材料与功率输入参考

## 原项目输入组织

MFIT将材料、几何层叠、热源分布和功率时序分开。材料支持方向热导率；几何使用mm、环境温度使用K，功率时序按各热源最大功率的百分数表达。[输入说明](https://github.com/AlishKanani/MFIT/blob/4444336d95fe7e9a3bf440c96937831126c6a37f/INPUT_FORMAT.md)

README说明其RC/DSS热模型以ANSYS Fluent有限元结果作对照，并提供参考模型；本次未运行或复现这些验证。[项目说明](https://github.com/AlishKanani/MFIT/blob/4444336d95fe7e9a3bf440c96937831126c6a37f/README.md)

## 用于本项目时的转换要求（归纳）

从MFIT参考输入转为Workbench输入时，先转换几何、温度与功率单位。功率百分数需要结合对应最大功率才能得到W，不能把百分数直接作为发热功率；热RC节点设置不是Mechanical有限元网格控制。

可借鉴分层热源记录方式，但不沿用示例尺寸、材料数值、对流系数或网格数量作为项目默认值。该模型输入没有构成完整结构应力本构/约束定义；温循的外表面指定温度与工作发热工况仍应分开。

材料继续使用[共享库](../../shared/materials/README.md)，结构使用[项目结构模板](../../shared/templates/package-structure-input.json)，分析输出需单独验证。

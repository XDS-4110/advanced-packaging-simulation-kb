---
id: KB-ANSYS242-OPS-03
title: "生成网格并按项目规则逐体验收"
document_type: software_operation
domain: simulation
status: reviewed
language: zh-CN
tags: [ANSYS, thermal-structural, operation, meshing]
physics: [thermal, structural]
software: [ANSYS Workbench, ANSYS Mechanical]
software_versions: ["2024 R2"]
source_ids: [SRC-ANSYS-242-OPS-API, SRC-PROJECT-MESH-CONFIRM-001]
source_locator: "正文列出的v242类/方法与固定提交示例段落；版本和哈希见data/source-selection.json"
updated_at: "2026-11-02"
reviewed_by: "Codex（官方文档核对；未在本机执行仿真）"
reviewed_at: "2026-11-02"
verification_scope: "API条目存在性与操作组织核对；非运行或物理验证"
---

# 生成网格并按项目规则逐体验收

## 前置输入

当前几何、材料/接触状态、仿真目标与待检查实体。重要区域按项目流程由LLM提出，再经人工确认。

## 操作与核对

1. 先采用系统自动划分，记录实际网格；v242 `Mesh.GenerateMesh()`提供生成入口。
2. 按[统一网格规则](../../verification/project-mesh-requirements.md)检查层数方向、圆周分段、形状、每实体平均/最小单元质量及全模型单元数。
3. 整体统计不能替代每个实体统计；全模型节点/单元数不能按各体节点数简单相加，接口共享节点可能重复。
4. 不合格时遵循统一规则中的尺寸优化和方法分支。重要区域确认、低质量单元例外批准、超过300万单元后的人工决定相互独立。

## 完成证据与停止条件

返回全模型节点/单元数、逐实体质量和层数证据、关键区域以及人工决定记录。未能导出的指标标记待核实；生成网格成功不等于合格。API存在性不证明逐实体质量导出已实现，不能伪造评估报告。

本条目仅提供软件操作检查顺序，所有数值阈值只引用统一规范，不复制成第二份规则。

## 精确来源

- [v242 Mesh](https://scripting.mechanical.docs.pyansys.com/version/stable/api/ansys/mechanical/stubs/v242/Ansys/ACT/Automation/Mechanical/MeshControls/Mesh.html)：GenerateMesh及网格相关属性。
- SRC-PROJECT-MESH-CONFIRM-001：项目用户确认的验收规则。

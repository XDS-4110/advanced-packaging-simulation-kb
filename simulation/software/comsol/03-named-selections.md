---
id: "COMSOL-GUIDE-NAMED-SELECTIONS"
title: "域组、面组与几何修改后的选择复核"
document_type: "software-guide"
domain: "simulation"
status: "draft"
software_versions: ["COMSOL Multiphysics 6.4"]
source_ids: ["SRC-COMSOL-OFFICIAL-explicit-selection", "SRC-COMSOL-OFFICIAL-cumulative-selection", "SRC-COMSOL-OFFICIAL-cad-import"]
source_locator: "SRC-COMSOL-OFFICIAL-explicit-selection: Entities to Select; Resulting Selection; Cumulative Selection; SRC-COMSOL-OFFICIAL-cumulative-selection: Cumulative Selections; SRC-COMSOL-OFFICIAL-cad-import: Associativity; Length Unit; Simplify and Repair"
verification: "official_documentation_checked; not_run_locally"
updated_at: "2026-11-16"
tags: ["COMSOL", "域编号", "面编号", "命名选择", "域组", "面组", "材料", "固定约束", "重建", "拓扑"]
language: "zh-CN"
software: ["COMSOL Multiphysics"]
reviewed_by: ""
reviewed_at: ""
---

# 域组、面组与几何修改后的选择复核

适用条件：材料映射、固定面命名、几何尺寸修改与 CAD 替换。

本文为官方资料的原创简要归纳及项目操作检查点；状态为草稿，须人工审核。

## 已核对的官方规则
Explicit Selection 区分对象、域、边界、边和点，Keep selection 与 Show in physics 控制后续可用性。Cumulative Selection 能汇集几何特征的选择。CAD 关联重导入依赖实体匹配；拓扑改变时关联可能失败，不能保证旧面编号仍指向同一物理部位。

## 项目操作检查点
1. “同材料的多个域合成一个组”应明确为命名选择；它不等于删除内部边界或把多个域布尔合并成一个域。
2. 材料选择域；底面固定约束等表面条件选择边界。名称可为“铜引脚”“固定底面”，编号仅作当前几何的成员标识。
3. 修改尺寸、替换模型或重新分割后，重新读取成员、数量和空间位置，并高亮复核。不能只确认旧编号仍存在。
4. 保存时记录几何来源、版本及选择成员；若成员映射存在歧义，标记“待核对”，不要静默迁移材料或边界。
5. 颜色、文件名和域序号不是材料物性的充分证据；同组域的材料名称及参数仍需明确来源。

## 验证边界
选择与 CAD 关联行为有官方依据；以上保存、提示和复核顺序属于项目实施规则，未做本地模型验证。

## 官方来源

- [Explicit Selection (Geometry Sequences)](https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/comsol_ref_visualizationselection.22.31.html)；版本：6.4；定位：Entities to Select; Resulting Selection; Cumulative Selection；访问日期：2026-11-16。
- [Cumulative Selections](https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/comsol_api_geom.48.034.html)；版本：6.4；定位：Cumulative Selections；访问日期：2026-11-16。
- [Importing and Exporting CAD Files](https://doc.comsol.com/6.4/doc/com.comsol.help.design/design_ug_function.5.24.html)；版本：6.4；定位：Associativity; Length Unit; Simplify and Repair；访问日期：2026-11-16。


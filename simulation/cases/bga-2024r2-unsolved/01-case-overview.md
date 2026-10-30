---
id: CASE-BGA-2024R2-001
title: "BGA 未求解工程：系统组成与提取范围"
document_type: case
domain: simulation
status: draft
language: zh-CN
tags: [BGA, thermal-cycling, extracted, unsolved]
physics: [thermal, structural]
software: [ANSYS Workbench, ANSYS Mechanical]
software_versions: ["2024 R2"]
source_ids: [SRC-BGA-001]
source_locator: "见本条目来源定位及 data/source-manifest.json"
updated_at: "2026-10-30"
reviewed_by: ""
reviewed_at: ""
---

# BGA 未求解工程：系统组成与提取范围

> 本文是已有工程的设置提取，未求解、未验证，不是推荐参数或通用建模规范。

## 已确认事实

- Workbench 工程版本为 2024 R2，项目记录版本号 24.2.1.0。
- 实际系统对象为 `SYS`（Transient Thermal）和 `SYS 1`（Transient Structural，目录 SYS-1）。工程中出现的其他分析模板不等于已创建分析。
- `journal1.wbjn` 记录：结构系统共享热系统的 Engineering Data、Geometry 和 Model；热系统的 Solution 数据传递到结构 Setup。
- 现有 CAERep 是瞬态热分析的导出快照，不能用它代替结构分析的完整设置。
- Mechanical 名称索引中存在“导入的载荷 (A6)”和“导入的几何体温度”对象；仅能确认对象存在，不能证明导入成功、映射正确或具有已求解温度数据。
- 用户说明尚未求解；目录与归档中未发现 `.rth`、`.rst` 结果文件。`ds.dat` 中含材料和网格不代表求解成功。

## 本次范围

收录现有设置与缺失信息，不推断实际芯片功率、制造参考温度或试验标准，不运行求解，不纠正源数据。

## 来源定位

`BGA.wbpj`：`/Storage/Containers/Container[@Name='Schematic']/Object` 中的两个 System 对象；`journal1.wbjn` 最后一次 `template2 = GetTemplate` 后的共享与 DataTransferFrom 记录；`CAERep.xml/SolverRep`；`SYS.mechdb` 的 `DS Objects Information` 名称索引。

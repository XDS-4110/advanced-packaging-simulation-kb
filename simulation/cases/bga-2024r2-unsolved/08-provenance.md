---
id: KB-BGA-PROVENANCE-001
title: "BGA 提取来源、一致性与可追溯方式"
document_type: knowledge
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

# BGA 提取来源、一致性与可追溯方式

> 本文是已有工程的设置提取，未求解、未验证，不是推荐参数或通用建模规范。

## 数据读取方法

1. 只读解析工作目录的 BGA.wbpj、CAERep.xml、MatML.xml 和 EngineeringData.xml。
2. 流式扫描约 1.01 GB 的 ds.dat，只提取参数证据、节点范围和单元块计数。
3. 只读 HDF5 容器中的对象名称索引，辅助识别网格控制、结果请求和导入载荷对象；不猜测私有二进制字段语义。
4. 只读列出 BGA.wbpz 条目并对小于 100 MB 的现有对应文件核对 CRC；其他文件未标记为已完成 CRC 核对。

## 工程目录与归档

关键文件 CAERep.xml、MatML.xml、EngineeringData.xml 和 SYS.mechdb 的归档 CRC 与工作目录相同。BGA.wbpj、journal2.wbjn 和 .project_cache 的归档与本地记录存在差异，本次以工作目录设置为主，未将两份文件视为完全相同快照。

归档还包含 `import_files/CMB97D39B(PCB--).STEP`；工作目录中未发现此对应路径。本次未对 CAD 曲面重建/逐实体精确尺寸作完整解析。

## 可追溯文件

- [源文件大小、SHA-256 及归档清单](data/source-manifest.json)
- [APDL 命令行号与网格计数证据](data/apdl-evidence.json)
- [HDF5 对象名称与 ID](data/object-names.json)
- [材料数据及其原始限定字段](../../../shared/materials/datasets/bga-2024r2-draft/materials.json)
- [热分析设置快照](data/thermal-settings.json)

原始工程文件保留在用户电脑，不复制进 GitHub。数据 SHA-256 用于后续检查对应源文件是否变化。

## RAG 状态

本案例可用于人工审阅和独立草稿索引。按仓库默认规则，draft 不进入正式工程决策索引；技术内容经人工审核后再升级状态。源参数与修正建议分别记录。

## 提取后的快照复核

复核时工作目录的 SYS/MECH 生成文件已不在原路径。因此进一步对归档中的 CAERep.xml、MatML.xml、EngineeringData.xml、SYS.mechdb 和约 1 GB 的 ds.dat 逐个流式计算 SHA-256，均与提取时的源文件哈希完全一致。归档本体哈希及已核对条目见 source-manifest.json。本文对应该归档快照；用户后续修改需作为新版本重新提取。

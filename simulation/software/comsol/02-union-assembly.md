---
id: "COMSOL-GUIDE-UNION-ASSEMBLY"
title: "联合体与装配体：连续性、接触对及压印"
document_type: "software-guide"
domain: "simulation"
status: "draft"
software_versions: ["COMSOL Multiphysics 6.4"]
source_ids: ["SRC-COMSOL-OFFICIAL-union-assembly"]
source_locator: "SRC-COMSOL-OFFICIAL-union-assembly: Physics Considerations; Form Union/Assembly"
verification: "official_documentation_checked; not_run_locally"
updated_at: "2026-11-16"
tags: ["COMSOL", "Union", "Assembly", "联合体", "装配体", "接触对", "恒等对", "压印", "外表面"]
language: "zh-CN"
software: ["COMSOL Multiphysics"]
reviewed_by: ""
reviewed_at: ""
---

# 联合体与装配体：连续性、接触对及压印

适用条件：多域芯片、引脚、塑封、焊球与基板的最终几何处理。

本文为官方资料的原创简要归纳及项目操作检查点；状态为草稿，须人工审核。

## 已核对的官方规则
Form Union 将对象联合，域之间仍可保留内部边界，通常通过共享几何实现物理场连续。Form Assembly 保留分离对象，连续连接需要相应的配对及物理条件；存在相对运动、滑移或接触时可需要装配体。Create imprints 可把相接的大面分出匹配区域。自动建立恒等对不等于已经完成全部接触物理设置。

## 项目操作检查点
1. 先读取最终几何节点的实际设置，不以“多域”直接判定几何错误。
2. 固结连接、滑移接触、热接触电阻分别识别，按真实物理关系决定 Union 或 Assembly。
3. 装配体核对配对覆盖、源面和目标面，以及物理场是否引用该对。
4. 压印或联合后重建并复核域、面、材料分配和边界命名，特别检查引脚穿出塑封的位置。
5. 不为获取“外表面”而无条件改成 Union；不把界面换热系数、摩擦或接触电阻自动补成猜测值。

## 验证边界
官方说明支持上述功能区分。具体封装能否成功联合、压印及配对，仍须用该几何在本地验证；本条未执行这些操作。

## 官方来源

- [The Form Union/Assembly Node — Unifying the Geometry](https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/comsol_ref_geometry.23.019.html)；版本：6.4；定位：Physics Considerations; Form Union/Assembly；访问日期：2026-11-16。


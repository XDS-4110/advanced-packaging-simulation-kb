---
id: "COMSOL-GUIDE-GEOMETRY-PARAMETERS"
title: "局部尺寸修改、原生参数化与几何容差"
document_type: "software-guide"
domain: "simulation"
status: "draft"
software_versions: ["COMSOL Multiphysics 6.4"]
source_ids: ["SRC-COMSOL-OFFICIAL-scale", "SRC-COMSOL-OFFICIAL-geometry-new", "SRC-COMSOL-OFFICIAL-cad-import"]
source_locator: "SRC-COMSOL-OFFICIAL-scale: Input; Scale Factor; Center of Scaling; SRC-COMSOL-OFFICIAL-geometry-new: Geometry News — Create parameters; SRC-COMSOL-OFFICIAL-cad-import: Associativity; Length Unit; Simplify and Repair"
verification: "official_documentation_checked; not_run_locally"
updated_at: "2026-11-16"
tags: ["COMSOL", "几何参数", "域尺寸", "整体缩放", "原生参数化", "STEP", "微米", "容差", "几何重建"]
language: "zh-CN"
software: ["COMSOL Multiphysics"]
reviewed_by: ""
reviewed_at: ""
---

# 局部尺寸修改、原生参数化与几何容差

适用条件：导入芯片的尺寸修改、参数化重建及毫米/微米模型适配。

本文为官方资料的原创简要归纳及项目操作检查点；状态为草稿，须人工审核。

## 已核对的官方规则
Scale 作用于其输入对象；选中全部对象就会缩放整体，可各向同性或各向异性，并有缩放中心。6.4 的部分几何基元支持 Create parameters。CAD 导入的长度单位和绝对导入容差可设置，简化/修复可能删除容差以下细节。

## 项目操作检查点
1. 改某个部件前，确认对象/域映射及被引用的几何参数；核对作用对象，不能把整体 Scale 伪装成局部尺寸编辑。
2. 导入几何加缩放节点不等于重建了原生参数化特征树。若需重建，应明确基元、截面、扫掠和布尔关系，并对原件逐部件比对。
3. 对引脚弯曲、键合线和薄层，不能仅以包围盒替代真实形状。比较尺寸、体积、位置及接触/间隙关系后再接受重建结果。
4. 毫米模型的固定绝对容差不能直接沿用到所有微米模型；读取长度单位、最小重要特征和实际容差，再检查细节是否被修复删除。
5. 参数改变后复核域/面命名选择及材料映射；保持“预览”和“已保存”的状态清晰。不要由几何颜色推断材料参数。

## 验证边界
缩放、几何基元和导入设置有官方依据；“重建等价性”与容差合适性需针对模型测量验证，当前未做本地验证。

## 官方来源

- [Scale](https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/comsol_ref_geometry.23.100.html)；版本：6.4；定位：Input; Scale Factor; Center of Scaling；访问日期：2026-11-16。
- [New Geometry and Mesh Functionality](https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/comsol_release_text.06.008.html)；版本：6.4；定位：Geometry News — Create parameters；访问日期：2026-11-16。
- [Importing and Exporting CAD Files](https://doc.comsol.com/6.4/doc/com.comsol.help.design/design_ug_function.5.24.html)；版本：6.4；定位：Associativity; Length Unit; Simplify and Repair；访问日期：2026-11-16。


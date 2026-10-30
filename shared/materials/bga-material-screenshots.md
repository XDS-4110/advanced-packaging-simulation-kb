---
id: MAT-BGA-SCREEN-EVIDENCE-001
title: "BGA 材料定义截图核对"
document_type: material
domain: shared
status: draft
language: zh-CN
tags: [BGA, material-input, screenshot-evidence]
physics: [thermal, structural]
software: [ANSYS Workbench]
software_versions: []
source_ids: [SRC-BGA-MAT-SCREEN-002, SRC-BGA-MAT-SCREEN-001, SRC-BGA-REV3-001]
source_locator: "材料属性截图.docx 的5张原图，按文档顺序image1至image5；不使用未经核实页码"
updated_at: "2026-10-30"
reviewed_by: ""
reviewed_at: ""
---

# BGA 材料定义截图核对

用户提供的5张Engineering Data截图补充了 [revision 3工程提取](bga-20261030-revision3.md) 的界面证据。可见字段与该快照相符；截图没有证明Mechanical材料已刷新或求解已完成，也没有显示可核实的软件发行版本。

## 初次5张截图的覆盖范围（历史记录）

| 原图与材料 | 可确认的定义与字段 | 尚未显示 |
| --- | --- | --- |
| image1：BT | 各向同性瞬时热膨胀系数；各向同性弹性，衍生于E与ν；密度、CTE、E、ν、热导率、比热 | 材料原始出处与方向假设依据 |
| image2：SFL | 各向同性瞬时CTE表格与各向同性弹性表格已存在；密度1890、热导率1、比热0.79 J/(g·K) | 未选中CTE/弹性属性，右侧未展开温度—CTE、温度—E/ν表；本图不能核对其数值 |
| image3：SI | 各向同性瞬时CTE及各向同性弹性；六种基础属性 | 使用各向同性近似的依据 |
| image4：Sn63Pb37 | Anand九参数及参考单位MPa、K、s^-1；E/ν的9点温度表；密度、热导率、比热 | 瞬时CTE属性存在，但右侧未显示其温度表 |
| image5：Underfill | 各向同性瞬时CTE及各向同性弹性；六种基础属性 | 原始出处与温度范围依据 |

## 关键数值与单位

- SFL比热为0.79 J/(g·K)，即790 J/(kg·K)，界面证据与revision 3一致。
- Anand m显示0.303；h0显示2640.8。工程XML为2640.75 MPa，截图显示值与其舍入精度相符，不能据此把原值改成2640.8。
- 焊料E/ν温度轴为−55、−35、−15、5、12、50、75、100、125 ℃。
- BT、SI、Underfill截图中的比热分别为0.92、0.713、0.87 J/(g·K)，焊料为0.128 J/(g·K)，换算至J/(kg·K)需乘1000。

[可见数值转录表](datasets/bga-material-screenshots-draft/visible-values.csv)共51条输入数值，不把软件推导出的体积/剪切模量作为独立输入重复收录。[来源哈希与图片索引](datasets/bga-material-screenshots-draft/source-manifest.json)保留定位；原DOCX与原图未上传仓库。

## 避免误读

SFL、焊料表格属性下面的“比例1、偏移0”是缩放设置，不是E=1 GPa、ν=1或CTE=1。实际值要查看右上方选中属性的完整表格。SFL截图当前选中的是比热，不能从它确认弹性表。

BT、SI、Underfill右上方场变量中的默认温度22 ℃，不是结构分析无应力参考温度的证据。瞬时CTE类型的可见选择也不证明该类型符合原始材料数据定义。

当前未新增材料版本数值，不覆盖revision 3或升级为validated。此前待补的三张材料温度表现已取得，见下文；结构分析参考温度与Mechanical材料实际值仍未确认。

## 后续三张温度表已补齐

用户另行提供的3张截图（SRC-BGA-MAT-SCREEN-002）新增15条温度相关输入的界面证据，均与revision 3快照一致。加上原5张图，现有8张截图、66条输入数值转录；不把温度列或派生模量重复计为独立属性。

| 截图 | 温度 ℃ | 可见输入 |
| --- | --- | --- |
| SFL-elasticity | 25 | E=26 GPa，ν=0.3 |
| SFL-elasticity | 260 | E=0.7 GPa，ν=0.3 |
| SFL-CTE | 25 | 瞬时CTE=8×10⁻⁶ K⁻¹ |
| SFL-CTE | 150 | 瞬时CTE=3.5×10⁻⁵ K⁻¹ |
| Sn63Pb37-CTE | −55、−35、−15、5、12、50、75、100、125 | 瞬时CTE依次为24.1、24.6、25.0、25.2、25.4、26.1、26.8、27.3、27.8 ×10⁻⁶ K⁻¹ |

[补充转录数据](datasets/bga-material-screenshots-draft/supplementary-temperature-tables.csv)与[截图哈希和定位](datasets/bga-material-screenshots-draft/supplementary-source-manifest.json)保留独立来源；原5张图转录表不改写。

此前三项“材料表未展开”的界面资料缺口现已关闭。材料原始来源与类型适用性、温区处理、结构参考温度及Mechanical同步仍未验证。

尤其本案例循环最低−55 ℃，SFL的E与CTE表都从25 ℃起；焊料E/ν/CTE表最高125 ℃，低于循环最高150 ℃。截图已完整显示当前输入表，但不提供这些区间之外的材料数据或求解器实际端点处理证据。不能自动补点、改变CTE类型或认定温区问题已解决。

---
id: KB-COURSE-PACKAGING-20261102-002
title: "叠层与互连阵列的导热方向性"
document_type: knowledge
domain: packaging
status: draft
language: zh-CN
tags: [thermal, anisotropy, substrate]
physics: [thermal, mechanical]
software: []
software_versions: []
source_ids: [SRC-COURSE-CHIP-PACKAGING-03, SRC-COURSE-CHIP-PACKAGING-02]
source_locator: "课件03 p.5–8；补充课件02 p.5–7（PDF文件页码）"
updated_at: "2026-11-02"
reviewed_by: ""
reviewed_at: ""
---

# 叠层与互连阵列的导热方向性

## 为什么同一块基板需要区分方向

连续铜平面能沿板面扩散热量，而穿过板厚时热量还要跨越介质层。过孔会建立局部跨层通路，其空间分布又影响热量是否能有效进入这些通路。因此板面方向与厚度方向的等效导热率通常需要分别描述；两条板面方向也不必相同，例如走线存在明显方向性时。

材料本体导热率与结构等效导热率不是同一个数据。铜的材料属性不能直接赋给含铜的整块基板；同样，把焊球阵列整体当作焊料也丢失了球间介质及面积占比。

## 两个用于理解的理想极限

在各层平整、充分接触、无热源、材料导热率为常数且温度场满足理想一维条件时，沿层面导热可用并联思路，穿过层厚可用串联思路：

- `k_parallel = Σ(fi ki)`。
- `k_perpendicular = 1 / Σ(fi/ki)`。

fi为第i层厚度占比，Σfi=1；ki和结果单位为W/(m·K)。这是对理想层状介质的推导，不是对含离散孔、断续走线或局部热点的普遍拟合公式；界面热阻也未计入。

## 等效数据必须附带哪些证据

记录原始结构范围、坐标轴定义、铜覆盖和连通性、孔/焊球分布、间隙介质、等效方法及验证对象。若等效目标是整体温升，应另行确认能否用于局部焊点温度；整体等效层不保留单球局部应力信息。

课件展示的FR4、焊料及球阵列等效数值没有足够牌号和温度依据，本条不将其登记成推荐材料参数。材料原始数据仍统一维护在shared/materials。

## 来源与审核边界

本条为课程课件的归纳及明确标注的基础推导/项目交接建议，尚待审核；未通过本案例求解验证。阅读范围与原文疑点见[课程阅读笔记](../../common/references/course-41-reading-notes.md)。

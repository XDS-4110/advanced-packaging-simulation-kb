---
id: KB-BGA-REV2-001
title: "BGA 第二次提取：材料修改与剩余问题"
document_type: knowledge
domain: simulation
status: draft
language: zh-CN
tags: [BGA, material-input, revision2, unsolved]
physics: [thermal, structural]
software: [ANSYS Workbench]
software_versions: ["2024 R2"]
source_ids: [SRC-BGA-REV2-001, SRC-BGA-001, SRC-BGA-REPORT-001]
source_locator: "EngineeringData.xml 材料/属性/参数名；journal2.wbjn；文件哈希见提取清单"
updated_at: "2026-10-30"
reviewed_by: ""
reviewed_at: ""
---

# BGA 第二次提取：材料修改与剩余问题

## 当前修订结论

材料保存值已核实：Anand m=0.303、h0=2640.75 MPa，焊料E/ν温度轴与报告一致。SFL比热仍为3305.36 J/(kg·K)，不是报告的790 J/(kg·K)。

完整记录与数据见 [共享材料修订证据](../../../shared/materials/bga-20261030-revision2.md)。原条目中的反向对应和旧温度轴属于revision 1历史，不应作为当前Engineering Data值检索返回；自动化引用须固定来源与修订。

## 提取范围与尚待补充

本轮使用当前EngineeringData.xml和journal2.wbjn交叉核对，没有打开或修改Workbench，也没有运行求解器。当前目录未保留原来可读的CAERep.xml/MatML.xml/ds.dat；Mechanical数据库存在，但未通过软件接口导出本轮设置。

因此不能以本轮检查认定约束、无应力参考温度、温度对象作用域、接触、网格或结构时间步已经核实。也不能确认新材料已刷新进入Mechanical。

## 归档与后续操作

当前BGA.wbpj与材料XML保存于15:49左右；现有BGA.wbpz时间为14:36，且其中材料XML哈希与当前文件不同。该归档不是本次修改版本。

后续应核对比热采用依据；在Workbench刷新/核对Model内材料，再保存工程并重新归档。单纯保存Engineering Data不构成Mechanical同步证据。无需为了知识提取而求解；当前案例仍保留“未求解、未验证”状态，报告结果仍单独记录。

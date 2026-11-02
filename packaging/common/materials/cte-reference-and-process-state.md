---
id: KB-PKG-CTE-REFERENCE-20261102
title: "CTE数据参考温度与封装工艺状态"
document_type: knowledge
domain: packaging
status: draft
language: zh-CN
tags: [CTE, reference-temperature, warpage, material-evidence]
physics: [mechanical, thermal]
software: []
software_versions: []
source_ids: [SRC-COURSE-VIDEO-WARPAGE-CORRECTION, SRC-ANSYS-242-CTE-DEFINITION, SRC-ANSYS-242-THERMAL-EXPANSION]
source_locator: "更正视频00:37–03:10；ANSYS 2024 R2 Linear Material Models及Material Reference §3.5"
updated_at: "2026-11-02"
reviewed_by: ""
reviewed_at: ""
---

# CTE数据参考温度与封装工艺状态

## 一张CTE表为什么还需要参考条件

热膨胀系数CTE描述热应变随温度的关系，但“平均/割线系数”与“瞬时/切线系数”的定义不同。割线系数联系某个共同参考点与当前温度，瞬时系数描述当前温度附近的变化率。因而一列温度和一列CTE并不足以完整定义材料输入，还需说明系数类型、测量基准及材料方向。[ANSYS 2024 R2材料说明](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ans_mat/ansmattherexp.html)区分了这两种输入与直接输入热应变的方式。

Engineering Data中的Zero-Thermal-Strain Reference Temperature与CTE数据的参考基准有关。它不应仅因工艺中出现某个峰值温度就被任意改成该数值；数据定义与模型参考状态不同时，需要一致的转换。参见[2024 R2 Engineering Data说明](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/wb_eda/eda_linear_mat_mdl.html)。

## 从更正视频得到的资料整理要求

课程更正视频00:37–01:40展示并讨论参考温度字段；01:45–03:10转向基板温度相关属性与工艺温度范围。其意义在于：封装侧交付材料时，应同时提交属性曲线的定义和实际工艺温度历程。

视频中的350°C是该演示的字段值，不是BGA或基板的通用参考温度。讲师演示中改变温度节点来讨论属性变化，也不构成目标材料的重新测量数据。不能为得到预期翘曲而改写目标材料的Tg或属性曲线。

## 需要分别登记的事实

| 事实 | 必须伴随的说明 |
| --- | --- |
| 材料CTE曲线 | 牌号、固化/含湿状态、方向、单位、割线或瞬时定义、测量参考点、温区 |
| 弹性或黏弹性数据 | 实验方法、温度与时间/频率条件；不要只保留室温单值 |
| 玻璃化转变温度Tg | 测量方法、取值准则、对应材料状态 |
| 装配工艺温度 | 芯片、基板等部件各自的温度—时间历史及测量位置 |
| 结构参考状态 | 在何时、何种约束和工艺状态下作为计算起点，依据是什么 |

上表是本项目的证据交接建议。材料的零热应变基准并不能单独证明装配件没有残余应力；是否存在固化收缩、界面约束或前序残余变形，需要独立证据。也不能把不同部件都当成经历了同一条温度曲线。

## 适用范围与待验证事项

本条适用于整理BGA、2.5D及其他封装的热机械材料证据，不提供软件操作步骤或推荐数值。材料输入与参考温度的具体映射交由simulation负责人核验；课程使用2020 R2，当前项目基线2024 R2。本条仍为draft，未完成算例复现。

课程观察与尚未确认的部分见[更正视频笔记](../references/course-video-warpage-correction.md)。

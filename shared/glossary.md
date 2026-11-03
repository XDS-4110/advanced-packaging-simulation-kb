---
id: KB-GLOSSARY-001
title: "术语与同义词对照表"
document_type: knowledge
domain: shared
status: draft
language: zh-CN
tags: [glossary, terminology, retrieval, synonym]
physics: [thermal, structural]
software: [ANSYS Workbench, ANSYS Mechanical]
software_versions: []
source_ids: [SRC-BGA-001]
source_locator: "本库各条目正文用词统计；定义不引入新来源"
updated_at: "2026-11-02"
reviewed_by: ""
reviewed_at: ""
---

# 术语与同义词对照表

> 用途有两个：统一正文用词；为检索提供同义词扩展（用户问"翘曲"，文档写 warpage）。
> 定义只做最小说明，不替代各专题条目；不含任何数值。

## 封装结构

| 中文 | 英文/缩写 | 说明 | 常见别名 |
| --- | --- | --- | --- |
| 球栅阵列 | BGA (Ball Grid Array) | 以焊球阵列作外部互连的封装形式 | 焊球阵列、ball array |
| 二维半集成 | 2.5D | 多芯片经中介层互连的集成架构，非封装外形 | 2.5D IC、硅中介层集成 |
| 芯粒 | chiplet | 可独立制造、再集成的裸片单元 | 小芯片、dielet |
| 中介层 | interposer | 芯片与基板之间提供高密度互连的中间层 | 转接板、interposer layer |
| 硅通孔 | TSV (Through-Silicon Via) | 穿过硅衬底的垂直互连；区别于其他衬底通孔 | 硅穿孔 |
| 再布线层 | RDL (Redistribution Layer) | 中介层或晶圆上的薄膜布线层 | 重布线、redistribution |
| 裸片 | die (pl. dice) | 未封装的芯片 | 芯片、晶粒、chip |
| 凸点 | bump | 芯片侧的微互连；尺寸小于焊球 | 微凸点、micro-bump |
| 焊球 | solder ball | 封装底部的外部互连球 | 锡球、solder bump |
| 底填 | underfill | 填充芯片与基板间隙的胶 | 底部填充胶、毛细底填 |
| 塑封料 | EMC / SFL (Epoxy Molding Compound) | 包封用环氧模塑料；本库工程中显示名为 SFL | 封胶、molding compound |
| 基板 | substrate (BT) | 封装内承载芯片的有机基板 | BT 板、载板 |
| 印制板 | PCB | 板级承载与互连 | 电路板 |

## 热与力学

| 中文 | 英文/缩写 | 说明 | 常见别名 |
| --- | --- | --- | --- |
| 翘曲 | warpage | 封装因材料失配产生的面外变形 | 变形、弯曲、warp、out-of-plane |
| 热膨胀系数 | CTE | 温度变化引起的应变率；区分瞬时与割线定义 | 线膨胀系数、α |
| 无应力参考温度 | stress-free / reference temperature | 该温度下结构应变为零 | 参考温度、零应力温度、stress-free temp |
| 玻璃化转变温度 | Tg | 材料模量显著下降的温度 | 玻璃化温度 |
| 粘塑性 | viscoplasticity | 与速率相关的塑性行为；焊料常用 Anand 模型 | 率相关塑性 |
| 蠕变 | creep | 恒定载荷下随时间发展的变形 | 徐变 |
| Anand 模型 | Anand | 焊料粘塑性本构，含九个具名参数 | Anand 本构、统一粘塑性 |
| 热循环 | thermal cycling | 按温度曲线反复升降温 | 温循、TCT |
| 保温段 | dwell | 循环中恒温保持的时段 | 驻留、保持时间 |
| 升降温段 | ramp | 循环中的温度变化段 | 斜坡 |
| 疲劳寿命 | fatigue life | 达到失效判据的循环数 | 寿命、cycles to failure |
| 界面热阻 | thermal interface resistance | 两固体接触面的附加热阻 | 接触热阻、TIM 热阻 |
| 导热界面材料 | TIM | 填充界面间隙以提高导热 | 导热垫、导热膏 |

## 仿真与流程

| 中文 | 英文/缩写 | 说明 | 常见别名 |
| --- | --- | --- | --- |
| 顺序耦合 | sequential coupling | 先热后结构，传递温度场 | 热-力顺序耦合、one-way coupling |
| 导入体温度 | Imported Body Temperature | 把热分析结果作为结构分析的体载荷 | 温度导入、imported load |
| 命名选择 | Named Selection | 命名的几何集合，供边界与接触引用 | 选择组、NS |
| 接触对 | contact pair | 源面与目标面的接触定义 | contact region |
| 绑定接触 | bonded | 界面不分离、不滑移的约束 | tie、绑定 |
| 分析步 | analysis step / load step | 载荷历程的分段 | 载荷步、step |
| 子步 | substep | 步内的求解增量 | 时间增量 |
| 收敛 | convergence | 迭代满足残差判据 | 收敛性 |
| 网格无关性 | mesh independence | 结果对网格加密不敏感 | 网格收敛、敏感性 |
| 试验设计 | DOE | 系统性采样设计空间 | 参数扫描、试验矩阵 |
| 代理模型 | surrogate model | 用少量仿真拟合的近似模型 | 响应面、Kriging、元模型 |
| 灵敏度 | sensitivity | 输出对输入的敏感程度 | 影响因子 |

## 标准与规范

| 中文 | 英文/缩写 | 说明 | 常见别名 |
| --- | --- | --- | --- |
| GJB 548C—2021 | — | 本工程采用的温循方法依据，方法 1010.1 | 国军标、548C |
| JEDEC | JEDEC | 封装可靠性常用标准体系 | — |

## 使用约定

1. 正文优先用"中文（英文缩写）"，首次出现给全称。
2. 检索时同义词全列等价，不做优先级排序。
3. 术语定义不引入数值；涉及具体参数的，引用对应材料或案例条目。

## 待补充

- 新增术语需同时补"本库出现位置"；
- 英文缩写与 ANSYS 界面用词的对应（如 SFL 与 EMC）需在实际界面核对后确认。

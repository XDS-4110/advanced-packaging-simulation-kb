---
id: KB-ANSYS242-PYMECH-THERMOSTRUCT-01
title: "PyMechanical热结构耦合：脚本接口与运行模式"
document_type: software_operation
domain: simulation
status: reviewed
language: zh-CN
tags: [PyMechanical, thermal-structural, temperature-transfer, scripting, execution-mode]
physics: [thermal, structural]
software: [ANSYS Mechanical, PyMechanical]
software_versions: ["2024 R2"]
source_ids: [SRC-ANSYS-242-OPS-API, SRC-ANSYS-THERMOMECH-WORKFLOW, SRC-PYMECH-GUIDANCE-001, SRC-PYMECH-IMPORTLOAD-998]
source_locator: "下文固定提交的函数/段落与issue评论；筛选范围、哈希见data/pymechanical-coupling-selection.json"
updated_at: "2026-11-02"
reviewed_by: "Codex（来源与版本条件核对；未连接ANSYS执行）"
reviewed_at: "2026-11-02"
verification_scope: "官方代码/文档提炼与历史问题核查；非2024 R2运行验证"
---

# PyMechanical热结构耦合：脚本接口与运行模式

用于回答“如何把热结构步骤转为PyMechanical调用”。总体流程沿用[温度传递与结构设置](05-temperature-transfer-structure.md)，不重复材料、网格与案例参数。这里讨论热结果→结构载荷的顺序耦合，不表示同时求解热/位移自由度的直接耦合。

## 先确认脚本在哪里执行

| 场景 | 可复用内容 | 需要适配的部分 |
| --- | --- | --- |
| 外部Python控制远程Mechanical | 外层客户端把脚本交给`mechanical.run_python_script(...)`，脚本体内访问`Model`、`DataModel`、`ExtAPI` | 文件路径以Mechanical主机为准；记录实际会话、软件与客户端版本 |
| 已有MCP工具接收Mechanical脚本体 | 提交上述脚本体 | 不在脚本体里再次启动`App()`或嵌套客户端调用；工具名称/签名须以你们实际服务为准 |
| 嵌入模式`App` | 底层Model API可作为参考 | `App/globals`初始化与远程模式不同；温度导入另见下文历史版本条件 |

外部CPython不会因已连接Mechanical就自动拥有`ExtAPI`。最新官方MCP的`describe_api`、`check_script`等仅是能力参考，不能假定你们现有服务已实现。项目不因本条目而更换连接架构或升级依赖。

来源：[官方嵌入模式说明](https://github.com/ansys/pymechanical/blob/ddcaf8256b8035e7a534cdca3b5b8b34b808f215/doc/source/user_guide/embedding/overview.rst)；[官方MCP guidance](https://github.com/ansys/pymechanical-mcp/blob/c6e3a5522da7d4fe5af2bb583f6821df6838689c/src/ansys/mechanical/mcp/contexts.py)的workflow/general函数。MCP固定提交包含更新版本提示，不能将它的全部示例视作2024 R2兼容脚本。

## 从官方示例保留的耦合API线索

下表是接口索引，**不是可直接执行的完整脚本**。`thermal`、`structural`、`imported_temperature`都表示已经核实身份的当前对象；实际参数、作用域和签名需回读/核对。

| 步骤 | 保留的API线索 | 使用条件/检查 |
| --- | --- | --- |
| 建立热分析 | `Model.AddTransientThermalAnalysis()` | 优先复用已有目标分析，避免重跑时重复创建 |
| 设置时间 | `thermal.AnalysisSettings.NumberOfSteps`、`SetStepEndTime(step, Quantity(...))` | 按实际逐步结束时间设置；不复制示例14步和720 s |
| 设置温循 | `thermal.AddTemperature()`、`Location`、`Magnitude.Inputs[0].DiscreteValues`、`Magnitude.Output.DiscreteValues` | 输入为时间、输出为温度；单位与点数对应；初温另核对 |
| 建立结构分析 | `Model.AddStaticStructuralAnalysis()`或`AddTransientStructuralAnalysis()` | 来源演示前者；后者的时间积分/惯性设置须另行验证 |
| 建立热载荷关联 | `structural.ImportLoad(thermal)` | 不假定返回值就是温度对象；调用后检查新建对象与源热分析关系 |
| 设置时间映射 | `imported_temperature.GetTableByName("Source Time")` | 来源示例用两列对应源/分析时间；当前对象列含义、顺序和实际保存时刻须核对，不能盲抄列号 |
| 导入实际温度 | `imported_temperature.ImportLoad()` | 热结果已存在，并检查目标覆盖、源/目标时刻及温度抽样 |
| 设置结果 | `Solution.AddTemperature()`；结构端`AddTotalDeformation()`、`AddEquivalentStress()`、`AddEquivalentPlasticStrain()`、`AddThermalStrain()`；结果`DisplayTime` | 分别用于适用分析；非线性应变指标取决于本构及可用结果。总变形不自动等于翘曲 |
| 求解/确认状态 | `Solution.Solve(True)`、`Solution.Status` | 仅在任务要求求解时使用；完成状态与日志、物理验收分开检查 |

API来源：[官方workflow](https://github.com/ansys/pyansys-workflows/blob/20647415eef62c71fdea3fc5a5e56abd5295dcf8/fluent-mechanical/wf_fm_02_mechanical.py)的Setup transient thermal、Setup Structural Analysis、Solve and post-process段；创建/时间控制/导入字段另与[既有v242 API记录](data/source-selection.json)核对。官方workflow的模型与CFD边界不用于封装默认值。

温循行由v242的Temperature字段与官方MCP的boundary_conditions示例归纳；workflow中的时变离散表实际用于对流字段，并未演示本项目Temperature温循表。字段类型可作接口线索，实际时间表仍须在242回读和测试。

原示例中`Model.Analyses[0]/[1]`、英文对象名第一个匹配及`Children[n]`依赖树顺序。实际自动化应记录目标分析ID和类型，检查同名对象唯一性、选择集合非空；树对象ID不等于CAD面ID。新增、删除或重导入后重新定位对象，避免旧标识继续作用于错误对象。

## 2024 R2需要保留的历史问题

[PyMechanical issue #998](https://github.com/ansys/pymechanical/issues/998)报告：热→静力的`ImportLoad`在嵌入模式失败，作者称批处理Mechanical脚本可运行。维护者于[2025-01-02](https://github.com/ansys/pymechanical/issues/998#issuecomment-2567876008)提出嵌入初始化使用`AddinConfiguration("WorkBench")`的临时方式，另于[2025-07-17](https://github.com/ansys/pymechanical/issues/998#issuecomment-3084944953)说明2025 R2已修复。

这是历史维护记录，不是本项目复现结论，也未给出覆盖所有旧版本/连接模式的保证。不能据issue关闭推断2024 R2已有修复；也不能把嵌入问题直接判为你们gRPC远程模式故障。仅在相同模式出现相同问题时参考，保留报错及版本交由连接负责人验证；不把临时初始化配置加入通用前处理脚本。

## 每个调用阶段应返回什么

返回目标分析ID/类型、Mechanical版本/执行模式、载荷对象ID与作用域、完整时刻映射及状态/报错。完成热求解、完成温度导入、完成结构求解分别记录；没有实际热结果只能交付连接配置。物理边界、网格验收和翘曲定义继续引用[既有操作集](README.md)，不由此API索引生成默认值。

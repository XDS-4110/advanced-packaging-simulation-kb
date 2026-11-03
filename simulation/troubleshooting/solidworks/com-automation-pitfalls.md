---
id: KB-TS-SWCOM-001
title: "SolidWorks COM 自动化：接口、状态与单位问题"
document_type: troubleshooting
domain: simulation
status: draft
scope: general
scope_note: "实测环境 SolidWorks 2024 SP0.1 + pywin32 + Windows 10；不同版本的行为需复核。"
language: zh-CN
tags: [solidworks, com, pywin32, mcp, troubleshooting]
physics: []
software: [SOLIDWORKS]
software_versions: ["2024 SP0.1"]
source_ids: [SRC-SW-COM-LAB-001]
source_locator: "2026-11-03 本机实测记录；现象与返回码见各条"
updated_at: "2026-11-03"
reviewed_by: ""
reviewed_at: ""
---

# SolidWorks COM 自动化：接口、状态与单位问题

> 全部为本机实测。每条给"现象 → 原因 → 处理"，不涉及具体模型参数。

## 1. GetActiveObject 连接失败

**现象**：`win32com.client.GetActiveObject("SldWorks.Application")` 抛 `(-2147221021, '操作无法使用')`，但 SolidWorks 明明在运行。

**原因**：该实例可能是由已退出的宿主进程创建，或未在 ROT 中按预期注册。

**处理**：改用 `win32com.client.Dispatch("SldWorks.Application")`。SolidWorks 是单实例应用，Dispatch 会返回已在运行的那个实例，并可直接读 `ActiveDoc`。

**不要**因为 GetActiveObject 失败就判断"SolidWorks 没开"。

## 2. 晚绑定调不到部分方法

**现象**：`feature.GetDefinition()` 报 `(-2147352573, '找不到成员')`；`gencache.EnsureDispatch` 报 `(-2147319765, '找不到元素')`。

**原因**：SolidWorks 的不少接口只走 vtable，pywin32 的 IDispatch 晚绑定无法调用；类型库也未按 EnsureDispatch 的默认方式暴露。

**处理**：
- 优先使用**有 dual 接口**的方法（如 `ModelDoc2.Parameter(name)`、`Dimension.SystemValue`、`EditRebuild3` 可用）；
- 需要 vtable-only 方法时，改用官方提供的 C#/COM 互操作层（例如 MCP 执行服务），不要在 Python 侧硬拼；
- 不要用"读特征定义"的方式取参数，直接用尺寸名访问尺寸对象。

## 3. 装配体中的组件读不到特征

**现象**：打开装配体后，组件的 `GetModelDoc2` 可用，但特征对象的方法全部报错或返回空。

**原因**：组件以**轻量化**方式加载，特征树未完全实例化。

**处理**：`doc.ResolveAllLightWeightComponents(True)` 后再访问；仍不稳定时，改为**直接打开零件文档**（顶层文档，不做为组件）再读取。

## 4. EditRebuild3 加括号报错

**现象**：`doc.EditRebuild3()` 抛 `'bool' object is not callable`。

**原因**：晚绑定下该成员被解析为属性/布尔，而非可调用方法。

**处理**：按属性方式取用，或退回 `doc.ForceRebuild3(False)`。重建后检查 `doc.Extension.NeedsRebuild2 == 0` 作为成功判据。

## 5. 尺寸值单位是米

**现象**：把 0.35 mm 写成 `SystemValue = 0.35`，模型变成 350 米厚，且**不报错**。

**原因**：`Dimension.SystemValue` 使用米；界面显示用毫米。

**处理**：写入前统一换算并以米为单位；读取后同样按米解释。此类错误不会触发任何警告，必须靠回读数值判断。

## 6. 通过 MCP 打开文档被拒

**现象**：`connect` 返回 ok，但打开文档返回 `SW_INSTANCE_NOT_READY`（"已有实例尚不可连接，已阻止重复启动"）。

**原因**：执行层在 attach 前检查实例状态；用户存在模态对话框、处于草图/特征编辑状态、或实例刚启动未就绪时都会拒绝。

**处理**：
- 先让 SolidWorks 回到空闲（关闭对话框、退出编辑）；
- 必要时完全退出 SolidWorks，由执行层重新启动一个实例；
- 该错误 `retryable=false`，重复同一调用不会自愈，必须改变状态或换路径（例如用 COM 直接处理已打开的活动文档）。

## 7. MCP 工具集不含尺寸枚举

**现象**：40 多个工具中没有"列出尺寸/特征参数"的能力，只能按**精确尺寸名**更新。

**原因**：工具集面向"构建与校验"，不做模型探查。

**处理**：尺寸名从界面获取（双击尺寸后，修改框中显示 `D1@特征名`），或由建模规范在建模阶段就固定命名；不要期望自动发现。

## 8. 尺寸名规则

格式为 `D<序号>@<特征名>`。特征名为中文界面下的本地化名称（如 `凸台-拉伸1`）时，尺寸名同样是中文，例如 `D1@凸台-拉伸1`；写成英文 `D1@Boss-Extrude1` 会**找不到**。跨语言环境共享模型时，这一点会导致自动化脚本失效。

## 判据

修复是否成立，用三条判断：

1. 操作返回码为成功；
2. 回读数值与预期一致（注意单位）；
3. `NeedsRebuild2 == 0` 或等效的重建完成标志。

只有第 1 条通过时不算修复。

## 待补充

- 2026/2025 版本的接口差异；
- 装配体级阵列参数是否可通过 COM 修改；
- 中文特征名在英文版 SolidWorks 下的对应关系。

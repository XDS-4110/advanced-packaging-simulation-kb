---
id: KB-TOOLS-UNRESOLVED-001
title: "执行契约骨架未决绑定与人工确认"
document_type: execution_contract
domain: shared
status: draft
language: zh-CN
software: [ANSYS Workbench, ANSYS Mechanical, PyMechanical]
software_versions: ["2024 R2"]
source_ids: [SRC-EXEC-CONTRACT-USER-001, SRC-EXEC-MECH-V242-001, SRC-EXEC-ENGDATA-V242-001, SRC-EXEC-JSONSCHEMA-202012]
source_locator: "本会话要求；tools.schema.json的x-contract.api_evidence及正文定位"
updated_at: "2026-11-02"
reviewed_by: ""
reviewed_at: ""
---

# 未对齐绑定与人工确认清单

当前所有工具绑定均为`unresolved`且执行禁用；官方页面有字段不代表项目适配器已实现。下表仅写卡点与关闭所需证据，没有替用户决定任何物理条件。关闭某个卡点也不自动提升本文draft状态；审核人/日期继续留空。

| 编号 | 影响范围 | 卡点 | 谁补充什么才能关闭 |
| --- | --- | --- | --- |
| U-RUNTIME | 全局 | ansys-mechanical-core确切版本、Workbench脚本入口/工程与Mechanical会话归属待确认。 | 连接负责人提供包版本与所连242会话/工程身份；只读回读记录可追溯。 |
| U-STABLE-ID | 两层resolve_entity | 项目stable_id不是官方原生ID；名称、树ID与CAD ID不能互换，几何更新后的映射规则尚未实现。 | 模型负责人提供实体清单/模型修订；连接负责人给出来源到真实对象的解析和歧义/失效处理证据。 |
| U-READBACK | 两层read_property及所有写入 | 通用属性键、温度表行列、来源字段、单位和比较容差未细化。 | 逐类对照v242字段；材料/模型负责人确认属性语义；执行端提供只读回读结果。 |
| U-PARAMETERS | workbench_project.list_parameters | 未找到已确认的v242工程参数枚举绑定；Engineering Data页面不是参数集API依据。用户说明当前STEP模型没有参数集，仍不能伪造一次成功枚举。 | 连接负责人提供Workbench参数查询入口或明确的无参数查询证据；绑定前返回unresolved。 |
| U-MATERIAL-REVISION | Engineering Data物性修改及Mechanical材料赋值 | 材料ID/revision到软件材料的映射、新revision创建和旧revision不可覆盖校验未实现；不能仅回读Body.Material名称就确认revision。 | 材料负责人确认ID/revision登记方式；连接负责人分别证明Engineering Data新版本快照与Mechanical显式切换的回读。 |
| U-GEOMETRY-IMPORT | mechanical.reimport_geometry | 文档有GeometryImport.Import；WBPJ几何单元关联、完整替换/刷新、材料与命名选择保留行为未核实。 | 模型负责人提供修改后文件及修订/单位；连接负责人验证工程归属、实际导入对象和失效清单，不能只在独立会话另建模型。 |
| U-GEOMETRY-TRANSFORM | mechanical.transform_entity | 尚未对上能修改当前导入实体位置/变换的v242 API；不把显示旋转或相机变换当CAD修改。 | 连接负责人提供官方242绑定或可审计的替代层；模型负责人确认坐标系与变换语义。在此之前禁用。 |
| U-GEOMETRY-PARAMETER | workbench_project.set_geometry_parameter | 当前STEP导入无Workbench参数名/参数集，也未提供SpaceClaim/DesignModeler参数化后端；没有可绑定的尺寸参数。 | 阶段二再评估参数化方案与官方API；实际参数名、单位及实体对应关系给出前持续unresolved。 |
| U-FIELD-TABLES | 对流、温度 | 已读到分析对象创建入口；系数、绝对温度与时变字段的完整绑定、作用域及单位转换未细化。 | 逐字段核对v242；模型负责人提供实际边界证据；连接负责人回读完整表与范围，不填默认环境温度或系数。 |
| U-CONSTRAINT | mechanical.apply_constraint | Fixed Support/Displacement创建入口有文档；分量自由/给定、方向与坐标系、支撑实际面尚未确认。其余kind为pending。 | 模型负责人在结构树/Details导出真实对象和作用域；连接负责人核对分量字段。不得默认全固定或补零。 |
| U-ANALYSIS-STEP | mechanical.add_analysis_step | 步数/结束时间有字段依据；增加步骤时原有逐步设置如何保留、时间积分与蠕变依赖尚未绑定。 | 连接负责人逐步回读设置；模型负责人确认物理时间历程，不自行生成时间步或继承当前选中步。 |
| U-RETRY | 创建对象/追加分析步/导出等写工具 | idempotent均为null；去重键、重复请求处理、部分写入恢复及输出覆盖策略未定义。 | 先明确更新/创建语义、request_id持久化记录及失败恢复条件，再逐工具判定；此前禁止自动重试。 |
| U-SAVE | 所有模型写入 | requires_save=true是项目验收条件；WBPJ保存和再次打开的官方绑定及证据结构未核实。Mechanical会话保存不能替代它。 | 连接负责人提供Workbench保存/工程路径/修订回读证据；当前不能宣称持久化成功。 |
| U-EXPORT | mechanical.export_results | 多时刻CSV含范围/极值/单位的封装、PNG、支反力及可选rst/npz绑定未确认；UZ坐标系和翘曲参考平面留空。 | 模型负责人确定结果范围、时刻与评价定义；连接负责人证明结果非过期、导出文件与元数据对应；未求解工程不能提供真实结果。 |
| U-UNITS | 全部数值字段 | 内部SI及绝对温度/温差区分已按用户要求声明；换算适配器、数值精度与比较容差留null。 | 细化阶段提供单位定义/转换依据及可审计比对规则；没有容差依据不能自动放宽或用常见值补齐。 |

## 当前人工对象清单

工程/系统与会话身份、实体stable_id映射、材料ID/revision与软件材料对应、几何文件修订、变换坐标系、温度/对流作用面、结构支撑面、各步时间设置、结果作用域和UZ方向坐标系均待提供或回读。这里不将BGA截图中的名字/ID自动填入新工具。

## API依据的边界

SRC-EXEC-MECH-V242-001与SRC-EXEC-ENGDATA-V242-001的精确URL/字段定位见[骨架](tools.schema.json)的`x-contract.api_evidence`，其catalog notes均为“仅字段/定义依据，不证明可执行”。未找到API的变换、参数集枚举与尺寸参数化，`adapter_method`保持null；不得从需求工具名猜出同名官方方法。SRC-EXEC-CONTRACT-USER-001仅提供项目要求，不能充当软件接口证据。

本轮没有ANSYS环境，未执行写入、回读、保存、求解或结果导出；也未解析任何Git LFS PDF正文。静态schema检查与上述运行证据分开记录。下一步只在用户确认骨架后细化第一阶段工具；阶段二与阶段三继续等待各自确认。

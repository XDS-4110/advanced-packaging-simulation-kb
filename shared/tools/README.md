---
id: KB-TOOLS-README-001
title: "执行契约骨架使用边界"
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

# 执行契约骨架：第一阶段审阅件

本目录是“规范加证据”，没有执行器、仿真脚本或已验证结果。当前只交付第一阶段骨架；审阅确认前不补全各工具的值类型/细节，也不修改结构输入模板或BGA取证文件。全部条目为draft，`software_version: null`等待用户提供ansys-mechanical-core确切版本；软件基线单独记录为Mechanical 2024 R2/v242。

[契约骨架](tools.schema.json)定义预览请求的形状；[未决清单](unresolved.md)集中记录API与人工取证卡点。源码中没有可调用适配器。所有工具`execution_enabled: false`；请求仅接受`execution_mode: preview_only`，各工具arguments暂时只接受null。示例用来审查字段，不是有效的仿真输入。

## 两套工具的边界

| 工具集 | 当前骨架 | 边界 |
| --- | --- | --- |
| Workbench脚本层 | `engineering_data.resolve_entity`、`engineering_data.read_property`、`engineering_data.update_material_properties` | Engineering Data材料读写单独命名；不由PyMechanical硬做 |
| Workbench工程子域 | `workbench_project.list_parameters`、`workbench_project.set_geometry_parameter` | 与材料函数分开；参数查询和后续参数化属于工程入口；参数化当前unresolved |
| Mechanical会话层 | `mechanical.resolve_entity`、`mechanical.read_property`、材料赋值、几何重导入/变换、边界与约束、分析步、结果导出 | 不修改Engineering Data物性表，不把会话保存当作WBPJ工程保存 |

这里仍是两个执行后端；Workbench层内的Engineering Data和工程子域分开命名。`resolve_entity`、`read_property`、`list_parameters`均为只读工具；材料定位/回读与Mechanical定位/回读分属各自层，不使用混合函数。读取工具也需后续适配与验证，不能因只读就视为已有实现。

## 骨架目前定义到哪里

每个工具保留参数名、最小调用示例、API文档线索、未决项引用以及`preconditions`、`readback`、`failure_handling`槽位。这三个槽位目前为null；共同门槛、失败码及生命周期在`x-contract`集中表达，具体工具细节等待骨架审阅后补充。

写工具额外提供：

- `idempotent`：目前全部null，表示重试安全性未知，不能自动重试；后续必须说明前提及如何避免重复创建对象。
- `requires_save`：模型写入为true，结果文件导出为false。这是项目持久化验收要求，不是关于软件属性即时生效时刻的API结论。保存接口尚未绑定。
- `invalidates`：列出后续必须重新检查或重建的对象；只声明项目依赖关系，不声称软件自动执行了重建。几何变更特别包括stable_id映射、命名选择和温度作用域。

JSON Schema验证的是骨架预览请求的结构，`x-contract`是配套的项目语义声明，不会由JSON Schema自动执行。通过静态验证不代表通过单位换算、实体解析、数值比对、持久化或ANSYS验证。

## 单位、实体与材料

全局单位规则位于`x-contract.units`：内部统一SI，仅在输入/输出边界换算；绝对温度与温差必须有不同语义标签，不能对温差施加绝对温度偏移。换算适配器和比较容差均为null，未给出任何工程数值或经验容差。

实体引用以项目`stable_id`为主键，显示名仅作提示。每个引用都包含`resolved_from`，记录命名选择、参数表、CAD导入或人工映射的来源及证据。Mechanical树ID、几何体ID与面ID分别记录，不相互替代；它们均绑定模型修订。当前null只表示未知；不得由LLM临时把名称当stable_id，或自动填入旧案例ID。

材料必须以ID与revision共同引用。物性修改产生同一材料ID的新revision，旧revision及既有引用保持不变，直到独立的实体材料切换操作明确执行。`Body.Material`只证明软件提供材料赋值字段，不提供本项目revision制度；revision与实际软件材料之间的映射保持unresolved。

## 已确定的范围，尚未实现的绑定

- 当前BGA为STEP导入，没有参数集；重导入与已有实体位置/变换是第一版意图范围。两者均未验证，尤其实体变换API仍未对上；尺寸参数化保留到阶段二评估，不猜方法。
- 约束第一版只细化Fixed Support与分量Displacement。其他枚举在`constraint_kinds`中标pending，不给实现。未指定的位移分量不得默认为零；自由/给定及坐标系待细化。
- 结果要求保留温度场多个时刻、等效应力、等效塑性应变、方向位移UZ及支反力。CSV需含作用域、时刻、极值、单位，并配PNG；rst/npz只作可选待定项。CSV封装和全场导出没有已确认绑定；UZ方向坐标系和翘曲参考平面留null，UZ本身不等于已定义翘曲。
- 阶段三将原结构侧第二项拆为支撑对象、接触配置、无应力参考温度三条独立证据；Body.ReferenceTemperature与Analysis Settings来源分别取证。本轮只记录后续范围，不提前编写或关闭证据。

## 最小调用示例与错误处理

每个工具的最小示例位于`x-contract.tools.<工具名>.example`。工程值、ID、位移/温度/时间、软件包版本和来源实例全部留null，未填真实案例值；工具名与`preview_only`仅是协议标记。

任何未解析绑定、未知必需值、失效引用、单位不明或revision不一致均阻止写入。后续回读不一致、部分写入、保存未确认、导出未确认分别报告，不能合并成“成功”。不自动回滚、不自动重试，不把Transaction当持久化或回滚。当前这些都是契约要求，不是已经实现的检查器。

## 来源与检索边界

- SRC-EXEC-CONTRACT-USER-001：本会话批准的范围、用户补充要求与执行端说明；工具名称、SI与revision制度都是项目设计，不宣称是ANSYS原生API。
- SRC-EXEC-MECH-V242-001：[Model](https://scripting.mechanical.docs.pyansys.com/version/stable/api/ansys/mechanical/stubs/v242/Ansys/ACT/Automation/Mechanical/Model.html)、[Body](https://scripting.mechanical.docs.pyansys.com/version/stable/api/ansys/mechanical/stubs/v242/Ansys/ACT/Automation/Mechanical/Body.html)等v242类/字段；各条精确页面及定位见`x-contract.api_evidence`。仅字段/定义依据，不证明可执行。
- SRC-EXEC-ENGDATA-V242-001：[Engineering Data](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/wb2_js/ContainerName37.html)，定位GetMaterials、GetMaterial、CreateMaterial。仅字段/定义依据，不证明可执行；不把按名称查找等同于stable_id/revision解析。
- SRC-EXEC-JSONSCHEMA-202012：[JSON Schema Core](https://json-schema.org/draft/2020-12/json-schema-core)，仅结构校验规范。

来源先登记于[catalog.csv](../references/catalog.csv)，再在本目录引用。依照仓库RAG规范，本目录、README及draft条目不进入默认领域检索；后续执行端应显式读取契约。本轮不修改RAG索引范围，也不读取files中的PDF指针。

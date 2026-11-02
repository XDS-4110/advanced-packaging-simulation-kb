---
id: KB-TOOLS-README-001
title: "执行契约骨架使用边界"
document_type: execution_contract
domain: shared
status: draft
language: zh-CN
software: [ANSYS Workbench, ANSYS Mechanical, PyMechanical]
software_versions: ["2024 R2"]
source_ids: [SRC-EXEC-CONTRACT-USER-001, SRC-ANSYS-242-OPS-API, SRC-ANSYS-242-ENGDATA, SRC-EXEC-JSONSCHEMA-202012]
source_locator: "本会话要求；tools.schema.json的x-contract.api_evidence及正文定位"
updated_at: "2026-11-02"
reviewed_by: ""
reviewed_at: ""
---

# 执行契约骨架：第一阶段审阅件

本目录是“规范加证据”，没有执行器、仿真脚本或已验证结果。当前为第一阶段参数值类型与语义审阅件；未绑定适配器方法，未实施仿真操作，本轮开始补结构输入模板的entity_ref与校验段，BGA结构侧取证文件尚未修改。全部条目为draft，`software_version: null`等待用户提供ansys-mechanical-core确切版本；软件基线单独记录为Mechanical 2024 R2/v242。

[契约骨架](tools.schema.json)定义预览请求的形状；[未决清单](unresolved.md)集中记录API与人工取证卡点。源码中没有可调用适配器。所有工具`execution_enabled: false`；请求仅接受`execution_mode: preview_only`，各工具arguments暂时只接受null。示例用来审查字段，不是有效的仿真输入。

## 两套工具的边界

| 工具集 | 当前骨架 | 边界 |
| --- | --- | --- |
| Workbench脚本层 | `engineering_data.resolve_entity`、`engineering_data.read_property`、`engineering_data.update_material_properties` | Engineering Data材料读写单独命名；不由PyMechanical硬做 |
| Workbench工程子域 | `workbench_project.list_parameters`、`workbench_project.set_geometry_parameter` | 与材料函数分开；参数查询和后续参数化属于工程入口；参数化当前unresolved |
| Mechanical会话层 | `mechanical.resolve_entity`、`mechanical.read_property`、材料赋值、几何重导入/变换、边界与约束、分析步、结果导出 | 不修改Engineering Data物性表，不把会话保存当作WBPJ工程保存 |

这里仍是两个执行后端；Workbench层内的Engineering Data和工程子域分开命名。`resolve_entity`、`read_property`、`list_parameters`均为只读工具；材料定位/回读与Mechanical定位/回读分属各自层，不使用混合函数。读取工具也需后续适配与验证，不能因只读就视为已有实现。

## 骨架目前定义到哪里

每个工具保留参数名、最小调用示例、API文档线索、未决项引用以及`preconditions`、`readback`、`failure_handling`槽位。这三个槽位已分别填为gate ID数组、回读字段名数组与失败码枚举数组，并由`$defs.tool_contract_slots`校验。各ID/字段定义集中于`gate_registry`、`readback_field_registry`和`failure_policy.codes`；它们是项目协议名称，不是ANSYS属性名。15个工具的值类型与逐字段语义已在argument_schema_ref和parameter_semantics中补齐；适配器仍待执行端版本及运行取证。

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

每个工具的最小示例位于`x-contract.tools.<工具名>.example`。工程值、实体ID、位移/温度/时间、软件包版本和来源实例全部留null；request_id使用字符串占位符，未填真实案例值；工具名与`preview_only`仅是协议标记。

任何未解析绑定、未知必需值、失效引用、单位不明或revision不一致均阻止写入。后续回读不一致、部分写入、保存未确认、导出未确认分别报告，不能合并成“成功”。不自动回滚、不自动重试，不把Transaction当持久化或回滚。当前这些都是契约要求，不是已经实现的检查器。

## 来源与检索边界

- SRC-EXEC-CONTRACT-USER-001：本会话批准的范围、用户补充要求与执行端说明；工具名称、SI与revision制度都是项目设计，不宣称是ANSYS原生API。
- SRC-ANSYS-242-OPS-API：[Model](https://scripting.mechanical.docs.pyansys.com/version/stable/api/ansys/mechanical/stubs/v242/Ansys/ACT/Automation/Mechanical/Model.html)、[Body](https://scripting.mechanical.docs.pyansys.com/version/stable/api/ansys/mechanical/stubs/v242/Ansys/ACT/Automation/Mechanical/Body.html)等v242类/字段；各条精确页面及定位见`x-contract.api_evidence`。仅字段/定义依据，不证明可执行。
- SRC-ANSYS-242-ENGDATA：[Engineering Data](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/wb2_js/ContainerName37.html)，定位GetMaterials、GetMaterial、CreateMaterial。仅字段/定义依据，不证明可执行；不把按名称查找等同于stable_id/revision解析。
- SRC-EXEC-JSONSCHEMA-202012：[JSON Schema Core](https://json-schema.org/draft/2020-12/json-schema-core)，仅结构校验规范。

来源登记于[catalog.csv](../references/catalog.csv)。原骨架新建的重复API来源已删除，改为复用SRC-ANSYS-242-OPS-API与SRC-ANSYS-242-ENGDATA，既有来源状态未修改；本契约始终是draft，不能从来源reviewed推导为可执行。依照仓库RAG规范，本目录、README及draft条目不进入默认领域检索；后续执行端应显式读取契约。本轮不修改RAG索引范围，也不读取files中的PDF指针。

## 契约身份、引用与版本

`$id`为`urn:advanced-packaging-simulation-kb:tools:0.1.0`，`x-contract.contract_version`为`0.1.0`，这是用户指定的协议版本，不是材料/工程数值。URN是契约身份，不是下载地址。执行端应将仓库中的该文件注册到此URI，2.5D等引用方用`$ref: urn:advanced-packaging-simulation-kb:tools:0.1.0#/$defs/entity_ref`引用；校验脚本实际检查离线跨文档解析，没有复制定义。

0.1.0在PR #1 squash合并并建立contract-0.1.0标签后冻结；标签指向该合并提交。标签建立前的分支审阅修订由Git提交区分，建立后同一$id内容不再原地修订；破坏性变化在0.x阶段升次版本，稳定版以后升主版本；兼容新增升次版本，仅说明变化升修订版本。版本变化同步更新$id，引用方显式升级；不使用latest。另有强制规则：preview_only变为允许执行（含执行开关false→true）必须升contract_version次版本并同步改$id；无论是否发布，同一0.1.0不得有两种执行行为。规则见`x-contract.versioning`。

## request_id与作用域

`request_id`是日志去重主键。每个写请求都必须非空；在任何模型修改/文件导出前先原子占位并持久化工具、契约版本、项目、预期修订及完整请求指纹。相同ID且指纹相同的已完成请求只返回原回执；不同载荷拒绝，在途请求不重复派发。部分写入或断线后的未知状态必须先核对日志与工程，不自动重试，也不换ID绕过未决状态。这是契约要求，日志存储、指纹与恢复实现仍未绑定，U-RETRY未关闭，idempotent仍为null。

请求新增`scope_kind`：entity要求实体引用；project要求target为null并从context识别工程；analysis允许target为null或分析对象引用，实际分析由analysis_ref确定。list_parameters采用project，export_results采用analysis；预览null不表示选择全部实体。示例仍只接受null工程参数。

## 参数类型与预览边界

每个工具的`argument_schema_ref`指向独立参数schema，`parameter_semantics`解释各字段。新增共享类型覆盖材料标识/revision、带来源SI量、温度/对流时间表、物性表、STEP文件引用与导入意图、真实变换、位移分量、分析步控制和结果导出。所有参数都有类型与语义；null仍表示未知。工程示例没有填任何非null数值。

当前请求`arguments`通过allOf同时接受类型检查与全null预览限制，所以“arguments含非null”原反例仍必须被拒。参数类型可以通过独立$ref作静态检查；不会据此开启派发。三类target规则直接写入每个oneOf分支：entity必须entity_ref，project必须null，analysis为entity_ref或null；缺失target也不通过。

单位采用内部SI；绝对温度与温差分类型。一般物性单位的量纲、换算、温度表坐标匹配、插值实现、时间单调性以及新旧revision比较属于仍未实现的语义门槛，不把JSON类型通过当作这些检查已完成。新增对象中的键是项目协议字段，不是猜测的ANSYS方法或枚举。适配器方法名及ansys-mechanical-core版本继续为null。

## 可复跑静态校验

从仓库根目录执行：`python shared/tools/validate_contract.py`。

校验器为python-jsonschema 4.26.0 / Draft202012Validator；缺少依赖时需要访问PyPI安装该固定版本，或预先从可访问环境取得对应wheel及依赖、使用内网镜像。无法取得依赖时，等价子集校验可作为独立复核，但不能标成已运行本脚本/此版本；脚本不会自动安装或降级依赖。

普通check只需Python、指定jsonschema及其依赖和仓库中的数据文件；不依赖git，也不要求干净工作树。默认只读校验，不启动ANSYS、不触碰几何/工程文件，CI可直接使用同一命令，失败返回非零退出码。`--record`在这些前提之外额外依赖git和干净、已提交的工作树，才把校验记录写回schema；这是审计记录，不是模型执行工具。

static_validation.last_run记录被校验提交commit、UTC时间at、python、jsonschema，并附schema_content_sha256和校验脚本哈希。last_run.commit指向最初被校验内容所在提交。在普通分支历史里它通常是随后审计提交的父提交；squash/rebase后不再保证这个父子关系，不能从main父提交推导回执位置。PR分支保留原取证历史；冻结版本以contract-0.1.0标签定位squash合并提交，并用内容/脚本哈希与registry、模板pin复核一致性。内容哈希用规范化JSON排除last_run/last_result两个自记录字段，避免提交/哈希自引用。首次取证前last_run保持null。

校验脚本哈希按UTF-8文本统一换行后计算，避免Windows与CI的LF/CRLF检出差异造成误报。

schema内容或校验脚本变更会使旧记录失效，脚本将拒绝沿用旧“通过”；需将last_run/last_result重置为null，提交内容后重新取证。记录校验结果不会将条目状态改为reviewed或validated。

校验包括原有两个反例，以及entity的target=null、project的非null目标、analysis的非法目标类型三项反例；还检查每个分支的目标规则、三个槽位、非法scope_kind、缺参数键、非法gate ID及独立参数类型。analysis允许null或合法引用的正例也会保留。通过仅证明静态结构，不证明去重日志、API回读、保存、求解或结果导出。


## 两种复核结论分开报告

| 报告用语 | 前提 | 可证明的范围 |
| --- | --- | --- |
| 指定校验器通过 | 实际运行本脚本及jsonschema 4.26.0；保留对应last_run与内容/脚本哈希 | 该内容版本通过本项目静态校验，不证明ANSYS可执行 |
| 逻辑等价复现通过 | 独立检查器/等价子集进行复核；未运行指定版本 | 只覆盖复核者列明的规则，不冒充指定校验器运行记录 |

用户本机PyPI不通，已报告的是逻辑等价复现；不能据此给用户环境补写jsonschema 4.26.0运行回执。本仓库代理环境实际运行的指定校验器回执与用户独立复核是两类证据，保留各自边界，不合并成“所有环境均已复跑”。

## stable_id注册表：阶段二前审阅件

[shared/entities/registry.csv](../entities/registry.csv)是本项目stable_id登记入口；目前为15行草稿种子，不是完整实体清单或已解析的运行时映射。由7个明确单体、5个目录材料定义、历史tem、截图“外表面”和历史热分析组成。凸点/焊球各取一个有源对象编号的单体作为起始样本，不代表阵列整体。

注册规则来源为SRC-ENTITY-REGISTRY-USER-001，已先登记在catalog；每行还保留实际数据来源SRC、文件、行/对象定位及该文件SHA-256。规则如下：

- 初始实体/分析/旧选择的stable_id由案例命名空间、种类与首次证据中的object_id确定，例如CSV中的ENT-BGA-BODY前缀；这不是原生API ID。材料直接复用材料目录的material_id；“外表面”使用固定逻辑主键ENT-BGA-NS-OUTER-001；证据编号只放在来源字段，不进入主键，也不填虚构树/面ID。
- 一经确认，stable_id不因显示名变化而重建；跨修订需要明确映射证据，不能根据新版本碰巧复用相同object_id就认作原实体。当前命名规则只是确定性初始登记，不是自动识别算法。
- 逻辑身份为stable_id，overlay选择必须同时限定model_revision；材料还要固定material_revision。model_revision采用原source-manifest.json登记的归档SHA-256，不是猜测的ANSYS版本号，也不是当前工程修订。
- source_object_id只保存历史导出编号。mechanical_tree_id、geometry_body_ids、geometry_face_ids均未运行回读，继续留空；CSV空字段代表未知，不表示零、空作用域或适用于任意修订。part_id未当作CAD体ID复制。
- 当前“外表面”截图没有归档/工程修订桥接证据，model_revision也留空，不能覆盖到原归档的tem。两条登记分别保留，不能自动合并。
- 材料目录当前只有revision 1，按原目录记录；不因材料名称相同就升级到revision 3。实体行只保留观察到的material_name_hint，实际material_id/revision绑定留空，避免把名称匹配当作版本证据。
- resolved_from在材料行使用parameter_table仅指材料CSV登记表，不表示存在Workbench参数集；各行来源用于解析取证，不把显示名称作为执行唯一键。

所有行status=draft、resolution_state=unresolved，审核字段为空；未绑定model_revision或未关闭解析证据的行不得供写工具执行。运行时映射仍需对应工程中只读解析与回读，不能通过复制历史编号获得“已解析”状态。注册表已获用户确认，本轮按新要求补唯一性、alias与自动检查，并开始阶段二模板的entity_ref与校验段；没有关闭运行时U-STABLE-ID。

注册表文件SHA-256固定在entity_policy.registry_sha256内，普通check也核对该哈希、逐行证据文件哈希、来源编号、历史对象编号、材料目录修订及overlay边界。修改注册表需同步更新哈希并重新取证；这些仍是只读静态检查，不是运行时实体解析。

registry_hash_kind及逐行source_hash_kind均明确为utf8-lf：对这里的CSV/JSON/Markdown证据去UTF-8 BOM、统一LF后计算文本哈希，避免Git在Windows/CI之间转换换行造成误报。它们不是原始CAD/工程文件的字节哈希；model_revision引用的原归档SHA-256仍是source-manifest中记录的原文件字节哈希，两者不混用。


## 阶段二第一部分：引用与校验

[结构输入模板](../templates/package-structure-input.json)为每个部件保留entity_ref，连接只保留lower_entity_ref和upper_entity_ref两端引用；连接本身是关系，不登记为实体；全部未知值保持null。引用形状复用工具契约的绝对$ref，不复制schema定义；原有尺寸、位置、材料和边界未知值没有补数。

registry.csv新增aliases和parent_id。当前只登记die_1→ENT-BGA-BODY-25、substrate_1→ENT-BGA-BODY-496；alias必须限定案例及修订，不是执行主键。interposer_1没有BGA实体可映射，保持未注册；parent_id全部留空，不填die/interposer/substrate层级。

校验器机械检查stable_id全局唯一、材料ID/revision在共享目录中存在、任一非空source_object_id在该案例bodies/object-names中存在、证据文件文本哈希一致、status/resolution_state属于声明枚举。所有实际entity_ref引用都检查注册行与修订；model_revision为空的行一律禁止被引用，包含ENT-BGA-NS-OUTER-001。源登记虽存在，不等于已解析运行时映射。

模板validation_state可声明draft/resolved/executable；当前为draft且ready_for_execution=false。draft允许未知引用留null，但不允许错误ID、悬空修订或错连端点。resolved需要全部必需引用、材料与注册映射已解析；executable还需几何重叠、单位、适配器及执行版本门槛。几何重叠和单位转换仍为unresolved，不由LLM宣称已检查；0.1.0始终禁止执行。

本轮仅完成上述数据结构与静态检查，不表示阶段二全部完成。单位换算、几何检查和运行时解析均未实现。阶段三现已补取证方法清单，但尚未采集证据或关闭缺口。


## 实体种类与连接语义

entity_kind只允许body、material、named_selection、analysis。components[].entity_ref和连接两端引用必须指向body；部件材料及underfill.material_id必须指向material。只验证存在性、case与revision不够，种类错误也必须拒绝；拼错entity_kind不能跳过证据分支。

连接没有独立entity_ref，也不新造connection种类；其id标识输入关系，由两端body引用和连接定义推导。旧connection.entity_ref即使为null也禁止重新加入。

## 修改注册表或模板后的协作顺序

1. 修改registry.csv或package-structure-input.json，保留来源与未知字段，不关闭未经取证的映射。
2. 同步更新tools.schema.json中的entity_policy.registry_sha256或package_structure_template.sha256；按utf8-lf规则计算，并将static_validation.last_run/last_result置null。先运行普通check，检查通过后提交内容，得到干净工作树。
3. 重跑`python shared/tools/validate_contract.py --record`，再单独提交回执。CI在第二步之前报pin不一致是预期保护，不表示修改内容本身一定错误。

变更后仍为draft，审计记录不等同于运行证据；若打开执行开关，必须遵守升次版本和同步$id的独立规则。


## 静态来源的审核路径与发布状态

internal_validation_record与消费它的契约分别审核，不互相等待。SRC-CONTRACT-STATIC-CHECK-001的有权限审核人（用户或其指定技术审阅人）应核对：指定校验器实际复跑、版本/命令、被校验提交、schema/脚本哈希及pin、反例拒绝原因和结论范围。审核人将姓名/角色、日期、复核记录与定位写入可追溯的审阅证据，由有权限维护者更新来源登记；本次代理不改reviewed状态、不代签审核。

该来源升级reviewed只表示静态回执可信，不要求先有ANSYS执行证据，也不自动提升契约或工程案例状态；这样避免“来源等契约、契约等来源”的循环。材料标定、实际适配器与仿真结果仍各自需要相应证据，不能由静态来源审核替代。

0.1.0作为只预览的历史版本，本次按授权保留status=draft与空审核字段后冻结。冻结的是被审阅的内容，不是授予执行权限；后续审核结论在新提交/新版本中维护，保留标签历史。当前缺少软件包版本和真实适配器证据，所以执行禁用。validated仍需明确计算/实验与验证范围，单次脚本成功不能证明物理模型有效。

## 冻结锚点与执行端交接

冻结引用为refs/tags/contract-0.1.0，必须指向PR #1的squash合并提交；禁止移动或删除该锚点。标签提供内容定位，本次未额外配置GitHub标签保护规则，权限层面的保护需仓库维护者另行管理。合并后只读复跑check，不在冻结版本上重写--record。

等待连接负责人提供ansys-mechanical-core确切版本、连接模式/Mechanical发行版、首个适配器的接口与代码修订、可复现输入和实际回读/失败记录后，再创建contract 0.2.0。此处不预填版本，不提前绑定adapter_method，也不提前打开执行开关。

指定校验器完整支持其声明的JSON Schema关键字，能避免等价子集漏实现allOf等问题；它仍只能验证已经编码的规则。此前补充的实体种类、连接语义和作用域反例说明业务约束也会遗漏。后续必须保留mutation检查，并分别验证真实ID解析、写后回读、持久化、去重日志和失败恢复；静态绿灯与真实执行证据不能合并汇报。

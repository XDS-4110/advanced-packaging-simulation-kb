# 中文尺寸指令：第一阶段离线预览

本阶段只承诺**理解结果可校验**，不承诺降低端到端总耗时。不调用LLM、不连接SolidWorks/Workbench、不调用几何修改脚本、不执行仿真。无需单独的nl_request.schema.json；确定性规则、运行时检查和测试约束意图输出。

当前case_id固定为bga-2024r2-unsolved，只使用该案例登记的参数与实体。不能将这些归档ID自动用于新建的三层模型或其他工程；新案例需要独立登记和审核映射。

## 使用

```bash
python tooling/nl_request.py "把芯片厚度改成0.45"
python tooling/nl_request.py --stdin < sentence.txt
python tooling/nl_request.py --repo /path/to/checkout "芯片厚度加0.1"
python -m unittest discover -s tooling/tests -q
python -m pytest tooling/tests -q
python tooling/ci_check.py
```

解析器只依赖标准库。pytest是可选入口；CI用unittest运行同一组测试，不会因缺少pytest跳过测试。非空契约请求须使用已有jsonschema做完整校验，缺失时明确失败，不提供不完整的子集校验。本阶段没有合法的SolidWorks契约适配器，contract_requests始终为空。

- stdout只有一个JSON对象。未知或歧义退出码0，unresolved记录原因。
- 空输入、非正尺寸、单位冲突和损坏的数据文件退出码2，诊断只写stderr。
- stdin去掉一次终止换行；其余空白和标点保留用于原句UTF-8 SHA-1，前12位形成request_id。
- 单目标、多目标都用intents数组；nl_schema_version仅是意图信封版本，不是执行契约升级。

## 意图与阻塞

例如“把芯片厚度改成0.45”能识别die_thickness、ENT-BGA-BODY-25、0.45 mm。但状态仍是blocked，不能作为执行许可。

| 标记 | 含义 |
| --- | --- |
| U-CONTRACT-GEOMETRY | 0.1.0的workbench_project.set_geometry_parameter面向Workbench参数集，且当前要求parameter_ref/value为null；不能冒充SolidWorks修改请求 |
| U-ENTITY-RUNTIME | 归档stable_id尚未绑定当前软件会话 |
| U-PARAM-UNKNOWN / U-PARAM-AMBIGUOUS | 未知或多义参数，不猜默认值 |
| U-PARAM-SEMANTICS | 非A类参数或表中物理含义待确认 |
| U-FOLLOWERS-UNAVAILABLE | 参数表无followers列或未登记随动，不能从聊天历史补入 |
| U-FOLLOWER-UNKNOWN / U-FOLLOWER-MISMATCH | 随动描述未知或与登记关系不一致 |
| U-CONFLICT | 重复目标或主目标/随动冲突 |

“凸点高度”目前没有明确参数，不映射为直径。参数表中的凸点轮廓含义待确认，也不能因别名匹配就当作已确认的物理尺寸。

同一句话request_id相同，但相对修改结果随CSV变化，因此另有input_fingerprint，涵盖原句、数据哈希和解析器文件哈希。未来执行端必须检查载荷/数据版本，不可只凭句子ID去重。本阶段不实现执行日志和去重。

## 规则与数据

- 参数来自geometry-parameters.csv；别名来自nl_aliases.csv；零件/实体对应来自nl_entity_map.csv。
- 映射核对registry.csv中的stable_id、case_id及body种类。不依赖显示名，不把geometry_body_ids当文件名；单个归档实体不代表整个阵列。
- 明确别名优先；短别名被更长匹配包含时消除重复。不同参数同时命中时报告歧义。
- 否定句不生成正向操作。范围、条件和未支持的尾部表达不能被静默忽略。
- 使用Decimal换算与相对运算；微米转mm，角度与长度不混用。无单位按用户规格使用mm，显式写assumptions。
- confidence是规则匹配等级，不是正确概率；高分不能消除实体/契约阻塞。
- 相对操作的base_value来自CSV快照，输出base_source，不声称实时读取模型。
- followers如mold_cut_depth:+1表示随动增量系数。无请求不补偿；递归、自循环、单位不一致和非正值拒绝。缺失列在真实预览中阻塞，测试临时表覆盖已登记的随动规则。

## 契约能力不等于可执行能力

现有契约已存在engineering_data.update_material_properties。当前执行层没有经本项目验证的材料属性写入适配，工具仍禁用；契约名字不能证明软件可执行。

用户现场反馈“2024 R2工程数据无对外脚本接口”限定记录为**当前执行入口未能实现**，不扩大为产品全局不存在接口。官方v242 Workbench Scripting Guide的Engineering Data容器确实列有CreateMaterial、ImportMaterial等方法：

https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/wb2_js/ContainerName37.html

2026-11-04核对官方文档，本次未实机执行。文档存在不代表本机适配可用；仍需验证容器、进程、版本、属性方法、单位及保存重开。此处不新增材料物性值，也不增加执行能力。

## 第二阶段单独评审

本阶段保持tools.schema.json、registry.csv、结构模板及两个pin不变。0.1.0→0.2.0另开评审：

1. 明确SolidWorks请求工具名、身份、单位、来源及preview_only范围。
2. 重新计算并同时核对/更新entity_policy.registry_sha256与package_structure_template.sha256；文件没变时pin值可不变，但不能漏检。
3. 同步contract_version、schema `$id`及回归证据；不得在同一0.1.0中放宽执行行为。
4. 执行适配、身份核验、日志/去重、保存与恢复独立验收，不由解析器替代。

整个stdout是意图信封，不直接符合tools.schema.json；只有contract_requests成员属于该契约。阶段一验收为理解结果、来源和阻塞可校验，不能假称已经通过旧规格中的“非空数值请求直接通过0.1.0契约”。

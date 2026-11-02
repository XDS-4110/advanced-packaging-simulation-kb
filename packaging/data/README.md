# 结构化索引与案例证据

[知识索引](knowledge-index.json)由 Markdown 元数据自动生成，不复制正文，不手工编辑。路径相对于仓库根目录；topic/category仅表示存放分类，不自动证明适用对象。适用条件必须读取原文，缺失元数据保留null。

在仓库根目录运行（Python 3，依赖 PyYAML）：

```powershell
python packaging/tools/build_knowledge_index.py
python packaging/tools/build_knowledge_index.py --check
```

每次新增或修改正文后重新生成并一并提交。索引含规范化全文哈希（UTF-8，去BOM，统一换行为LF），用于识别变更；它不是向量数据库，也没有接入API。README导航不进入知识索引。

推荐检索流程：按主题、类别和审核状态筛选 → 按条目路径读取Markdown → 保留来源、适用条件与局限 → 检查案例资料缺口。draft仅供研究和人工筛选，不用于自动生成工程设置；reviewed/validated也不意味着适用于任意案例。索引不授予求解执行权限。

[BGA案例证据清单](../bga/cases/reproduction-evidence.json)是待填清单，尚未绑定具体器件，也没有从原工程自动抽取数据。checklist_basis说明清单依据，不是参数值的来源。所有value均为空；建议单位不代表原资料单位已核实。

填写要求：

- status采用missing、unverified、reviewed；missing必须保留value为null。获得数据后先标unverified。
- 每项值记录source_id、source_locator和applicability；reviewed须补审核人和日期。
- 尺寸细化为带单位的命名分量；时间历程细化为时间和物理量序列，注明单位、插值定义与循环数，不将复合单位字符串直接传给求解器。
- 材料只引用公共材料库的ID和revision，不复制本构常数。
- 不同来源的冲突不得覆盖，应保留候选证据并解释选择。
- 这是交接数据格式约定，当前没有JSON Schema自动校验或求解器映射；提交前需要人工审核。simulation负责工程输入和求解验证。

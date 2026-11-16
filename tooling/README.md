# 只读知识检索工具

Python 3.10+，仅使用标准库，不调用求解器、不改工程。

```text
python tooling/kb_retrieve.py info
python tooling/kb_retrieve.py search "COMSOL 网格质量" --tier explain --k 3
python tooling/kb_retrieve.py resolve transient-thermal
python tooling/kb_retrieve.py lookup CURRENT-MODEL-ID
python tooling/kb_retrieve.py eval
python tooling/rebuild_metadata.py
python tooling/ci_check.py
```

`--repo <path>` 或 `KB_REPO` 可指定副本。`strict` 只返回 reviewed/validated；`explain` 也返回 draft。每条结果保留来源、状态及 `usable_for_arguments`；即使已审核也须核对适用范围。新增 COMSOL 文档保持 draft，不能用提高状态的方式让查询返回正式参数。

`lookup` 只读明确登记的实体，未找到则返回缺失。旧工程实体和材料数值已撤下，当前注册表为空。`resolve` 是文档路由，不是执行计划或写入授权。

保留原有可选 stdio 资料服务，但本次不连接客户端，也不增加求解器执行接口。

## 元数据与检查

`rebuild_metadata.py` 同步语料基线与封装导航索引。`info` 的 `baseline_match` 应为 true；具体计数和哈希以 `corpus-baseline.json` 为准。知识内容、来源或状态修改后，在同一 PR 重建并检查。

`ci_check.py` 检查基线、换行、来源、路由、相对链接及草稿门禁；`eval` 检查检索命中和负例。不把文档静态检查说成 COMSOL 运行验证。

正文范围保持封装、仿真和公共材料条目；README、代理规则、模板、工具、原文件及生成索引不进入知识正文。来源旁存映射只补充元数据，不拼入正文。

迁移范围与待审内容见 [清理记录](COMSOL_MIGRATION.md)。

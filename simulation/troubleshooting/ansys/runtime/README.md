# Workbench 运行与对象接口失败记录

2026-11-03 本机记录，入口见[ANSYS索引](../README.md)。五篇案例均为draft，仅供解释与排查，不得直接作为工具参数来源。

- data/probe_log.txt：Geometry DataReference.Import失败。
- data/probe2_log.txt：系统DataReference.GetChildren失败及成员回读。
- data/probe3_log.txt：geometry refreshed后Model DataReference.Edit失败。
- data/source-manifest.json：原始文件与脱敏文件SHA-256；未上传的脚本和代理摘要的来源定位。
- data/execution-observations.json：实际日志证据、代理摘要与未完成阶段的区别。

原始Windows用户目录已替换为[WORKSPACE]。不上传账号配置、令牌、安装包、工程模型或厂商文档全文。原始完整记录仍保留在本机。

本次只整理证据，不重新启动Workbench、不修复软件、不宣称材料分配、网格或求解完成。实际运行版本、稳定启动方式、保存重开及失败恢复机制仍待补证；所有审核字段保持空白。

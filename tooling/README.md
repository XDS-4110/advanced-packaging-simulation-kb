# tooling — 知识库检索与自动化代码

本目录存放可执行代码。知识条目仍在 `packaging/`、`simulation/`、`shared/`；本目录**不进入 RAG 正文索引**，也不提供任何工程数值。

## 当前内容

| 文件 | 用途 |
| --- | --- |
| `kb_retrieve.py` | 知识库检索引擎；同时提供 CLI 与 MCP stdio 服务 |
| `kb_eval.csv` | 检索评估集（问题 / 期望命中 / 不得命中） |
| `mcp.example.json` | MCP 客户端配置示例 |
| `README.md` | 本文件 |

## 依赖

- Python ≥ 3.9（实测 3.12.14）
- **无第三方依赖**，不需要 pip install

## 用法

全部命令在仓库根目录执行。

```bash
python tooling/kb_retrieve.py info
python tooling/kb_retrieve.py search "温度场怎么传给结构" --tier strict -k 3
python tooling/kb_retrieve.py resolve transient-thermal
python tooling/kb_retrieve.py lookup MAT-BGA-SN63PB37-001 anand
python tooling/kb_retrieve.py eval
python tooling/kb_retrieve.py serve
```

指定其他仓库副本：`--repo <path>` 或环境变量 `KB_REPO`。

## 状态门控

| tier | 允许状态 | 能否作为工具参数值 |
| --- | --- | --- |
| `strict` | `reviewed`、`validated` | 可以 |
| `explain` | 上述 + `draft`（标注） | **不可以** |

每条结果带 `status` 与 `usable_for_arguments`。门控在代码中强制，不依赖提示词。`draft` 结果仅供解释与排错，不得写入 `arguments`。

## MCP 接入

`serve` 提供三个工具：`kb_search`、`kb_resolve`、`kb_lookup`。配置见 `mcp.example.json`，把 `command` 与 `args` 换成目标机器的绝对路径。

## 换机验收

在新机器上执行 `info`，看 `baseline_match`。基线固定在 `corpus-baseline.json`，含 commit、文档数与内容哈希。

```
baseline_match = true
documents = 119, chunks = 585
corpus_sha256 = 0bba538c862ac59b4b74377812b47ea23f4747a9e8c42402cf5355fdef14ae44
```

`baseline_match: false` 表示知识内容已变。改内容时**在同一 PR 内**更新 `corpus-baseline.json`，不要事后补。

## 索引范围

只索引知识条目：`packaging/`、`simulation/`、`shared/materials/`。
**排除**：`README.md`、`AGENTS.md`、`CONTRIBUTING.md`、`shared/templates/`、`shared/tools/`、`files/`、`tooling/`。
指令文件与代码不得成为可引用来源，否则代理会引用自己的规则。

## 评估

`eval` 输出 `hit_at_5`、`mrr`、`gate_violations`。`gate_violations` 必须恒为 0：它统计的是 `strict` 模式下是否返回了非 reviewed/validated 文档。

2026-11-03 快照：12 题，hit@5 = 1.0，MRR = 0.903，gate_violations = 0。其中 2 题命中但未排第一，属排序调优项。

## 边界

- 不做向量检索：当前可入库正文规模约 8 万字符，BM25 足够；引入 embedding 会带来版本漂移。
- 不生成、不推断任何工程数值；数值只能来自 `kb_lookup` 命中的材料表或案例数据。
- 不连接 ANSYS，不执行求解。执行端适配器不在本目录。
- 尚未接入 CI；`eval` 目前需手动运行。

## 待办

- 排序调优（课程笔记类文档需降权）
- 评估集扩到 20 题
- 与 `shared/tools/validate_contract.py` 的证据编号互链

## 中文指令离线预览（第一阶段）

`python tooling/nl_request.py "把芯片厚度改成0.45"` 输出确定性意图JSON。只承诺理解结果可校验，不承诺减少总耗时。无软件执行、无LLM调用，契约保持0.1.0。详见 [实现与边界](nl_request.md)。

同一套测试支持 `python -m unittest discover -s tooling/tests -q` 和 `python -m pytest tooling/tests -q`；`ci_check.py` 用标准库运行测试，不新增pytest运行依赖。

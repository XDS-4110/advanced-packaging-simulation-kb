# LLM 驱动先进封装自动化建模与仿真知识库

为先进封装自动化建模与仿真提供可追溯的 RAG 知识。当前仅有目录与填写模板，尚无已审核技术正文或材料参数。

## 两个知识入口

| 入口 | 主要维护 | 内容 |
| --- | --- | --- |
| [封装知识 packaging](packaging/README.md) | 封装协作者 | 基础、结构、工艺、材料原始资料、可靠性试验与封装案例 |
| [仿真知识 simulation](simulation/README.md) | 仿真负责人 | 建模等效、热分析、结构分析、发热应力翘曲、温度循环、材料输入、软件操作与验证 |

仿真基线：**ANSYS Workbench 2024 R2**。当前重点为运行发热后的应力与翘曲，以及温度循环。

## 公共资料

- [填写模板](shared/templates/README.md)
- [RAG 入库规范](shared/rag/README.md)
- [资料来源登记](shared/references/README.md)
- [贡献与协作约定](CONTRIBUTING.md)

## 两人协作方式

1. 封装协作者在 `packaging/` 补充结构、工艺、材料原始证据及试验条件。
2. 仿真负责人在 `simulation/` 补充建模假设、材料输入、边界、网格、求解和验证。
3. 材料原始资料放在 `packaging/materials/`；仿真采用值与本构设置放在 `simulation/materials/`，明确引用来源。
4. 先在 `shared/references/catalog.csv` 登记来源，再复制模板建立条目，默认状态为 `draft`。
5. 知识元数据 `domain` 填 `packaging` 或 `simulation`，方便 RAG 按领域过滤。模板和目录说明不进入正式检索索引。

目录分工不限制协作者的实际写入权限；本次整理不修改仓库可见性或成员权限。

缺失信息标注“待补充”，不填猜测数值。不上传密钥、受限工程文件或未经许可的论文和标准全文；外部内容保留原始许可和署名。公开前另行确定本仓库许可。

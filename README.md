# LLM 驱动先进封装自动化建模与仿真知识库

本仓库整理电子封装与仿真相关知识，为 LLM 的检索增强生成（RAG）提供可追溯的依据。

当前阶段：知识库骨架。尚未收录经过审核的技术条目、材料参数或仿真案例；后续逐步补充。

## 内容导航

| 目录 | 用途 |
| --- | --- |
| [封装基础](knowledge/packaging/README.md) | 封装类型、结构、工艺、术语与可靠性 |
| [建模与简化](knowledge/modeling/README.md) | 几何识别、参数化、TSV/凸点等效、均匀化 |
| [热仿真](knowledge/simulation/thermal/README.md) | 稳态/瞬态传热、边界条件、接触热阻 |
| [力学仿真](knowledge/simulation/mechanical/README.md) | 热应力、翘曲、焊点与界面可靠性 |
| [电磁与耦合仿真](knowledge/simulation/electromagnetic/README.md) | 互连寄生、信号/电源完整性、电热耦合 |
| [网格与验证](knowledge/verification/README.md) | 网格收敛、热平衡、结果核验与误差分析 |
| [材料数据](materials/README.md) | 带来源、单位、温度与适用条件的材料属性 |
| [软件操作](software/README.md) | ANSYS Mechanical、Icepak、HFSS 等版本化操作与脚本说明 |
| [仿真案例](cases/README.md) | 输入、建模步骤、结果、验证与复现记录 |
| [资料来源](references/README.md) | 论文、官方文档、数据表、标准和外部项目索引 |
| [填写模板](templates/README.md) | 知识条目、材料、案例和文献模板 |
| [RAG 入库规范](rag/README.md) | 元数据、切分边界、筛选与来源追踪 |

## 如何开始补充

1. 在 `references/catalog.csv` 登记资料来源。
2. 从 `templates/` 复制对应模板，放入合适目录，并填写元数据。
3. 保留公式条件、变量单位、页码或章节，标明事实、推导或个人经验。
4. 默认标记为 `draft`；完成审核后再设为 `reviewed`，完成案例验证后可设为 `validated`。
5. 按 [贡献说明](CONTRIBUTING.md) 提交修改。模板和目录说明默认不进入正式检索索引。

不上传密钥、受限工程文件或未经许可的论文、标准全文。外部内容保留原始许可和署名；仓库初始不统一授予开源许可，公开前另行确定。

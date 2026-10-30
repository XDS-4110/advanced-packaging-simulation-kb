# 封装知识

主要维护：封装协作者。按共用基础、BGA 专题、2.5D 专题组织；具体软件操作与计算设置由仿真负责人维护。

## 三个知识入口

| 入口 | 范围 |
| --- | --- |
| [电子封装共用基础](common/README.md) | 通用概念、结构单元、材料知识、工艺与可靠性基础 |
| [BGA 专题](bga/README.md) | 球栅阵列封装的分类、结构、装配、可靠性与案例 |
| [2.5D 专题](2-5d/README.md) | 多芯片、中介层与桥接架构的结构、工艺、可靠性与案例 |

2.5D 是集成架构，BGA 是外部互连形式；同一封装可同时涉及两者。“专题特有”表示重点研究对象，不表示其中所有技术都独占于该专题。跨专题案例保留一个主记录，另一入口通过链接引用。

## 内容归属

- 通用定义和原理写在 common；BGA、2.5D 写具体结构中的应用及差异。
- TSV、RDL、凸点、焊球、底填胶的基础知识只维护一份；专题引用基础条目。
- 材料参数统一维护在 [公共材料库](../shared/materials/README.md)，按材料 ID 和 revision 引用；不新建三份材料参数库。
- 封装部分记录实物结构、尺寸来源、材料牌号、工艺历史、实际工况及试验依据。
- 等效、本构输入、边界条件、接触、网格、求解和验证方法归 [simulation](../simulation/README.md)。

## 开始补充

使用 [公共模板](../shared/templates/README.md)，封装条目 domain 填 packaging；共用材料记录遵循公共材料库规则。来源登记到 [统一来源表](../shared/references/catalog.csv)。缺失信息写“待补充”，未审核条目标 draft。

遵循 [贡献约定](../CONTRIBUTING.md) 与 [RAG 规范](../shared/rag/README.md)。本次建立的是分类与待编写清单，README 不作为已审核知识入库。

当前优先补充共用基础中与 BGA 相关的知识，以及 [BGA 案例资料](bga/cases/README.md)。旧的七个平级分类入口已移除；新增内容仅写入上述三个入口。旧外部链接请改为对应专题路径。

## 写入流程与文件职责

1. 在 shared/references/catalog.csv 登记来源，取得唯一 SRC- 编号。
2. 选择 common（通用知识）、bga（BGA 应用）或 2-5d（2.5D 应用），再选择内容类别。
3. 复制对应模板，新建小写英文连字符命名的 Markdown 文件；不要把技术正文堆入 README。
4. 填写唯一 id、domain: packaging、status: draft、source_ids 和原文页码/图表位置。未知内容写“待补充”。
5. README 只维护范围、填写说明和已新增条目的链接；不作为已审核知识入库。

| 内容类别 | 写入内容 | 使用模板 |
| --- | --- | --- |
| fundamentals | 定义、分类、原理和适用范围 | knowledge-entry |
| structures | 部件位置、连接关系、层叠、结构差异 | knowledge-entry |
| processes | 制造/装配顺序、温度时间历史、材料状态 | knowledge-entry |
| reliability | 失效机理、试验条件、失效判据、测量证据 | knowledge-entry |
| references | 一份资料的书目信息、原文定位、结论及局限 | reference-note |
| cases（专题内） | 一个实物对象的尺寸、材料引用、工况、试验及缺口 | packaging-case |
| common/materials | 材料作用、牌号识别和物性条件等概念 | knowledge-entry |

模板见 [公共模板](../shared/templates/README.md)。具体材料数值统一写入 [公共材料库](../shared/materials/README.md)，案例仅引用 ID 与 revision。软件设置、网格、接触和求解步骤写入 simulation。

例如：一篇 BGA 温循论文先在 bga/references 写阅读笔记；特定器件的尺寸和温循表写入 bga/cases；可复用的通用原理另写 common，使用链接关联而不复制全文。

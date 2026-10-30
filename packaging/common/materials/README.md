# 材料知识与公共库入口

范围：Si、铜、焊料、基板介质、Underfill、塑封料及 TIM 的作用；牌号、成分、固化状态、温度依赖、各向异性、Tg 与物性测试条件。

材料数据统一维护于 [公共材料库](../../../shared/materials/README.md)。封装协作者补充牌号、成分、工艺/固化状态、厂商数据及测试条件，与仿真负责人共同审阅同一记录；通过材料 ID 和修订版引用。

当前待补充经审核的知识条目。使用 [公共模板](../../../shared/templates/README.md)，遵循 [贡献约定](../../../CONTRIBUTING.md) 与 [RAG 规范](../../../shared/rag/README.md)。来源登记至 [统一来源表](../../../shared/references/catalog.csv)；未知信息标为“待补充”。

[返回本专题](../README.md) · [封装总入口](../../README.md)

## 如何新增文件

复制 [填写模板](../../../shared/templates/knowledge-entry.md) 到本目录，另起有意义的文件名，例如 `topic-note.md`（仅为命名示例）。

- 必填内容：材料的作用、牌号/成分、固化状态、Tg、温度依赖和方向性等知识；链接公共材料记录。
- 自查：数值和参数表统一维护在 shared/materials，不在本目录建立副本。
- 元数据：唯一 id、domain: packaging、status: draft、source_ids、原文页码或图表、更新日期。
- README 仅作导航；新增正文后在下方添加链接。

## 已有知识条目

暂无独立正文；本目录说明和待办清单不代表已审核知识。

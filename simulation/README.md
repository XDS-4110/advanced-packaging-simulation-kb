# 仿真知识

主要维护：仿真负责人（你）。这是内容分工，不改变 GitHub 仓库访问权限。

## 目录

- [几何建模与等效](modeling/README.md)
- [热分析](thermal/README.md)
- [结构分析](mechanical/README.md)
- [发热后的应力与翘曲](thermal-stress/README.md)
- [温度循环](thermal-cycling/README.md)
- [电磁与其他耦合（扩展）](electromagnetic/README.md)
- [网格与结果验证](verification/README.md)
- [公共材料库（双方共用）](../shared/materials/README.md)
- [材料本构与软件输入](materials/README.md)
- [仿真软件操作](software/README.md)
- [仿真案例](cases/README.md)
- [仿真文献笔记](references/README.md)

## 开始补充

从 [公共模板](../shared/templates/README.md) 复制对应条目；元数据 `domain` 填 `simulation`。来源登记到 [统一来源表](../shared/references/catalog.csv)。跨领域内容保留一份，通过条目 ID 或相对链接引用，避免两份参数不一致。

## 问题排查

- [COMSOL 与 ANSYS 问题案例及解决办法](troubleshooting/README.md)

## BGA 参数提取案例

- [首个案例：BGA 未求解参数提取](cases/bga-2024r2-unsolved/README.md)（draft，未求解；含待复核设置，不能直接作为推荐输入）。

# ANSYS 问题索引

当前基线为 ANSYS Workbench 2024 R2；Mechanical 等具体产品、模块及其他版本需逐案注明。

## 分类与待收集主题

以下是收集方向，不是已验证的原因或解决办法。

- [几何导入与修复](geometry/README.md)
- [薄层、焊点网格质量](mesh/README.md)
- [约束、刚体运动、非线性收敛与单元畸变](solver/README.md)
- [接触设置与状态异常](contacts/README.md)
- [温度场向结构场传递](load-transfer/README.md)
- [应力峰值与翘曲提取](postprocessing/README.md)

## 案例登记

新增本机运行失败案例均为draft；尚无经审核的解决方案或仿真结果。

| 案例 ID 与链接 | 报错/现象关键词 | 软件与版本 | 物理场 | 审核状态 |
| --- | --- | --- | --- | --- |
| [KB-TS-ANSYS-0001：Workbench 批处理长时间无日志与反复启动](runtime/batch-launch-without-progress.md) | batch / launch / timeout / journal | 目标2024 R2；实际版本待核验 | 前处理/运行环境 | draft |
| [KB-TS-ANSYS-0002：几何导入失败：DataReference 没有 Import](runtime/geometry-datareference-has-no-import.md) | geometry / DataReference / Import / AttributeError | 目标2024 R2；实际版本待核验 | 前处理/运行环境 | draft |
| [KB-TS-ANSYS-0003：Mechanical 调用失败：DataReference 没有 Edit 和 GetChildren](runtime/mechanical-component-container-mismatch.md) | Mechanical / DataReference / Edit / GetChildren / SendCommand | 目标2024 R2；实际版本待核验 | 前处理/运行环境 | draft |
| [KB-TS-ANSYS-0004：Workbench 目标路径与窗口版本不一致](runtime/workbench-runtime-version-mismatch.md) | version / v242 / 2026 / runtime | 目标2024 R2；实际版本待核验 | 前处理/运行环境 | draft |
| [KB-TS-ANSYS-0005：如何判断材料和网格阶段确实完成](runtime/materials-mesh-completion-evidence.md) | materials / mesh / evidence / partial | 目标2024 R2；实际版本待核验 | 前处理/运行环境 | draft |

参见 [排错库使用说明](../README.md)。

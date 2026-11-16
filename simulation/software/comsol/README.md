# COMSOL 操作与核验资料

基线 COMSOL Multiphysics 6.4。以下均为新整理的 `draft`；已核对官方文档，尚未在本机逐项运行验证。每篇保留具体来源与适用限制，旧版本资料不自动当作 6.4 可执行接口。

| 主题 | 资料 |
| --- | --- |
| 单位 | [绝对温度与温差](01-temperature-units.md) |
| 几何拓扑 | [Union / Assembly](02-union-assembly.md) |
| 作用域 | [命名选择](03-named-selections.md)、[暴露空气的外表面](04-air-exposed-boundaries.md) |
| 热边界 | [指定温度与对流](05-temperature-vs-convection.md) |
| 耦合 | [瞬态热结构与惯性](06-transient-thermal-stress.md) |
| 温循 | [函数与插值表](07-thermal-cycle-functions.md) |
| 网格 | [质量与收敛](08-mesh-quality-convergence.md) |
| 求解 | [时间步与容差](09-time-stepping-tolerances.md) |
| 保存 | [MPH 保存和读回](10-mph-save-readback.md) |
| 参数 | [几何尺寸与参数化](11-geometry-parameters.md) |

不提供通用材料常数、通用网格阈值、已验证工程参数或自动执行授权。官方来源登记见 `shared/references/catalog.csv` 和 `shared/references/comsol-official-sources.json`。

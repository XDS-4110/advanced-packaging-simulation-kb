# 材料模型与输入：Workbench 2024 R2

物理参数统一引用 [公共材料库](../../shared/materials/README.md)。这里记录本构选择、属性映射、单位处理和输入检查，不维护另一份数值。

## 学习与填写顺序

1. [属性到 Engineering Data 的映射](01-property-input-mapping.md)
2. [发热翘曲与温度循环的模型选择](02-model-selection.md)
3. [单位、温度轴与瞬时/割线 CTE](03-units-temperature-cte.md)
4. [Sn63Pb37 的 Anand 字段核对](04-anand-input-check.md)
5. [BGA 待补资料与完成判据](05-bga-material-review.md)

## 工作表

- [材料字段映射](data/bga-input-mapping.csv)：只引用公共 ID/版本与属性键；当前禁止自动采用。
- [输入审核清单](data/bga-review-checklist.csv)：待填写，初始全部 pending。

初版均为 draft，尚未本地界面逐项复现或求解。官方字段核对不等于材料已标定。原工程及公共参数不作修改，新数据保留修订记录。

## 已取得的报告证据

[BGA 报告与工程对照](../references/bga-thermal-reliability-report/report-project-comparison.md) 已确认 m/h0 对应、SFL 比热单位和焊料弹性温度轴不一致。原值不覆盖，需决定采用依据。

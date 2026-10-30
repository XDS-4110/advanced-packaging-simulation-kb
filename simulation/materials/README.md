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

## 当前修改状态

见 [revision 2材料证据](../../shared/materials/bga-20261030-revision2.md)：m/h0和E/ν温度轴已对齐报告，比热差异仍在；不要把历史revision 1的差异当成当前保存值。

## 最新状态：revision 3

[比热修正后的当前材料证据](../../shared/materials/bga-20261030-revision3.md)：65条材料属性与报告对齐。此前差异记录保留历史；Mechanical同步与归档仍待核对。

## 材料界面证据

[材料截图及后补温度表核对](../../shared/materials/bga-material-screenshots.md)：初次51条可见数值及后补15条温度相关输入均与revision 3相符；三张温度表截图已补齐。Mechanical同步、结构参考温度及材料温区依据仍待核实。

## Mechanical赋值证据

[BGA七类部件材料赋值截图记录](../cases/bga-2024r2-unsolved/11-material-assignment-ui.md)：确认材料名称关联，具体参数同步另行核实。

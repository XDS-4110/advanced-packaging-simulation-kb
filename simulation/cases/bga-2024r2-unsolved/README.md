# BGA：Workbench 2024 R2 未求解工程的知识提取

本案例依据用户提供的工程文件只读提取。**尚未求解、没有温度/应力/翘曲/寿命结果；全部技术条目为 draft。**

## 内容入口

- [案例总览与系统连接](01-case-overview.md)
- [实体、材料赋值与接触](02-geometry-contacts.md)
- [材料属性与 Anand 参数原值](03-materials.md)
- [温度循环载荷](04-temperature-cycle.md)
- [分析设置、网格与输入文件范围](05-settings-mesh.md)
- [无法可靠提取的内容与补充清单](06-missing-information.md)
- [发现的待复核问题](07-review-findings.md)
- [提取方法与来源证据](08-provenance.md)

`data/` 提供 CSV 和 JSON，保留原值、单位及定位。原始 WBPZ、STEP、Mechanical 数据库与大网格输入不上传仓库。

优先复核第 7 篇的 Anand 参数、材料温区和时间节点，再补全第 6 篇的结构设置。不要将本案例直接作为已验证的自动化模板。

## 新取得的报告

- [报告方法与来源](../../references/bga-thermal-reliability-report/report-knowledge.md)
- [报告—工程差异及决策](../../references/bga-thermal-reliability-report/report-project-comparison.md)

报告有作者结果，但当前工程仍未求解。

## 最新提取

- [第二次提取：材料修改与剩余问题](09-revision2-material-review.md)。第1～8篇保留初次快照和后续报告的证据历史；当前Engineering Data修改状态以第9篇为准。

## 最新状态：revision 3

[比热修正后的当前材料证据](../../../shared/materials/bga-20261030-revision3.md)：65条材料属性与报告对齐。此前差异记录保留历史；Mechanical同步与归档仍待核对。

## 材料界面证据

[材料截图及后补温度表核对](../../../shared/materials/bga-material-screenshots.md)：初次51条可见数值及后补15条温度相关输入均与revision 3相符；三张温度表截图已补齐。Mechanical同步、结构参考温度及材料温区依据仍待核实。

## 当前瞬态热设置

[第10篇：热分析界面及暴露表面作用域](10-thermal-ui-scope.md)：初温25 ℃、tem共335面、第14步结束时间已更新；结构分析尚未开展。

---
id: KB-TS-ANSYSED-001
title: "ANSYS 工程数据：材料库文件、唯一 ID 与加载顺序"
document_type: troubleshooting
domain: simulation
status: draft
scope: general
scope_note: "实测环境 ANSYS 2024 R2 + Windows 10；不同版本的文件布局与加载规则需复核。"
language: zh-CN
tags: [ansys, engineering-data, material-library, matml, troubleshooting]
physics: [thermal, structural]
software: [ANSYS Workbench, ANSYS Mechanical]
software_versions: ["2024 R2"]
source_ids: [SRC-ANSYS-ED-LAB-001]
source_locator: "2026-11-03 本机实测：工程数据文件结构、GUID 去重、加载顺序"
updated_at: "2026-11-03"
reviewed_by: ""
reviewed_at: ""
---

# ANSYS 工程数据：材料库文件、唯一 ID 与加载顺序

> 一次"文件里明明有 6 个材料、界面上只显示 1 个"的排查记录。

## 问题

把材料直接写进工程的工程数据文件，重新打开 Workbench 后，材料表里仍然只有默认的「结构钢」。

## 工程数据存在哪

一个 Workbench 工程里，材料数据出现在**三处**：

| 路径 | 作用 | 是否被界面读取 |
| --- | --- | --- |
| `<project>_files/dp0/global/MECH/SYS.engd` | 工程级材料库 | 启动时读取 |
| `<project>_files/dp0/SYS/ENGD/material.engd` | 系统级副本 | 否 |
| `<project>_files/dp0/SYS/ENGD/EngineeringData.xml` | 可读副本 | **否** |

工程数据界面显示的是**工程打开时载入内存的状态**，并在启动瞬间用内存状态**回写**上述文件。因此：

- 在 Workbench 关闭时改文件，**可能**在下次启动被读到；
- 在 Workbench 运行期间改文件，必被覆盖；
- 改 `EngineeringData.xml` 单独一个文件没有意义。

实测：启动瞬间 `EngineeringData.xml` 被重写为 27 KB（仅 1 个材料），而同目录 `material.engd` 与 `global/MECH/SYS.engd` 保持被写入的内容。三份文件因此并不一致。

## 三个真实原因

### 1. Material Unique Id 必须唯一

每个 `<Material>` 里有一个隐藏属性：

```xml
<PropertyData property="pr15">
  <Qualifier name="guid">59002a79-71c2-428e-906b-55d7dbee100e</Qualifier>
</PropertyData>
```

从模板克隆材料时，这个 GUID 会一起被复制。**Workbench 按 GUID 去重，重复的只保留第一个，且不报错。**

实测：6 个材料共用 1 个 GUID 时，界面只显示 1 个；改为 6 个唯一 GUID 后不再被去重。

### 2. 材料库 XML 的元素顺序

`MatML_Doc` 的子元素顺序必须是：

```
<Material> ... </Material>   ← 可以多个
<Metadata> ... </Metadata>   ← 必须最后
```

若 `Metadata` 出现在中间，**其后的材料不会被加载**。用脚本追加材料时最易犯：追加操作把新材料放在了 `Metadata` 之后。

实测：顺序为「结构钢 → Metadata → SI → …」时，库里只看见结构钢；调整为「6 个材料 → Metadata」后，6 个全部可见。

### 3. 材料库要用「工程数据源」加载

两个菜单不是一回事：

| 操作 | 作用 |
| --- | --- |
| 工程数据 → 文件 → 导入 | 导入**数据**，不建立材料库 |
| 工程数据 → **工程数据源** → 添加新库 | 把文件注册为**材料库** |

只有后者会让库出现在「工程数据源」列表里。加载后还需要**勾选该库**，再**把材料加入工程**——库注册 ≠ 材料进工程。

## 正确流程

1. 生成材料库文件（`.engd` 或 `.xml`，MatML 结构）
2. 工程数据 → 工程数据源 → 添加新库 → 选文件
3. **勾选**新库
4. 在库的材料列表中逐个「添加到工程」
5. 关闭工程数据 → 工程数据单元格变黄 → 右键更新

## 附带：ANSYS 内置 Python 的三处缺陷

用脚本读写工程数据/模型时，ANSYS 自带的 IronPython 是**裁剪版本**：

| 写法 | 结果 |
| --- | --- |
| `import json` | `ImportError: No module named _json` |
| `codecs.open(..., "utf-8")` | `LookupError: unknown error handler name 'strict'` |
| `str(b.Material)`（对 .NET 对象） | `UnicodeEncodeError: unknown` |

**可靠写法**：只用 .NET 文件接口，避免 Python 字符串转换：

```python
import clr
clr.AddReference("System")
from System.IO import StreamWriter
from System.Text import Encoding
sw = StreamWriter(path, False, Encoding.UTF8)
sw.WriteLine(b.Name)      # 直接写 .NET 字符串，不调用 str()
sw.Close()
```

## 判据

- 材料表可见个数 == 文件里的 `<Material>` 个数，才算写入成功；
- 出现"文件里有、界面没有"时，先查 **GUID 是否重复**，再查 **Metadata 是否在末尾**；
- 库文件能被"添加新库"识别，不等于材料可用，必须显式加入工程。

## 未验证

- 其他版本是否同样按 GUID 去重；
- `SYS.engd` 在 Workbench 关闭状态下修改是否总被接受（本机一次成功、一次未生效）；
- 温度相关属性表（CTE、弹性模量随温度变化）在库文件中的正确编码方式，本次只写入了常数属性。

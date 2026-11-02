---
id: REF-COURSE-VIDEO-OPTICAL-20261102
title: "光通信封装案例：结构与连接证据笔记"
document_type: reference_note
domain: packaging
status: draft
tags: [course-video, optical-package, wire-bond, connectivity]
source_ids: [SRC-COURSE-VIDEO-OPTICAL-UP, SRC-COURSE-VIDEO-OPTICAL-DOWN, SRC-COURSE-VIDEO-OPTICAL-SUPPLEMENT, SRC-CARPENTER-KOVAR, SRC-IBIS-TOUCHSTONE-21]
source_locator: "光通信封装仿真实例上、下、下下；具体时间戳见正文；中段暂未形成笔记"
updated_at: "2026-11-02"
reviewed_by: ""
reviewed_at: ""
---

# 光通信封装案例：结构与连接证据笔记

## 阅读范围

讲师阿姆、仿真秀；正式出版年份待确认。本轮读完上段（约19分钟）、下段（约71分钟）、下下补充段（约13分钟）的机器转录，并抽查下列原尺寸画面。中段尚未形成核对结论。不是逐帧完整语义审核，原始工程也没有本地复现；下段软件画面显示Electronics Desktop 2020 R2。

机器转录存在PD、TIA、wire bond、端口和数值误识别。对完整矩阵、材料值和网格参数不按识别文本直接入库。文件哈希及阅读状态见[视频清单](../../../files/course-41-video-review-manifest.json)。

## 上段：封装层级与功能

00:00–07:40介绍模块、发射/接收功能与内部器件；08:00–13:10比较TO-can及盒式光器件；13:10–16:45讨论热、电和对准位移问题。抽查画面为08:46、11:46、15:47，可见器件剖面、TX/RX注释及组件布局。

可用于本项目的辨析：模块与内部封装不是同一层级；目标温度、允许相对位移应从具体产品要求取得，不能把课程举例的温度或微米级位移当成所有封装的阈值。Kovar在转录中被描述为不锈钢的说法不采纳；[Carpenter原厂资料](https://www.carpentertechnology.com/hubfs/7407324/Material%20Saftey%20Data%20Sheets/Kovar.pdf)将其列为铁镍钴低膨胀合金。原音措辞尚未逐句核对。

## 下段：几何与连接决定模型是否描述了同一结构

| 时间 | 观察与处理 |
| --- | --- |
| 00:00–13:50 | 从整体器件截取局部电连接结构，讨论导入与实体分割；材料临时代替不是目标器件材料证据 |
| 13:50–21:45 | 建立键合线、调整线弧与落点，强调工艺可制造性；17:29和19:32画面抽查 |
| 28:00–37:15 | 补充参考地与过孔；列举的孔尺寸和纵横比不是统一工艺能力 |
| 44:45–50:15 | 分离信号与参考导体；48:40画面可见分割后的独立金属与端口相关报错 |
| 54:30–57:00 | 根据异常响应检查到过孔位置造成连接错误；56:00画面查看过孔，57:42查看重新求解进度 |
| 59:50–70:35 | 继续优化接地并说明CAD实体合并问题；图形改善不等于实验验证，宽带性能数值未采纳 |

形成[键合线几何、工艺与电连接](../structures/wire-bond-geometry-and-connectivity.md)。软件菜单、端口选择和频率设置不在packaging中复制为操作教程。

## 下下段：导出数据仍须保留定义

00:00–04:00展示Touchstone导出文件，随后导入电路软件，最后讨论端口场分布。02:30、03:19原尺寸画面可见`# GHz S MA R 50`和端口注释；10:20抽查端口显示界面。不能把机器转录中的“零赫兹”等字样越过文件头直接作为单位依据。

两端口数据的顺序按格式版本核对：Touchstone 1.0/1.1惯例为N11、N21、N12、N22；2.0/2.1使用`[Two-Port Data Order]`明确顺序。见[IBIS Touchstone 2.1规范第10、15页](https://ibis.org/touchstone_ver2.1/touchstone_ver2_1.pdf)。课程口述/转录给出的顺序不能代替规范，尤其不能因互易例子中两个传输项相近就认为解析顺序无关。

## 对知识库的适用范围

这些光器件不是2.5D或BGA专属案例，因此只提取通用结构证据方法，不新增光器件必需层或推荐参数。全部条目为draft。尚待核对完整原工程、物理材料、工艺能力、原始测试，以及未完成的中段视频。

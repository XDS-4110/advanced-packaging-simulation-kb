---
id: REF-COURSE-VIDEO-WARPAGE-CORRECTION-20261102
title: "warpage计算问题更正：视频证据笔记"
document_type: reference_note
domain: packaging
status: draft
tags: [course-video, warpage, CTE, evidence]
source_ids: [SRC-COURSE-VIDEO-WARPAGE-CORRECTION, SRC-ANSYS-242-CTE-DEFINITION, SRC-ANSYS-242-THERMAL-EXPANSION]
source_locator: "正式课程/6. 第11讲warpage计算问题更正_.mkv；时间戳见正文"
updated_at: "2026-11-02"
reviewed_by: ""
reviewed_at: ""
---

# warpage计算问题更正：视频证据笔记

## 书目信息与阅读范围

课程讲师自述阿姆，画面标识仿真秀；正式出版年份待确认。视频约7分08秒。SHA256：`73c35b68d990392365a54d672edcabe5d178efab936ab76c7bb45d0dd81c49f6`。

程序解码10,693帧，生成149张变化/定时索引图。本轮已查看这些索引图及每10秒预览；对00:45、04:20、05:50、06:50另看原尺寸画面。索引采用1秒最短保存间隔及变化阈值，不能保证覆盖短暂细节。这不等于逐一语义审核10,693张原始帧。

已阅读全段00:02–07:03的机器转录并与索引画面对照。语音由本地模型生成带时间戳转录，专业术语与数字存在明显错误，不能把机器转录当作讲师准确原话。全课程范围见[视频核对清单](../../../files/course-41-video-review-manifest.json)。未上传原视频、课程截图或完整转录。

## 时间戳与可核对的内容

| 区间 | 观察及入库处理 |
| --- | --- |
| 00:00–00:36 | Engineering Data中的Die材料页面，随后切换Substrate；不凭材料名认定牌号 |
| 00:37–01:40 | 展示基板正交各向异性割线CTE及Zero-Thermal-Strain Reference Temperature字段；00:45画面值350°C，记录为演示值 |
| 01:45–03:10 | 展示CTE和弹性模量随温度变化，讲解涉及Tg与不同部件的工艺温度；转录中的具体温度存在误识别，不据此补齐载荷 |
| 03:10–05:40 | 切换各方向CTE及弹性属性，继续讨论简化；不能推出所有基板都可忽略Tg或厚度方向差异 |
| 05:44–06:12 | 修改材料表中的温度节点；中间存在尚未输入完成的表格状态，不应从任意一帧抄录材料卡 |
| 06:14–06:38 | 返回Mechanical并执行求解；画面可见ANSYS 2020 R2，与本项目2024 R2不同 |
| 06:39–07:07 | 展示Y方向位移云图；06:50显示最小值约−79.919 μm、最大值0 μm，是课程屏幕结果，不是本项目复现或验证结果 |

## 重要辨析

视频补充了PDF没有完整呈现的材料定义和修改过程。对本项目最有用的是把CTE定义、参考基准、温度区间与工艺历程一起交接，而不是记住一个软件字段数值。

课程中“350°C”的演示不能推广成任意封装的材料参考温度。已对照ANSYS 2024 R2的[CTE输入定义](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/wb_eda/eda_linear_mat_mdl.html)和[热膨胀说明](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ans_mat/ansmattherexp.html)，区分材料数据基准与模型参考状态；不能仅根据工艺峰温改写实测CTE的定义基准。

## 全段转录补充核对

04:25–05:13的转录说明，这次补充与从回流示例转到热压键合示例时未同步调整材料温区有关。05:19–06:09中讲师通过抬高属性转折温度演示修改，随后重算。这是对该教学模型的处理，不能解释成“改变真实材料Tg即可修复仿真”。真实器件应核实部件各自温度历程、材料测量曲线及模型简化是否一致。

06:25–06:46讲师比较此前较大结果与重算后的约80；后者可与06:50画面的−79.919 μm对应。此前“700多”的精确值、单位与原始模型尚未独立核验，因此不计算改进百分比，也不称为实验误差下降。

## 验证与局限

未在本地重跑视频工程，没有原工程的完整输入快照，也没有实验对照。修改温度节点后出现云图不证明修改符合真实材料；软件版本、输入完成状态、载荷与约束均需进一步核验。视频对简化影响大小的经验判断尚未通过目标器件验证。

本轮不发布视频操作为通用求解教程。可归入packaging的资料整理原则见[CTE参考温度与工艺状态](../materials/cte-reference-and-process-state.md)。全部内容仍为draft。

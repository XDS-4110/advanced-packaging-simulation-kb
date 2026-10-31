# 书籍资料

存放本项目使用的书籍资料，供 packaging 与 simulation 共同引用。

| 书籍 | 文件 | 说明 |
| --- | --- | --- |
| 微电子封装技术 | [PDF](microelectronic-packaging-technology.pdf) | 用户提供的原始文件；作者、出版社、版次与年份待核对。尚未完成内容提取与审核。 |

PDF 使用 Git LFS 保存。克隆项目后执行 `git lfs pull` 下载原始文件；网页端可通过文件页面下载。

引用时补齐书目信息及章节、页码，来源登记至 [来源目录](../shared/references/README.md)。阅读笔记及审核后的知识放回 packaging 或 simulation；上传文件本身不代表已建立可检索、可用于仿真的知识条目。

## BGA 共用基础论文与笔记（2026-10-31）

| 论文 | 原文获取状态 | 笔记 |
| --- | --- | --- |
| [Underfill: A Review of Reliability Improvement Methods in Electronics Production](https://pmc.ncbi.nlm.nih.gov/articles/PMC12389694/) | PDF 未取得；公开页面或书目线索已核对 | [阅读笔记](../packaging/common/references/underfill-2025.md) |
| [Survey on Fatigue Life Prediction of BGA Solder Joints](https://mdpi-res.com/d_attachment/electronics/electronics-11-00542/article_deploy/electronics-11-00542.pdf?version=1644572039) | [PDF](bga-fatigue-2022.pdf) | [阅读笔记](../packaging/bga/references/bga-fatigue-2022.md) |
| [Effect of critical properties of epoxy molding compound on warpage prediction: A critical review](https://terpconnect.umd.edu/~bthan/paper/A%20Chapter%2C%20Review%20and%20Invited/Review%20papers/2022%20Warpage%20Review%20Paper%20MRE.pdf) | PDF 已在本地读取；仅提供原文链接，未确认转载许可 | [阅读笔记](../packaging/common/references/emc-warpage-2022.md) |
| [Solder joint failures under thermo-mechanical loading conditions – A review](https://doi.org/10.1080/2374068X.2020.1751514) | PDF 未取得；公开页面或书目线索已核对 | [阅读笔记](../packaging/common/references/solder-failures-2020.md) |
| [Material and constitutive parameters of various Pb-based and Pb-free solders and other interconnection materials: A collective review](https://doi.org/10.1016/j.rineng.2025.105618) | PDF 未取得；公开页面或书目线索已核对 | [阅读笔记](../packaging/common/references/constitutive-2025.md) |

获取记录见 [清单](paper-acquisition.json)。未下载的文件不以摘要或生成 PDF 代替。所有笔记为 draft，尚不能作为已审核工程输入。

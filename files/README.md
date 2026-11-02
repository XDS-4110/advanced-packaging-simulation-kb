# 文件：论文与书籍原始资料

此处统一保存原件；笔记和知识条目位于 packaging。全部新增知识仍为 draft，不直接用于生成仿真参数。

| 资料 | 原件或原文入口 | 阅读与许可状态 |
| --- | --- | --- |
| 微电子封装技术 | [书籍PDF](microelectronic-packaging-technology.pdf) | 用户此前提供并上传的原件，本次迁入；作者、版次及全文学习待补，不作为本批条目证据 |
| Survey on Fatigue Life Prediction of BGA Solder Joints | [论文PDF](bga-fatigue-2022.pdf) | Qiu等，2022；CC BY 4.0；DOI 10.3390/electronics11040542；重点章节阅读 |
| A Review of System-in-Package Technologies: Application and Reliability of Advanced Packaging | [论文PDF](sip-review-2023.pdf) | Wang等，2023；CC BY 4.0；DOI 10.3390/mi14061149；重点章节阅读 |
| RDL聚合物介质综述 | [公开原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC10575375/) | DOI 10.3390/polym15193895；CC BY 4.0；PDF下载403，正文部分核对 |
| Underfill综述 | [公开原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12389694/) | DOI 10.3390/polym17162206；PDF未取得；已核对页面部分 |
| 塑封料与翘曲综述 | [作者公开PDF](https://terpconnect.umd.edu/~bthan/paper/A%20Chapter%2C%20Review%20and%20Invited/Review%20papers/2022%20Warpage%20Review%20Paper%20MRE.pdf) | DOI 10.1016/j.microrel.2022.114480；本地阅读，保留所有权利，未确认转载许可，仅链接 |

PDF保持原样，保留作者及许可信息。文件校验见 [manifest](manifest.json)。PDF通过Git LFS保存，克隆后可执行 `git lfs pull`。论文和书籍统一存放于本目录，不另设图书目录。

## 用户筛选建议

先审查条目的适用范围和来源定位，再决定保留、修改或删除。不要仅因属于同一封装类别而采用论文参数；具体材料数据统一进入 shared/materials。尚未检得可完整入库的新专著，本次书籍原件是已有资料的迁移，不宣称新增专著或完成整本书学习。

## 文献笔记与获取记录


| 论文 | 原文获取状态 | 笔记 |
| --- | --- | --- |
| [Underfill: A Review of Reliability Improvement Methods in Electronics Production](https://pmc.ncbi.nlm.nih.gov/articles/PMC12389694/) | PDF 未取得；公开页面或书目线索已核对 | [阅读笔记](../packaging/common/references/underfill-2025.md) |
| [Survey on Fatigue Life Prediction of BGA Solder Joints](https://mdpi-res.com/d_attachment/electronics/electronics-11-00542/article_deploy/electronics-11-00542.pdf?version=1644572039) | [PDF](bga-fatigue-2022.pdf) | [阅读笔记](../packaging/bga/references/bga-fatigue-2022.md) |
| [Effect of critical properties of epoxy molding compound on warpage prediction: A critical review](https://terpconnect.umd.edu/~bthan/paper/A%20Chapter%2C%20Review%20and%20Invited/Review%20papers/2022%20Warpage%20Review%20Paper%20MRE.pdf) | PDF 已在本地读取；仅提供原文链接，未确认转载许可 | [阅读笔记](../packaging/common/references/emc-warpage-2022.md) |
| [Solder joint failures under thermo-mechanical loading conditions – A review](https://doi.org/10.1080/2374068X.2020.1751514) | PDF 未取得；公开页面或书目线索已核对 | [阅读笔记](../packaging/common/references/solder-failures-2020.md) |
| [Material and constitutive parameters of various Pb-based and Pb-free solders and other interconnection materials: A collective review](https://doi.org/10.1016/j.rineng.2025.105618) | PDF 未取得；公开页面或书目线索已核对 | [阅读笔记](../packaging/common/references/constitutive-2025.md) |

获取记录见 [清单](paper-acquisition.json)。未下载的文件不以摘要或生成 PDF 代替。所有笔记为 draft，尚不能作为已审核工程输入。

- [芯片封装仿真41讲资料清单](course-41-reading-manifest.json)及[阅读笔记](../packaging/common/references/course-41-reading-notes.md)：记录本地课件的哈希和阅读范围，原课程文件未上传。

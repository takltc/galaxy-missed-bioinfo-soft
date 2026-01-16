# Haplocheck Galaxy Wrapper

[English](README.md)

基于线粒体系统发育的污染检测工具 Galaxy 集成。

## 软件信息

| 属性 | 值 |
|------|-----|
| 版本 | 1.3.3 |
| 开发者 | Sebastian Schönherr, Hansi Weissensteiner, Lukas Forer (Genepi Innsbruck) |
| 许可证 | MIT License |
| GitHub | https://github.com/genepi/haplocheck |
| DOI | 10.1101/gr.256545.119 |
| PMID | 33452015 |

## 概述

Haplocheck 通过分析线粒体 DNA 内容来检测 mtDNA 和全基因组测序 (WGS) 研究中的样本内污染。它通过检测表现为异质性（多态性）位点的系统发育不兼容线粒体单倍型来识别污染。

### 核心功能

- 检测低至 1% 水平的污染（需要足够覆盖度）
- 同时适用于 mtDNA 靶向测序和 WGS 数据
- 提供带有系统发育树可视化的交互式 HTML 报告
- 可作为核 DNA 污染检测的代理工具
- 快速处理：约 2,500 个样本在 2 小时内完成

## 工作流程

```
BAM/CRAM (mtDNA 比对)
         │
         ▼
   Mutserve Call
         │
         ▼
    VCF (变异)
         │
         ├──────────────────┐
         │                  │
         ▼                  ▼
    Haplocheck         Haplogrep3
         │                  │
         ▼                  ▼
    污染报告           单倍群分类
```

## 输入要求

| 格式 | 要求 |
|------|------|
| VCF | 同质性变异编码为 "1/1"，异质性变异编码为 "0/1" 并带有 AF 标签 |
| 来源 | Mutserve Call 输出或 GATK MuTect2 线粒体流程 |

## 输出文件

| 文件 | 描述 |
|------|------|
| contamination.txt | 主报告，包含污染状态、水平和单倍群 |
| contamination.raw.txt | 扩展指标（可选） |
| report.html | 带有系统发育树的交互式 HTML 报告（可选） |

## 污染报告列说明

| 列名 | 描述 |
|------|------|
| Sample | 样本标识符 |
| Contamination Status | YES、NO 或 ND（不可检测） |
| Distance | 主要/次要单倍群之间的系统发育距离 |
| Contamination Level | 估计的污染百分比 |
| Sample Coverage | mtDNA 平均覆盖度 |
| Major Haplogroup | 主要单倍群 |
| Minor Haplogroup | 污染单倍群 |

## 最佳实践参数

基于文献研究 (PMID: 33452015):

| 参数 | 推荐值 | 描述 |
|------|--------|------|
| 覆盖度 | ≥100x 用于 10% | ≥600x 用于 1% 污染检测 |
| 质量 | 单倍群质量 ≥0.5 | 可靠检测所需 |
| 距离 | 系统发育距离 ≥2 | 单倍群之间的最小距离 |

### 不同污染水平的覆盖度要求

| 污染水平 | 最低覆盖度 |
|---------|-----------|
| 10% | 100x |
| 5% | 200x |
| 1% | 600x |

## 污染场景

Haplocheck 检测三种污染场景：

1. **场景 A**: 两个单倍型分支到两个不同的谱系
2. **场景 B**: 次要单倍型是主要单倍型的祖先（同一谱系）
3. **场景 C**: 主要单倍型是次要单倍型的祖先（同一谱系）

## 基准测试表现

根据 García-Olivares 等人 (2021) Sci Rep (PMID: 34654896):

- Haplocheck 是 mtDNA 分析最完整的工具
- 对全基因组测序 (WGS) 和全外显子测序 (WES) 数据都准确
- 成功测试了 Nanopore 长读长测序数据

## Docker 容器

使用本目录中的 Dockerfile 构建：

```bash
cd docker
docker build -t omniverse/haplocheck:1.3.3 .
```

## 文件结构

```
haplocheck/
├── docker/
│   └── Dockerfile
├── haplocheck.xml
├── tool_conf.xml
├── README.md
└── README_CN.md
```

## 相关工具

- **Mutserve**: mtDNA 变异检测（为 Haplocheck 生成输入 VCF）
- **Haplogrep3**: mtDNA 单倍群分类
- **mtDNA-Server 2**: 完整的 mtDNA 分析流程

## 局限性

- 无法检测具有相同单倍群的样本之间的污染
- 极少数的大型 NUMT 可能导致假阳性结果
- 古 DNA 由于 DNA 降解需要更高的覆盖度

## 引用

如果您在研究中使用此工具，请引用：

> Weissensteiner H, Forer L, Fendt L, Kheirkhah A, Salas A, Kronenberg F, Schoenherr S. 
> Contamination detection in sequencing studies using the mitochondrial phylogeny. 
> Genome Res. 2021;31:309-316. doi:10.1101/gr.256545.119

## 链接

- 在线服务: https://mitoverse.i-med.ac.at
- GitHub: https://github.com/genepi/haplocheck
- 文档: https://mitoverse.readthedocs.io/haplocheck/haplocheck/

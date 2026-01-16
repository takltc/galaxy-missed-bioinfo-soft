# fastMitoCalc Galaxy Wrapper

[English](README.md)

Galaxy 集成：用于从全基因组测序数据超快速估算线粒体 DNA 拷贝数。

## 软件信息

| 属性 | 值 |
|------|-----|
| 版本 | 1.0.0 |
| 开发者 | Yong Qian, Jun Ding 等 (NIA/NIH) |
| 许可证 | 未指定 |
| GitHub | https://github.com/qian0001/fastMitoCalc |
| DOI | 10.1093/bioinformatics/btx167 |
| PMID | 28453676 |

## 概述

fastMitoCalc 是一个超快速程序，用于从全基因组测序 (WGS) 数据估算线粒体 DNA (mtDNA) 拷贝数。它比原始 mitoCalc 程序快约 100 倍，可以在不到一分钟内分析一个 BAM 文件（核 DNA 平均覆盖度为 4X）。

### 主要特点

- **超快速处理**：比原始 mitoCalc 快约 100 倍
- **最低要求**：核 DNA 平均覆盖度 4X 即可工作
- **灵活方法**：随机区域、特定染色体或自定义 BED 文件
- **大规模研究**：适合处理数千个样本

## 算法

mtDNA 拷贝数计算公式：

```
mtDNA-CN = 2 × (mtDNA 覆盖度 / 核 DNA 覆盖度)
```

因子 2 是因为核基因组是二倍体，而线粒体基因组是单倍体。

## 工作流程

```
FASTQ (WGS)
     │
     ▼
  BWA-MEM
     │
     ▼
BAM (已索引)
     │
     ├──────────────────┐
     │                  │
     ▼                  ▼
fastMitoCalc      Mutserve Call
     │                  │
     ▼                  ▼
mtDNA 拷贝数      VCF (变异)
   报告                │
                       ├──────────────┐
                       │              │
                       ▼              ▼
                  Haplocheck    Haplogrep3
                       │              │
                       ▼              ▼
                  污染检测      单倍群分类
                    报告          报告
```

## 输入要求

| 格式 | 要求 |
|------|------|
| BAM | 坐标排序，已索引（需要 .bai 文件）|
| 覆盖度 | 核 DNA 最低 4X 平均覆盖度 |
| 参考基因组 | 染色体命名需一致 |

## 输出

制表符分隔的报告，包含以下列：

| 列名 | 描述 |
|------|------|
| mt_copy_number_avg | 估算的 mtDNA 拷贝数 |
| mt_coverage | 平均 mtDNA 测序覆盖度 |
| autosomal_coverage | 平均核 DNA 覆盖度 |
| actual_basepairs_covered | 被读段覆盖的总碱基数 |
| chrom_used_for_autosomal_coverage | 用于计算的染色体 |

## 覆盖度估算方法

### 1. 随机区域（默认，最快）

从常染色体中随机选择 N 个指定大小的区域：
- 默认：3000 个 1000 bp 的区域
- 以最少的计算提供稳健的估算

### 2. 特定染色体

使用整条染色体进行核 DNA 覆盖度估算：
- 22号染色体常用（体积较小）
- 更彻底但更慢

### 3. 自定义 BED 文件

用户定义的核 DNA 覆盖度估算区域：
- 适用于专门分析
- 软件包包含用于 WES 数据的 1000G 脱靶区域

## 最佳实践参数

基于文献研究：

| 参数 | 推荐值 | 描述 |
|------|--------|------|
| num_regions | 3000 | 随机区域数量（默认）|
| region_size | 1000 | 每个区域大小（bp，默认）|
| 覆盖度 | ≥4X | 最低核 DNA 覆盖度 |

### 染色体命名

| 参考基因组 | 常染色体 | 线粒体 |
|------------|----------|--------|
| GRCh37/38 | 1, 2, ... 22 | MT |
| hg19/38 | chr1, chr2, ... | chrM |

## 典型 mtDNA 拷贝数值

| 组织 | mtDNA-CN 范围 |
|------|---------------|
| 血液 (PBMC) | 50-500 |
| 心脏 | 1000-10000 |
| 肝脏 | 500-5000 |
| 肌肉 | 1000-6000 |
| 大脑 | 500-3000 |

## 临床应用

mtDNA 拷贝数已被用作以下疾病的生物标志物：

- **阿尔茨海默病**：较低的 mtDNA-CN 与 AD 风险增加相关
- **帕金森病**：PD 患者小脑 mtDNA-CN 升高
- **心血管疾病**：与冠心病风险呈负相关
- **衰老**：65 岁后下降
- **哮喘**：较高的 mtDNA-CN 与急性发作风险降低相关

## Docker 容器

使用此目录中的 Dockerfile 构建：

```bash
cd docker
docker build -t omniverse/fastmitocalc:1.0.0 .

# 测试
docker run --rm omniverse/fastmitocalc:1.0.0 perl /opt/fastMitoCalc/fastMitoCalc.pl
```

## 文件结构

```
fastmitocalc/
├── docker/
│   └── Dockerfile
├── fastmitocalc.xml
├── tool_conf.xml
├── README.md
└── README_CN.md
```

## 相关工具

- **Mutserve**：mtDNA 变异检测工具
- **Haplocheck**：污染检测工具
- **Haplogrep3**：mtDNA 单倍群分类工具
- **mitoAnalyzer**：同一开发者的原始 mtDNA 分析流程

## 引用

如果您在研究中使用此工具，请引用：

> Qian Y, Butler TJ, Opsahl-Ong K, Giroux NS, Sidore C, Nagaraja R, Cucca F, Ferrucci L, Abecasis GR, Schlessinger D, Ding J. fastMitoCalc: an ultra-fast program to estimate mitochondrial DNA copy number from whole-genome sequences. Bioinformatics. 2017 May 1;33(9):1399-1401. doi:10.1093/bioinformatics/btx167

## 链接

- GitHub：https://github.com/qian0001/fastMitoCalc
- 原始 mitoAnalyzer：https://lgsun.irp.nia.nih.gov/hsgu/software/mitoanalyzer/index.html
- PubMed：https://pubmed.ncbi.nlm.nih.gov/28453676/

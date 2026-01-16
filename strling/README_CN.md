# STRling Galaxy Wrapper

[English](README.md)

短串联重复序列 (STR) 扩展检测工具的 Galaxy 集成，支持已知和新发位点检测。

## 软件信息

| 属性 | 值 |
|------|-----|
| 版本 | 0.6.0 |
| 开发者 | Quinlan Lab (University of Utah) |
| 许可证 | MIT |
| DOI | 10.1186/s13059-022-02826-4 |
| PMID | 36474232 |

## 功能概述

STRling (发音类似 "sterling") 是一种使用 k-mer 计数方法从短读测序数据中检测大型短串联重复序列 (STR) 扩展的工具。主要特点：

- **新发 STR 扩展检测**: 可检测参考基因组中不存在的 STR 扩展
- **已知位点检测**: 同时检测参考基因组中已注释的 STR 扩展
- **k-mer 计数**: 使用 k-mer 计数恢复错误映射的 STR 读段
- **碱基对级别精度**: 使用软剪切读段精确定位扩展插入点

## 临床应用

STRling 特别适用于检测导致以下疾病的重复序列扩展：

| 疾病 | 基因 | 重复单元 |
|------|------|----------|
| CANVAS | RFC1 | AAGGG |
| 亨廷顿病 | HTT | CAG |
| 弗里德赖希共济失调 | FXN | GAA |
| 脆性 X 综合征 | FMR1 | CGG |
| 肌强直性营养不良 | DMPK/CNBP | CTG/CCTG |
| 脊髓小脑共济失调 | 多种 | 多种 |

以及其他 40+ 种 STR 相关疾病。

## 输入格式

| 格式 | 说明 |
|------|------|
| BAM/CRAM | PCR-free WGS 比对文件（需排序和索引） |
| FASTA | 参考基因组（推荐 GRCh38） |

## 工作流程

STRling 工作流程分为三个主要步骤：

```
BAM/CRAM 文件
      │
      ▼
   Extract (提取 STR 信息读段)
      │
      ▼
   Call (调用 STR 扩展)
      │
      ▼
   输出结果
```

## 关键参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| min_support | 5 | 调用 STR 扩展所需的最小支持读段数 |
| min_cluster_reads | 2 | 报告位点所需的最小簇读段数 |

## 输出文件

| 文件类型 | 说明 |
|----------|------|
| Bounds | STR 位点边界信息，包含检测到的 STR 扩展位置 |
| Genotype | 基因型估计，包含等位基因大小估计 |
| Unplaced | 无法分配到特定位点的 STR 读段计数 |

## 性能指标

根据原始论文验证：

| 指标 | 单独调用 | 联合调用 |
|------|----------|----------|
| 灵敏度 | 87.2% | 98.9% |
| 位置精度 | - | 平均误差 6.14 bp |
| FDR | - | 0.078 |

## Docker 容器

自建镜像：

```bash
cd docker
docker build -t strling:0.6.0 .
```

**注意**: STRling 仅支持 linux/amd64 架构。

## 文件结构

```
strling/
├── docker/
│   └── Dockerfile
├── strling.xml
├── tool_conf.xml
├── test-data/
├── README.md
└── README_CN.md
```

## 引用

如果您在研究中使用了此工具，请引用：

> Dashnow H, Pedersen BS, Hiatt L, et al. STRling: a k-mer counting approach that detects short tandem repeat expansions at known and novel loci. Genome Biol. 2022;23(1):257. doi:10.1186/s13059-022-02826-4

## 相关链接

- GitHub: https://github.com/quinlan-lab/STRling
- 文档: https://strling.readthedocs.io/
- Quinlan Lab: https://quinlanlab.org/

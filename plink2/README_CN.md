# PLINK2 Galaxy Wrapper

[English](README.md)

用于基因型数据质量控制和人群分层分析的 Galaxy 集成。

## 软件信息

| 属性 | 值 |
|------|-----|
| 版本 | 2.0 |
| 开发者 | Christopher Chang |
| 许可证 | GNU GPL v3 |
| DOI | 10.1186/s13742-015-0047-8 |
| PMID | 25722852 |

## 概述

PLINK2 是 PLINK 1.9 的完全重写版本，提供显著的性能提升和新功能。本 wrapper 提供 PRS 工作流所需的核心功能：

- **质量控制 (QC)**: MAF、缺失率和 HWE 过滤
- **主成分分析 (PCA)**: 人群分层校正
- **等位基因频率计算**: 每个变异的等位基因频率

## 最佳实践参数 (来自 UK Biobank 研究)

| 参数 | 推荐值 | 文献来源 |
|------|--------|----------|
| MAF | ≥0.01 | PMID:35251129 |
| geno | ≤0.02 | PMID:35251129 |
| mind | ≤0.02 | PMID:35251129 |
| HWE | ≥1e-6 | PMID:35251129 |
| PCA | 10 PCs | PMID:39425790 |

## 输入格式

| 格式 | 描述 |
|------|------|
| VCF | 标准变异调用格式 |
| PLINK binary | .bed (基因型), .bim (变异), .fam (样本) |

## 输出文件

| 模式 | 输出文件 |
|------|----------|
| QC | 过滤后的 PLINK binary (.bed/.bim/.fam) |
| PCA | 特征向量 (.eigenvec), 特征值 (.eigenval) |
| Freq | 等位基因频率表 (.afreq) |

## Docker 容器

构建镜像:

```bash
cd docker
docker build -t plink2:2.0 .
```

## 文件结构

```
plink2/
├── docker/
│   └── Dockerfile
├── plink2.xml
├── tool_conf.xml
├── test-data/
├── README.md
└── README_CN.md
```

## 引用

如果您在研究中使用此工具，请引用：

> Chang CC, Chow CC, Tellier LC, Vattikuti S, Purcell SM, Lee JJ. Second-generation PLINK: rising to the challenge of larger and richer datasets. Gigascience. 2015;4:7. doi:10.1186/s13742-015-0047-8

## 链接

- 官网: https://www.cog-genomics.org/plink/2.0/
- GitHub: https://github.com/chrchang/plink-ng

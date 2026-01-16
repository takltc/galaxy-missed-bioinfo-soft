# Haplogrep3 Galaxy Wrapper

[English](README.md)

线粒体 DNA (mtDNA) 单倍群分类工具的 Galaxy 集成。

## 软件信息

| 属性 | 值 |
|------|-----|
| 版本 | 3.2.2 |
| 开发者 | Innsbruck Medical University |
| 许可证 | MIT |
| DOI | 10.1093/nar/gkad284 |
| PMID | 37070190 |

## 功能概述

Haplogrep3 用于对人类线粒体 DNA 进行单倍群分类，广泛应用于：

- **医学遗传学**: 线粒体疾病诊断、疾病关联研究
- **法医学**: 母系血缘鉴定、失踪人员案件
- **进化研究**: 人类群体研究、迁徙模式分析
- **群体遗传学**: 祖先溯源、人口历史重建

## 输入格式

| 格式 | 说明 |
|------|------|
| FASTA | 线粒体基因组序列 (完整或部分) |
| VCF | 来自测序或基因分型芯片的变异调用格式 |
| HSD | 制表符分隔的文本格式 (样本ID、范围、变异) |

## 系统发育树

| 树 | 参考序列 | 用途 |
|----|----------|------|
| PhyloTree 17 Forensic Update 1.2 | rCRS | 法医学应用 (推荐) |
| PhyloTree 17.2 | rCRS | 最新研究级系统发育 |
| PhyloTree 17.0 | rCRS/RSRS | 标准分析 |
| PhyloTree 16.0/15.0 | rCRS | 向后兼容 |

## 关键参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| tree | phylotree-fu-rcrs-1.2 | 系统发育树选择 |
| metric | kulczynski | 距离度量方法 |
| hits | 1 | 输出的 top N 命中数 |
| hetLevel | 0.9 | 异质性水平阈值 (VCF) |

## Docker 容器

自建镜像：

```bash
cd docker
docker build -t haplogrep3:3.2.2 .
```

## 文件结构

```
haplogrep3/
├── docker/
│   └── Dockerfile
├── haplogrep3.xml
├── tool_conf.xml
├── README.md
└── README_CN.md
```

## 引用

如果您在研究中使用了此工具，请引用：

> Schönherr S, Weissensteiner H, Kronenberg F, Forer L. 
> Haplogrep 3 - an interactive haplogroup classification and analysis platform. 
> Nucleic Acids Res. 2023. doi:10.1093/nar/gkad284

## 相关链接

- Web Service: https://haplogrep.i-med.ac.at
- GitHub: https://github.com/genepi/haplogrep3
- Documentation: https://haplogrep.readthedocs.io

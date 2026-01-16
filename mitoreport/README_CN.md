# MitoReport Galaxy Wrapper

[English](README.md)

Galaxy 集成 MitoReport - 用于线粒体 DNA 变异分析和临床解释的综合工具。

## 软件信息

| 属性 | 值 |
|------|-----|
| 版本 | 1.2.3 |
| 开发者 | Murdoch Childrens Research Institute (MCRI) 生物信息学方法组 |
| 许可证 | 开源 |
| GitHub | https://github.com/bioinfomethods/mitoreport |
| 演示 | https://bioinfomethods.github.io/mitoreport/examples/mitoreport-MITOREPORT-TEST-SAMPLE/index.html |

## 概述

MitoReport 是一个线粒体 DNA 变异分析应用程序，可生成用于临床解释的交互式 HTML 报告。它集成了：

- MitoMap 变异注释
- gnomAD 人群频率
- 异质性分析
- 缺失检测
- 母系异质性比较

## 工具组件

### 1. MitoReport (mitoreport)

主分析工具，从以下输入生成交互式报告：

- VEP 注释的 VCF 文件
- 包含 mtDNA 读段的 BAM 文件
- MitoMap 注释
- gnomAD 人群频率

### 2. MitoReport Download (mitoreport_download)

用于从 https://mitomap.org 下载最新 MitoMap 注释的实用工具

## 工作流程

```
                    ┌──────────────────┐
                    │  MitoReport      │
                    │  Download        │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ MitoMap JSON     │
                    └────────┬─────────┘
                             │
┌──────────────────┐         │         ┌──────────────────┐
│ VEP 注释的       │         │         │ gnomAD mtDNA     │
│ VCF              ├─────────┼─────────┤ VCF              │
└──────────────────┘         │         └──────────────────┘
                             │
┌──────────────────┐         │         ┌──────────────────┐
│ 探针 BAM         ├─────────┼─────────┤ 对照 BAMs        │
└──────────────────┘         │         │ (可选)           │
                             │         └──────────────────┘
┌──────────────────┐         │
│ 母系 VCF         ├─────────┘
│ (可选)           │
└──────────────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    MitoReport    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ 交互式 HTML      │
                    │ 报告             │
                    └──────────────────┘
```

## 输入要求

| 输入 | 格式 | 必需 | 描述 |
|------|------|------|------|
| VCF | VCF/VCF.GZ | 是 | VEP 注释的线粒体变异 |
| 样本名称 | 文本 | 是 | 样本标识符 |
| BAM | BAM | 是 | 包含 mtDNA 的比对读段 |
| MitoMap JSON | JSON | 是 | 来自 MitoReport Download 的注释 |
| gnomAD VCF | VCF/VCF.GZ | 是 | 人群频率数据 |
| 对照 BAMs | BAM | 否 | 用于缺失归一化的参考样本 |
| 母系 VCF | VCF/VCF.GZ | 否 | 用于异质性遗传分析 |
| 母系样本名 | 文本 | 否 | 母系 VCF 中的样本名称 |

## 输出文件

| 文件 | 格式 | 描述 |
|------|------|------|
| 交互式报告 | HTML | 主输出，包含可搜索的变异表 |
| 完整报告归档 | TAR.GZ | 用于离线使用的完整输出目录 |

## 主要功能

### 变异注释
- 集成 MitoMap 疾病关联
- gnomAD 人群频率
- VEP 功能注释
- 单倍群标记信息

### 异质性分析
- 变异等位基因频率量化
- 异质性水平的可视化表示
- 与母系样本的比较（如提供）

### 缺失检测
- 大规模 mtDNA 缺失分析
- 使用对照样本进行归一化
- 可视化缺失图

## 最佳实践参数

基于英国最佳实践指南 (PMID: 36513735)：

| 参数 | 推荐值 | 描述 |
|------|--------|------|
| 覆盖度 | ≥500x | 可靠异质性检测的最低要求 |
| VAF 阈值 | 1-5% | 用于临床变异检测 |
| 对照样本 | ≥3 | 用于准确的缺失归一化 |

### 推荐工作流程

1. 首先运行 **Haplocheck** 检查污染
2. 使用 **Mutserve** 进行变异调用（异质性阈值 1-5%）
3. 使用 **VEP** 注释变异
4. 使用 **MitoReport Download** 下载 MitoMap 注释
5. 使用 **MitoReport** 生成报告

## Docker 容器

使用此目录中的 Dockerfile 构建：

```bash
cd docker
docker build -t omniverse/mitoreport:1.2.3 .
```

## 资源文件

MitoReport 需要外部资源文件：

1. **gnomAD mtDNA VCF**: `gnomad.genomes.v3.1.sites.chrM.vcf.bgz`
   - 下载地址：https://gnomad.broadinstitute.org/downloads#v3-mitochondrial-dna
   
2. **MitoMap 注释**：由 MitoReport Download 工具生成

3. **对照 BAMs**（可选）：来自 1000 Genomes 或您自己的数据

## 文件结构

```
mitoreport/
├── docker/
│   └── Dockerfile
├── mitoreport.xml
├── mitoreport_download.xml
├── tool_conf.xml
├── README.md
└── README_CN.md
```

## 相关工具

- **Mutserve**：mtDNA 变异调用（异质性检测）
- **Haplocheck**：污染检测（在 MitoReport 之前运行）
- **Haplogrep3**：单倍群分类
- **VEP**：变异效应注释

## 临床应用

- 原发性线粒体疾病诊断
- 异质性监测
- 携带者检测
- mtDNA 变异研究

## 致谢

MitoReport 由 Murdoch Childrens Research Institute (MCRI) 的生物信息学方法组开发，贡献者包括：

- 维多利亚州临床遗传学服务中心 (VCGS)
- 澳大利亚基因组学健康联盟
- MCRI 脑与线粒体研究组

## 引用

如果您在研究中使用此工具，请引用：

> Bioinformatics Methods Group. MitoReport: Interpretation software for mitochondrial variants. GitHub. https://github.com/bioinfomethods/mitoreport

对于 mtDNA 分析最佳实践：

> Mavraki E, et al. Genetic testing for mitochondrial disease: the United Kingdom best practice guidelines. Eur J Hum Genet. 2023;31:148-163. doi:10.1038/s41431-022-01249-w

## 链接

- GitHub：https://github.com/bioinfomethods/mitoreport
- 演示：https://bioinfomethods.github.io/mitoreport/examples/
- MitoMap：https://mitomap.org/MITOMAP
- gnomAD mtDNA：https://gnomad.broadinstitute.org/downloads#v3-mitochondrial-dna

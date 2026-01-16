# ExpansionHunter Galaxy Wrapper

[English](README.md)

短串联重复序列 (STR) 扩展检测工具的 Galaxy 集成。

## 软件信息

| 属性 | 值 |
|------|-----|
| 版本 | 5.0.0 |
| 开发者 | Illumina |
| 许可证 | Apache License 2.0 |
| DOI | 10.1101/gr.225672.117, 10.1093/bioinformatics/btz431 |
| PMID | 28887402, 31134279 |

## 功能概述

ExpansionHunter 用于从 PCR-free 全基因组测序数据中估计短串联重复序列（STR）的大小，广泛应用于：

- **临床遗传学**: 重复扩展疾病诊断
- **脆性 X 综合征**: FMR1 基因 CGG 重复检测
- **亨廷顿病**: HTT 基因 CAG 重复检测
- **肌萎缩侧索硬化症 (ALS)**: C9orf72 基因 GGGGCC 重复
- **脊髓小脑共济失调**: 多种 SCA 亚型检测
- **弗里德赖希共济失调**: FXN 基因 GAA 重复

## 输入格式

| 格式 | 说明 |
|------|------|
| BAM/CRAM | PCR-free WGS 比对文件（需排序和索引） |
| FASTA | 参考基因组，必须与比对参考一致 |
| JSON | 变异目录，定义要检测的重复位点 |

## 分析模式

| 模式 | 说明 |
|------|------|
| Seeking | 使用 BAM 索引定位特定读段，适合小型目录（<100 位点） |
| Streaming | 单次读取整个文件，适合大型目录，内存需求更高 |

## 关键参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| sex | female | 样本性别，仅影响性染色体上的重复 |
| analysis_mode | seeking | 分析模式选择 |
| min_locus_coverage | 10 | 位点最小覆盖深度 |
| region_extension_length | 1000 | 搜索信息性读段的区域扩展长度 |

## 输出文件

| 文件类型 | 说明 |
|----------|------|
| VCF | 标准 VCF 格式的基因型结果 |
| JSON | 详细的分析结果，包含更多信息 |
| BAM (可选) | 包含重比对读段的 BAMlet 文件 |

## Docker 容器

自建镜像：

```bash
cd docker
docker build -t expansionhunter:5.0.0 .
```

## 文件结构

```
expansionhunter/
├── docker/
│   └── Dockerfile
├── expansionhunter.xml
├── tool_conf.xml
├── test-data/
├── README.md
└── README_CN.md
```

## 变异目录

Illumina 提供了常见病理性重复的目录文件，可从以下地址获取：
- https://github.com/Illumina/RepeatCatalogs

## 引用

如果您在研究中使用了此工具，请引用：

> Dolzhenko E, et al. Detection of long repeat expansions from PCR-free whole-genome sequence data. Genome Res. 2017;27(11):1895-1903. doi:10.1101/gr.225672.117

> Dolzhenko E, et al. ExpansionHunter: a sequence-graph based tool to analyze variation in short tandem repeat regions. Bioinformatics. 2019;35(22):4754-4756. doi:10.1093/bioinformatics/btz431

## 相关链接

- GitHub: https://github.com/Illumina/ExpansionHunter
- 文档: https://github.com/Illumina/ExpansionHunter/tree/master/docs
- RepeatCatalogs: https://github.com/Illumina/RepeatCatalogs

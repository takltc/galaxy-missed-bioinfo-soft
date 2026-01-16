# MitoZ Galaxy Wrapper

[English](README.md)

MitoZ 是一个用于动物线粒体基因组组装、注释和可视化的综合性工具包。

## 软件信息

| 属性 | 值 |
|------|-----|
| 版本 | 3.6 |
| 开发者 | Guanliang Meng (BGI-Shenzhen) |
| 许可证 | GPL-3.0 |
| DOI | 10.1093/nar/gkz173 |
| PMID | 30864657 |
| GitHub | https://github.com/linzhi2013/MitoZ |

## 工具组件

### MitoZ All-in-One (mitoz_all)

一站式解决方案，从原始 FASTQ 数据到完整的线粒体基因组注释：

1. **数据过滤**: 使用 fastp 清洗原始数据
2. **从头组装**: 使用 MEGAHIT 或 SPAdes 组装
3. **序列识别**: 使用 HMM profiles 识别线粒体序列
4. **基因注释**: 注释 PCGs、tRNAs 和 rRNAs
5. **可视化**: 生成 Circos 图

## 工作流程

```
Raw FASTQ files (PE or SE)
         │
         ▼
    Data Filtering (fastp)
         │
         ▼
    De novo Assembly (MEGAHIT/SPAdes)
         │
         ▼
    Mitogenome Identification (HMMER)
         │
         ▼
    Gene Annotation (PCGs + tRNAs + rRNAs)
         │
         ▼
    Visualization (Circos)
         │
         ▼
    Annotated Mitogenome + GenBank + Circos Plot
```

## 支持的物种分类

| 分类群 | 遗传密码 | 说明 |
|--------|----------|------|
| Chordata | 2 | 脊椎动物 (哺乳类、鸟类、爬行类、两栖类、鱼类) |
| Arthropoda | 5 | 节肢动物 (昆虫、甲壳类、蛛形纲) |

## 最佳实践参数

基于 Meng et al. (2019) 论文和作者建议：

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| data_size | 0.3-3 Gbp | 先尝试小数据量，失败后再增加 |
| kmers_megahit | 59 79 99 119 141 | 优先使用较大的 k-mer |
| fastq_read_length | 100-200bp | 短读长测序 |
| memory | 50 GB | MEGAHIT 最大内存 |

## 输入格式

- **FASTQ**: Paired-end 或 Single-end 数据
- **支持压缩**: gzip 压缩格式 (.gz)
- **平台**: Illumina, BGI-SEQ 等短读长平台

## 输出文件

| 文件 | 格式 | 说明 |
|------|------|------|
| mitogenome.fasta | FASTA | 组装的线粒体基因组序列 |
| annotation.gbf | GenBank | 完整的基因注释文件 |
| visualization.svg | SVG | Circos 可视化图 (矢量) |
| visualization.png | PNG | Circos 可视化图 (位图) |
| cds.fasta | FASTA | 蛋白编码基因序列 |
| trna.fasta | FASTA | tRNA 基因序列 |
| rrna.fasta | FASTA | rRNA 基因序列 |
| summary.txt | TXT | 组装和注释统计摘要 |
| overlap_info.txt | TXT | 环状验证信息 |

## Docker 容器

使用官方预构建镜像：
```bash
docker pull guanliangmeng/mitoz:3.6
```

或使用本目录下的 Dockerfile 自行构建：
```bash
cd docker
docker build -t mitoz:3.6 .
```

## 使用示例

### 基本用法 (Paired-end 数据)
```bash
mitoz all \
    --outprefix sample1 \
    --thread_number 16 \
    --clade Chordata \
    --genetic_code 2 \
    --fq1 sample1_R1.fq.gz \
    --fq2 sample1_R2.fq.gz \
    --fastq_read_length 150 \
    --data_size_for_mt_assembly 3,0 \
    --assembler megahit \
    --kmers_megahit 59 79 99 119 141 \
    --memory 50 \
    --requiring_taxa Chordata
```

### 小数据量快速测试
```bash
mitoz all \
    --outprefix sample1 \
    --thread_number 8 \
    --clade Chordata \
    --genetic_code 2 \
    --fq1 sample1_R1.fq.gz \
    --fq2 sample1_R2.fq.gz \
    --fastq_read_length 150 \
    --data_size_for_mt_assembly 0.3,0 \
    --assembler megahit \
    --kmers_megahit 43 71 99 \
    --memory 8
```

## 常见问题

### 1. 线粒体基因组不完整
- 尝试使用更少的数据 (0.3 Gbp)
- 尝试不同的 k-mer 大小

### 2. 缺少 tRNA 注释
- 确保 shell 为 bash
- 检查 MitoZ 版本 (建议使用 3.6)

### 3. 内存不足
- 减少 `--memory` 参数
- 减少 `--data_size_for_mt_assembly`

## 文件结构

```
mitoz/
├── docker/
│   └── Dockerfile
├── mitoz_all.xml
├── tool_conf.xml
├── README.md
└── README_CN.md
```

## 引用

如果您在研究中使用了此工具，请引用：

> Meng G, Li Y, Yang C, Liu S. MitoZ: a toolkit for animal mitochondrial genome 
> assembly, annotation and visualization. Nucleic Acids Research. 2019;47(11):e63.
> https://doi.org/10.1093/nar/gkz173

## 相关软件引用

MitoZ 内部调用了多个软件，请同时引用：
- fastp (数据过滤)
- MEGAHIT/SPAdes (组装)
- HMMER (序列识别)
- Circos (可视化)
- 详见: https://github.com/linzhi2013/MitoZ/wiki/Citations

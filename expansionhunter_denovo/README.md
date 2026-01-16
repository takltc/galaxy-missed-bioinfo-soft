# ExpansionHunter Denovo Galaxy Wrapper

ExpansionHunter Denovo (EHdn) 是一套用于检测短串联重复序列 (STR) 新型扩增的工具。

## 软件信息

- **版本**: 0.9.0
- **开发者**: Illumina
- **许可证**: Apache License 2.0
- **原始论文**: Dolzhenko E, et al. (2020) Genome Biology
- **DOI**: 10.1186/s13059-020-02017-z
- **PMID**: 32345345

## 工具组件

### 1. Profile (expansionhunter_denovo_profile)
从 BAM/CRAM 文件生成 STR profile，包含：
- 锚定的重复内读段 (Anchored IRRs)
- 配对的重复内读段 (Paired IRRs)

### 2. Merge (expansionhunter_denovo_merge)
合并多个样本的 STR profiles 用于队列分析。

### 3. Locus Analysis (expansionhunter_denovo_locus)
基于基因组位点的统计分析：
- Case-Control 分析
- Outlier 分析

### 4. Motif Analysis (expansionhunter_denovo_motif)
基于重复基序的统计分析：
- 识别特定基序的整体富集
- 适用于未知具体位置的情况

## 工作流程

```
BAM/CRAM files
      │
      ▼
   Profile (per sample)
      │
      ▼
   Merge (combine all)
      │
      ▼
  Locus/Motif Analysis
      │
      ▼
  Ranked candidate expansions
```

## 最佳实践参数

基于 Dolzhenko et al. (2020) 论文的建议：

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| min-anchor-mapq | 50 | 锚定读段的最小 MAPQ |
| max-irr-mapq | 40 | 重复内读段的最大 MAPQ |
| 测序深度 | 30-40x | 全基因组测序 |
| 读长 | 100-200bp | 短读长测序 |

## Docker 容器

使用 Bioconda 预构建镜像：
```bash
docker pull quay.io/biocontainers/expansionhunterdenovo:0.9.0--h6ac36c1_11
```

或使用本目录下的 Dockerfile 自行构建：
```bash
cd docker
docker build -t expansionhunterdenovo:0.9.0 .
```

> **注意**: 自建 Dockerfile 使用独立的 conda 环境指定 Python 3.9，以解决 `backports.lzma` 依赖问题。

## 文件结构

```
expansionhunter_denovo/
├── docker/
│   └── Dockerfile
├── expansionhunter_denovo_profile.xml
├── expansionhunter_denovo_merge.xml
├── expansionhunter_denovo_locus.xml
├── expansionhunter_denovo_motif.xml
├── tool_conf.xml
└── README.md
```

## 引用

如果您在研究中使用了此工具，请引用：

> Dolzhenko E, Bennett MF, Richmond PA, et al. ExpansionHunter Denovo: a computational method for locating known and novel repeat expansions in short-read sequencing data. Genome Biol. 2020;21(1):102. doi:10.1186/s13059-020-02017-z

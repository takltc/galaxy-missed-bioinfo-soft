# GangSTR Galaxy Wrapper

[English](README.md)

全基因组串联重复序列 (STR) 分析工具的 Galaxy 集成。

## 软件信息

| 属性 | 值 |
|------|-----|
| 版本 | 2.5.0 |
| 开发者 | Gymrek Lab (UCSD) |
| 许可证 | GNU GPL v3 |
| DOI | 10.1093/nar/gkz501 |
| PMID | 31165139 |

## 功能概述

GangSTR 用于从短读长测序数据中进行全基因组串联重复序列（STR）分析，关键优势是能够处理**超过读长的重复序列**。广泛应用于：

- **全基因组 STR 分析**: 一次性分析数十万个 STR 位点
- **疾病位点检测**: 靶向模式用于特定疾病相关位点
- **群体遗传学**: STR 变异的群体研究
- **进化研究**: STR 突变率和多态性分析

## 工作原理

GangSTR 使用概率模型，综合考虑以下几类读段：

| 读段类型 | 说明 |
|----------|------|
| Spanning reads | 跨越整个重复区域的读段 |
| Flanking reads | 部分覆盖重复区域的读段 |
| Enclosing reads | 完全包含在重复区域内的读段 |
| FRR | 完全由重复序列组成的读段 |

## 输入格式

| 格式 | 说明 |
|------|------|
| BAM | 比对后的测序数据（支持多样本） |
| FASTA | 参考基因组 |
| BED | 目标 STR 区域定义 |

## 运行模式

| 模式 | 说明 |
|------|------|
| 全基因组 | 默认模式，适用于 WGS 数据 |
| 靶向模式 | 使用 --targeted，适用于疾病位点检测 |

## 关键参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| targeted | false | 靶向模式开关 |
| readlength | 自动检测 | 读段长度 |
| coverage | 自动计算 | 平均覆盖度 |
| stutterup | 0.05 | Stutter 插入概率 |
| stutterdown | 0.05 | Stutter 删除概率 |

## 输出文件

| 文件类型 | 说明 |
|----------|------|
| VCF | 包含每个位点的基因型信息 (GT, DP, Q, REPCN, REPCI, RC) |
| Sample Stats | 样本级别的统计信息 |

## Docker 容器

自建镜像：

```bash
cd docker
docker build -t gangstr:2.5.0 .
```

## 文件结构

```
gangstr/
├── docker/
│   └── Dockerfile
├── gangstr.xml
├── tool_conf.xml
├── test-data/
├── README.md
└── README_CN.md
```

## 参考区域文件

GangSTR 提供了预构建的参考区域文件：
- https://github.com/gymreklab/GangSTR#references

BED 文件格式要求：
- chrom: 染色体
- start: 起始位置
- end: 结束位置
- period: 重复单元长度
- ref_copy: 参考基因组中的重复次数

## 引用

如果您在研究中使用了此工具，请引用：

> Mousavi N, Shleizer-Burko S, Yanicky R, Gymrek M. Profiling the genome-wide landscape of tandem repeat expansions. Nucleic Acids Res. 2019;47(15):e90. doi:10.1093/nar/gkz501

## 相关链接

- GitHub: https://github.com/gymreklab/GangSTR
- Wiki: https://github.com/gymreklab/GangSTR/wiki
- Gymrek Lab: https://gymreklab.com/

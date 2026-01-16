# Mutserve Galaxy Wrapper

Mutserve 是一个专用于线粒体 DNA (mtDNA) 变异检测的工具，可以检测同质性 (homoplasmic) 和异质性 (heteroplasmic) 位点。

## 软件信息

- **版本**: 2.0.0-rc15
- **开发者**: Sebastian Schönherr, Hansi Weissensteiner, Lukas Forer (Genepi Innsbruck)
- **许可证**: MIT License
- **GitHub**: https://github.com/seppinho/mutserve
- **原始论文**: Weissensteiner H, et al. (2021) Genome Research
- **DOI**: 10.1101/gr.256545.119
- **PMID**: 33452015

## 工具组件

### 1. Mutserve Call (mutserve_call)
从 BAM/CRAM 文件检测 mtDNA 变异：
- 同质性变异 (homoplasmic): 所有 mtDNA 拷贝中都存在
- 异质性变异 (heteroplasmic): 仅在部分 mtDNA 拷贝中存在

### 2. Mutserve Annotate (mutserve_annotate)
对检测到的变异进行功能注释：
- 基因/区域分配
- 氨基酸变化
- tRNA/rRNA 注释

## 工作流程

```
BAM/CRAM (mtDNA aligned)
         │
         ▼
   Mutserve Call
         │
         ├──→ VCF (主输出)
         │
         └──→ Raw Data (可选)
                  │
                  ▼
         Mutserve Annotate
                  │
                  ▼
         Annotated Variants
```

## 最佳实践参数

基于文献研究 (PMID: 35350246) 的建议：

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| heteroplasmy_level | 0.01-0.05 | 异质性检测阈值 (1-5%) |
| mapQ | 20 | 最小比对质量 |
| baseQ | 20 | 最小碱基质量 |
| alignQ | 30 | 最小比对质量 |

### 异质性阈值选择

- **1% (0.01)**: 高灵敏度，适用于研究目的
- **5% (0.05)**: 平衡灵敏度和特异性，推荐用于临床应用
- **10% (0.10)**: 高特异性，适用于污染敏感的研究

## 基准测试性能

根据 Ip et al. (2022) Front Genet 的系统评估：
- Mutserve 在合成基准数据集上表现最佳 (F1 score = 0.74)
- 同质性变异检测准确率高且一致
- 异质性变异检测在 1-5% 阈值下表现稳定

## Docker 容器

使用本目录下的 Dockerfile 构建：
```bash
cd docker
docker build -t omniverse/mutserve:2.0.0-rc15 .
```

## 参考序列

推荐使用 rCRS (revised Cambridge Reference Sequence)：
- 序列: NC_012920.1
- 长度: 16,569 bp
- 下载: https://raw.githubusercontent.com/seppinho/mutserve/master/files/rCRS.fasta

## 文件结构

```
mutserve/
├── docker/
│   └── Dockerfile
├── test-data/
├── mutserve_call.xml
├── mutserve_annotate.xml
├── tool_conf.xml
└── README.md
```

## 引用

如果您在研究中使用了此工具，请引用：

> Weissensteiner H, Forer L, Fendt L, Kheirkhah A, Salas A, Kronenberg F, Schoenherr S. Contamination detection in sequencing studies using the mitochondrial phylogeny. Genome Res. 2021;31:309-316. doi:10.1101/gr.256545.119

> Weissensteiner H, Forer L, Fuchsberger C, Schöpf B, Kloss-Brandstätter A, Specht G, Kronenberg F, Schönherr S. mtDNA-Server: next-generation sequencing data analysis of human mitochondrial DNA in the cloud. Nucleic Acids Res. 2016;44:W64-9. doi:10.1093/nar/gkw247

## 相关工具

- **Haplocheck**: 使用 Mutserve 进行污染检测
- **Haplogrep**: mtDNA 单倍群分类
- **mtDNA-Server 2**: 完整的 mtDNA 分析流水线

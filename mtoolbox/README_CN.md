# MToolBox Annotate

## 概述
使用 MToolBox 框架对线粒体 DNA 变异进行全面注释。

## 描述
MToolBox Annotate 为 mtDNA 变异分配致病性评分和功能注释。它集成了多个权威数据库的数据：
- **MITOMAP**：经专家确认的疾病关联。
- **HmtDB**：群体变异性。
- **ClinVar**：临床意义。
- **gnomAD-mtDNA**：群体频率。

它还可以选择性地应用 **ACMG/AMP mtDNA 特异性标准** (PMID:32906214) 将变异分类为致病、可能致病、VUS、可能良性或良性。

## 输入
- **Input VCF**：包含 mtDNA 变异的 VCF 文件（需比对到 rCRS）。

## 输出
- **Annotated VCF**：已填充 INFO 字段（例如 `MITOMAP_DISEASE`、`ACMG_CLASS`）的 VCF。
- **Clinical Report**：总结致病发现的 HTML 报告。
- **Annotation Report**：用于下游处理的 JSON 格式报告。

## 参考文献
- Calabrese C, et al. MToolBox: a highly automated pipeline for heteroplasmy annotation and prioritization analysis of human mitochondrial variants. Bioinformatics. 2014. PMID:25028726

# mtDNA Fusion Merger

## 概述
将 Mutserve 和 Mutect2 的 mtDNA 变异调用结果使用 "Fusion" 策略进行合并，这是 mtDNA-Server 2 中描述的方法。

## 描述
此工具实现了一种专门针对线粒体 DNA 设计的集成变异调用策略。它合并了两个领先的调用器的变异结果：
- **Mutserve**：对 SNV 具有很高的准确性。
- **Mutect2**：更好地支持 INDEL。

**Fusion 模式**（推荐）优先使用 Mutserve 的 SNV 和 Mutect2 的 INDEL，并在冲突时优先选择 INDEL。这种策略在基准测试中被证明可以实现灵敏度和特异性（F1-score）的最佳平衡 (PMID:38709886)。

## 输入
- **Mutserve VCF**：Mutserve Call 的输出。
- **Mutect2 VCF**：GATK Mutect2（线粒体模式）的输出。

## 输出
- **Merged VCF**：包含 `FUSION_SOURCE` 和 `FUSION_CONFIDENCE` 标签的合并变异结果。
- **Fusion Report**：合并过程的 JSON 摘要报告。

## 参考文献
- Weissensteiner H, et al. mtDNA-Server 2: advancing mitochondrial DNA analysis through highly parallelized data processing and interactive analytics. Nucleic Acids Res. 2024. PMID:38709886

# mtDNA Fusion Merger

## Overview
Merge Mutserve and Mutect2 mtDNA variant calls using the "Fusion" strategy described in mtDNA-Server 2.

## Description
This tool implements an ensemble variant calling strategy specifically designed for mitochondrial DNA. It merges variant calls from two leading callers:
- **Mutserve**: High accuracy for SNVs.
- **Mutect2**: Better support for INDELs.

The **Fusion Mode** (recommended) prioritizes SNVs from Mutserve and INDELs from Mutect2, resolving conflicts in favor of INDELs. This strategy has been shown to achieve the best balance of sensitivity and specificity (F1-score) in benchmarks (PMID:38709886).

## Inputs
- **Mutserve VCF**: Output from Mutserve Call.
- **Mutect2 VCF**: Output from GATK Mutect2 (mitochondria mode).

## Outputs
- **Merged VCF**: Consolidated calls with `FUSION_SOURCE` and `FUSION_CONFIDENCE` tags.
- **Fusion Report**: JSON summary of the merge process.

## References
- Weissensteiner H, et al. mtDNA-Server 2: advancing mitochondrial DNA analysis through highly parallelized data processing and interactive analytics. Nucleic Acids Res. 2024. PMID:38709886

# MToolBox Annotate

## Overview
Comprehensive annotation for mitochondrial DNA variants using the MToolBox framework.

## Description
MToolBox Annotate assigns pathogenicity scores and functional annotations to mtDNA variants. It integrates data from multiple authoritative databases:
- **MITOMAP**: Confirmed disease associations.
- **HmtDB**: Population variability.
- **ClinVar**: Clinical significance.
- **gnomAD-mtDNA**: Population frequencies.

It also optionally applies **ACMG/AMP mtDNA-specific criteria** (PMID:32906214) to classify variants as Pathogenic, Likely Pathogenic, VUS, Likely Benign, or Benign.

## Inputs
- **Input VCF**: VCF file with mtDNA variants (rCRS aligned).

## Outputs
- **Annotated VCF**: VCF with INFO fields populated (e.g., `MITOMAP_DISEASE`, `ACMG_CLASS`).
- **Clinical Report**: HTML report summarizing pathogenic findings.
- **Annotation Report**: JSON format for downstream processing.

## References
- Calabrese C, et al. MToolBox: a highly automated pipeline for heteroplasmy annotation and prioritization analysis of human mitochondrial variants. Bioinformatics. 2014. PMID:25028726

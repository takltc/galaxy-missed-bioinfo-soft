# PLINK2 Galaxy Wrapper

[中文版](README_CN.md)

Galaxy integration for genotype data quality control and population stratification analysis.

## Software Information

| Property | Value |
|----------|-------|
| Version | 2.0 |
| Developer | Christopher Chang |
| License | GNU GPL v3 |
| DOI | 10.1186/s13742-015-0047-8 |
| PMID | 25722852 |

## Overview

PLINK2 is a comprehensive rewrite of PLINK 1.9, providing significant performance improvements and new features. This wrapper provides essential functions for PRS workflows:

- **Quality Control (QC)**: MAF, missing rate, and HWE filtering
- **Principal Component Analysis (PCA)**: Population stratification correction
- **Allele Frequency Calculation**: Per-variant allele frequencies

## Best Practice Parameters (from UK Biobank studies)

| Parameter | Recommended Value | Literature Source |
|-----------|------------------|-------------------|
| MAF | ≥0.01 | PMID:35251129 |
| geno | ≤0.02 | PMID:35251129 |
| mind | ≤0.02 | PMID:35251129 |
| HWE | ≥1e-6 | PMID:35251129 |
| PCA | 10 PCs | PMID:39425790 |

## Input Formats

| Format | Description |
|--------|-------------|
| VCF | Standard variant call format |
| PLINK binary | .bed (genotypes), .bim (variants), .fam (samples) |

## Output Files

| Mode | Output Files |
|------|--------------|
| QC | Filtered PLINK binary (.bed/.bim/.fam) |
| PCA | Eigenvectors (.eigenvec), Eigenvalues (.eigenval) |
| Freq | Allele frequency table (.afreq) |

## Docker Container

Build custom image:

```bash
cd docker
docker build -t plink2:2.0 .
```

## File Structure

```
plink2/
├── docker/
│   └── Dockerfile
├── plink2.xml
├── tool_conf.xml
├── test-data/
├── README.md
└── README_CN.md
```

## Citations

If you use this tool in your research, please cite:

> Chang CC, Chow CC, Tellier LC, Vattikuti S, Purcell SM, Lee JJ. Second-generation PLINK: rising to the challenge of larger and richer datasets. Gigascience. 2015;4:7. doi:10.1186/s13742-015-0047-8

## Links

- Official Site: https://www.cog-genomics.org/plink/2.0/
- GitHub: https://github.com/chrchang/plink-ng

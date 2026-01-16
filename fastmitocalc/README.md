# fastMitoCalc Galaxy Wrapper

[中文版](README_CN.md)

Galaxy integration for ultra-fast mitochondrial DNA copy number estimation from whole-genome sequencing data.

## Software Information

| Property | Value |
|----------|-------|
| Version | 1.0.0 |
| Developer | Yong Qian, Jun Ding et al. (NIA/NIH) |
| License | Not specified |
| GitHub | https://github.com/qian0001/fastMitoCalc |
| DOI | 10.1093/bioinformatics/btx167 |
| PMID | 28453676 |

## Overview

fastMitoCalc is an ultra-fast program to estimate mitochondrial DNA (mtDNA) copy number from whole-genome sequencing (WGS) data. It is approximately 100 times faster than the original mitoCalc program and can analyze an individual BAM file (with 4X average coverage for nuclear DNA) in less than a minute.

### Key Features

- **Ultra-fast processing**: ~100x faster than original mitoCalc
- **Minimal requirements**: Works with 4X average nuclear DNA coverage
- **Flexible methods**: Random regions, specific chromosome, or custom BED file
- **Large-scale studies**: Suitable for processing thousands of samples

## Algorithm

mtDNA copy number is calculated as:

```
mtDNA-CN = 2 × (mtDNA coverage / nuclear DNA coverage)
```

The factor of 2 accounts for the diploid nuclear genome vs. the haploid mitochondrial genome.

## Workflow

```
FASTQ (WGS)
     │
     ▼
  BWA-MEM
     │
     ▼
BAM (indexed)
     │
     ├──────────────────┐
     │                  │
     ▼                  ▼
fastMitoCalc      Mutserve Call
     │                  │
     ▼                  ▼
mtDNA Copy       VCF (variants)
Number Report          │
                       ├──────────────┐
                       │              │
                       ▼              ▼
                  Haplocheck    Haplogrep3
                       │              │
                       ▼              ▼
                Contamination   Haplogroup
                   Report      Classification
```

## Input Requirements

| Format | Requirements |
|--------|-------------|
| BAM | Coordinate-sorted, indexed (.bai required) |
| Coverage | Minimum 4X average nuclear DNA coverage |
| Reference | Consistent chromosome naming |

## Output

Tab-delimited report with the following columns:

| Column | Description |
|--------|-------------|
| mt_copy_number_avg | Estimated mtDNA copy number |
| mt_coverage | Average mtDNA sequencing coverage |
| autosomal_coverage | Average nuclear DNA coverage |
| actual_basepairs_covered | Total bases covered by reads |
| chrom_used_for_autosomal_coverage | Chromosomes used for calculation |

## Coverage Estimation Methods

### 1. Random Regions (Default, Fastest)

Randomly selects N regions of specified size from autosomes:
- Default: 3000 regions of 1000 bp each
- Provides robust estimation with minimal computation

### 2. Specific Chromosome

Uses entire chromosome for nuclear coverage estimation:
- Chromosome 22 commonly used (smaller size)
- More thorough but slower

### 3. Custom BED File

User-defined regions for nuclear coverage estimation:
- Useful for specialized analyses
- Package includes 1000G off-target regions for WES data

## Best Practice Parameters

Based on literature research:

| Parameter | Recommended Value | Description |
|-----------|-------------------|-------------|
| num_regions | 3000 | Number of random regions (default) |
| region_size | 1000 | Size of each region in bp (default) |
| Coverage | ≥4X | Minimum nuclear DNA coverage |

### Chromosome Naming

| Reference | Autosomes | Mitochondria |
|-----------|-----------|--------------|
| GRCh37/38 | 1, 2, ... 22 | MT |
| hg19/38 | chr1, chr2, ... | chrM |

## Typical mtDNA Copy Number Values

| Tissue | mtDNA-CN Range |
|--------|----------------|
| Blood (PBMC) | 50-500 |
| Heart | 1000-10000 |
| Liver | 500-5000 |
| Muscle | 1000-6000 |
| Brain | 500-3000 |

## Clinical Applications

mtDNA copy number has been used as a biomarker in:

- **Alzheimer's disease**: Lower mtDNA-CN associated with increased AD risk
- **Parkinson's disease**: Elevated cerebellum mtDNA-CN in PD patients
- **Cardiovascular disease**: Inverse association with CHD risk
- **Aging**: Decline after 65 years of age
- **Asthma**: Higher mtDNA-CN associated with reduced exacerbation risk

## Docker Container

Build using the Dockerfile in this directory:

```bash
cd docker
docker build -t omniverse/fastmitocalc:1.0.0 .

# Test
docker run --rm omniverse/fastmitocalc:1.0.0 perl /opt/fastMitoCalc/fastMitoCalc.pl
```

## File Structure

```
fastmitocalc/
├── docker/
│   └── Dockerfile
├── fastmitocalc.xml
├── tool_conf.xml
├── README.md
└── README_CN.md
```

## Related Tools

- **Mutserve**: mtDNA variant caller
- **Haplocheck**: Contamination detection
- **Haplogrep3**: mtDNA haplogroup classification
- **mitoAnalyzer**: Original mtDNA analysis pipeline from the same developers

## Citations

If you use this tool in your research, please cite:

> Qian Y, Butler TJ, Opsahl-Ong K, Giroux NS, Sidore C, Nagaraja R, Cucca F, Ferrucci L, Abecasis GR, Schlessinger D, Ding J. fastMitoCalc: an ultra-fast program to estimate mitochondrial DNA copy number from whole-genome sequences. Bioinformatics. 2017 May 1;33(9):1399-1401. doi:10.1093/bioinformatics/btx167

## Links

- GitHub: https://github.com/qian0001/fastMitoCalc
- Original mitoAnalyzer: https://lgsun.irp.nia.nih.gov/hsgu/software/mitoanalyzer/index.html
- PubMed: https://pubmed.ncbi.nlm.nih.gov/28453676/

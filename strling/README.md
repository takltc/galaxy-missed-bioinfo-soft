# STRling Galaxy Wrapper

[中文版](README_CN.md)

Galaxy integration for the Short Tandem Repeat (STR) expansion detection tool, supporting both known and novel loci.

## Software Information

| Property | Value |
|----------|-------|
| Version | 0.6.0 |
| Developer | Quinlan Lab (University of Utah) |
| License | MIT |
| DOI | 10.1186/s13059-022-02826-4 |
| PMID | 36474232 |

## Overview

STRling (pronounced like "sterling") is a method for detecting large short tandem repeat (STR) expansions from short-read sequencing data using a k-mer counting approach. Key features:

- **Novel STR Expansion Detection**: Detects STR expansions not present in the reference genome
- **Known Loci Detection**: Also detects annotated STR expansions in the reference
- **K-mer Counting**: Uses k-mer counting to recover mismapped STR reads
- **Base-pair Level Precision**: Uses soft-clipped reads to precisely locate expansion insertion points

## Clinical Applications

STRling is particularly suitable for detecting repeat expansions causing:

| Disease | Gene | Repeat Unit |
|---------|------|-------------|
| CANVAS | RFC1 | AAGGG |
| Huntington's Disease | HTT | CAG |
| Friedreich's Ataxia | FXN | GAA |
| Fragile X Syndrome | FMR1 | CGG |
| Myotonic Dystrophy | DMPK/CNBP | CTG/CCTG |
| Spinocerebellar Ataxias | Various | Various |

Plus 40+ other STR-related diseases.

## Input Formats

| Format | Description |
|--------|-------------|
| BAM/CRAM | PCR-free WGS aligned reads (must be sorted and indexed) |
| FASTA | Reference genome (GRCh38 recommended) |

## Workflow

STRling workflow consists of three main steps:

```
BAM/CRAM files
      │
      ▼
   Extract (extract STR-containing reads)
      │
      ▼
   Call (call STR expansions)
      │
      ▼
   Output results
```

## Key Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| min_support | 5 | Minimum supporting reads to call an STR expansion |
| min_cluster_reads | 2 | Minimum reads in a cluster to report a locus |

## Output Files

| File Type | Description |
|-----------|-------------|
| Bounds | STR locus boundary information with detected expansion locations |
| Genotype | Genotype estimates including allele size estimates |
| Unplaced | STR read counts that couldn't be assigned to specific loci |

## Performance Metrics

According to the original paper validation:

| Metric | Individual Calling | Joint Calling |
|--------|-------------------|---------------|
| Sensitivity | 87.2% | 98.9% |
| Position Accuracy | - | Average error 6.14 bp |
| FDR | - | 0.078 |

## Docker Container

Build custom image:

```bash
cd docker
docker build -t strling:0.6.0 .
```

**Note**: STRling only supports linux/amd64 architecture.

## File Structure

```
strling/
├── docker/
│   └── Dockerfile
├── strling.xml
├── tool_conf.xml
├── test-data/
├── README.md
└── README_CN.md
```

## Citations

If you use this tool in your research, please cite:

> Dashnow H, Pedersen BS, Hiatt L, et al. STRling: a k-mer counting approach that detects short tandem repeat expansions at known and novel loci. Genome Biol. 2022;23(1):257. doi:10.1186/s13059-022-02826-4

## Links

- GitHub: https://github.com/quinlan-lab/STRling
- Documentation: https://strling.readthedocs.io/
- Quinlan Lab: https://quinlanlab.org/

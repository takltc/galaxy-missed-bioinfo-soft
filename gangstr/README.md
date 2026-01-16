# GangSTR Galaxy Wrapper

[中文版](README_CN.md)

Galaxy integration for the genome-wide Short Tandem Repeat (STR) profiling tool.

## Software Information

| Property | Value |
|----------|-------|
| Version | 2.5.0 |
| Developer | Gymrek Lab (UCSD) |
| License | GNU GPL v3 |
| DOI | 10.1093/nar/gkz501 |
| PMID | 31165139 |

## Overview

GangSTR performs genome-wide tandem repeat sequence (STR) analysis from short-read sequencing data. Its key advantage is the ability to handle **repeats longer than read length**. It is widely used for:

- **Genome-wide STR Analysis**: Analyze hundreds of thousands of STR loci in one run
- **Disease Locus Detection**: Targeted mode for specific disease-related loci
- **Population Genetics**: Population studies of STR variation
- **Evolutionary Studies**: STR mutation rates and polymorphism analysis

## How It Works

GangSTR uses a probabilistic model considering several read classes:

| Read Type | Description |
|-----------|-------------|
| Spanning reads | Reads spanning the entire repeat region |
| Flanking reads | Reads partially covering the repeat region |
| Enclosing reads | Reads completely contained within the repeat region |
| FRR | Fully Repetitive Reads composed entirely of repeat sequence |

## Input Formats

| Format | Description |
|--------|-------------|
| BAM | Aligned sequencing data (supports multiple samples) |
| FASTA | Reference genome |
| BED | Target STR region definitions |

## Running Modes

| Mode | Description |
|------|-------------|
| Genome-wide | Default mode, suitable for WGS data |
| Targeted | Use --targeted flag, suitable for disease locus detection |

## Key Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| targeted | false | Targeted mode switch |
| readlength | auto-detected | Read length |
| coverage | auto-calculated | Average coverage |
| stutterup | 0.05 | Stutter insertion probability |
| stutterdown | 0.05 | Stutter deletion probability |

## Output Files

| File Type | Description |
|-----------|-------------|
| VCF | Genotype information per locus (GT, DP, Q, REPCN, REPCI, RC) |
| Sample Stats | Sample-level statistics |

## Docker Container

Build custom image:

```bash
cd docker
docker build -t gangstr:2.5.0 .
```

## File Structure

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

## Reference Region Files

GangSTR provides pre-built reference region files:
- https://github.com/gymreklab/GangSTR#references

BED file format requirements:
- chrom: Chromosome
- start: Start position
- end: End position
- period: Repeat unit length
- ref_copy: Reference copy number

## Citations

If you use this tool in your research, please cite:

> Mousavi N, Shleizer-Burko S, Yanicky R, Gymrek M. Profiling the genome-wide landscape of tandem repeat expansions. Nucleic Acids Res. 2019;47(15):e90. doi:10.1093/nar/gkz501

## Links

- GitHub: https://github.com/gymreklab/GangSTR
- Wiki: https://github.com/gymreklab/GangSTR/wiki
- Gymrek Lab: https://gymreklab.com/

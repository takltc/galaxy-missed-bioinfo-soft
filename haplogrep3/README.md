# Haplogrep3 Galaxy Wrapper

[中文版](README_CN.md)

Galaxy integration for the mitochondrial DNA (mtDNA) haplogroup classification tool.

## Software Information

| Property | Value |
|----------|-------|
| Version | 3.2.2 |
| Developer | Innsbruck Medical University |
| License | MIT |
| DOI | 10.1093/nar/gkad284 |
| PMID | 37070190 |

## Overview

Haplogrep3 is used for haplogroup classification of human mitochondrial DNA, widely applied in:

- **Medical Genetics**: Mitochondrial disease diagnosis, disease association studies
- **Forensics**: Maternal lineage identification, missing persons cases
- **Evolutionary Studies**: Human population studies, migration pattern analysis
- **Population Genetics**: Ancestry tracing, demographic history reconstruction

## Input Formats

| Format | Description |
|--------|-------------|
| FASTA | Mitochondrial genome sequences (complete or partial) |
| VCF | Variant call format from sequencing or genotyping arrays |
| HSD | Tab-separated text format (Sample ID, Range, Variants) |

## Phylogenetic Trees

| Tree | Reference Sequence | Use Case |
|------|-------------------|----------|
| PhyloTree 17 Forensic Update 1.2 | rCRS | Forensic applications (recommended) |
| PhyloTree 17.2 | rCRS | Latest research-grade phylogeny |
| PhyloTree 17.0 | rCRS/RSRS | Standard analysis |
| PhyloTree 16.0/15.0 | rCRS | Backward compatibility |

## Key Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| tree | phylotree-fu-rcrs-1.2 | Phylogenetic tree selection |
| metric | kulczynski | Distance metric method |
| hits | 1 | Number of top N hits to output |
| hetLevel | 0.9 | Heteroplasmy level threshold (VCF) |

## Docker Container

Build custom image:

```bash
cd docker
docker build -t haplogrep3:3.2.2 .
```

## File Structure

```
haplogrep3/
├── docker/
│   └── Dockerfile
├── haplogrep3.xml
├── tool_conf.xml
├── README.md
└── README_CN.md
```

## Citations

If you use this tool in your research, please cite:

> Schönherr S, Weissensteiner H, Kronenberg F, Forer L. 
> Haplogrep 3 - an interactive haplogroup classification and analysis platform. 
> Nucleic Acids Res. 2023. doi:10.1093/nar/gkad284

## Links

- Web Service: https://haplogrep.i-med.ac.at
- GitHub: https://github.com/genepi/haplogrep3
- Documentation: https://haplogrep.readthedocs.io

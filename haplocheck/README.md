# Haplocheck Galaxy Wrapper

[中文版](README_CN.md)

Galaxy integration for the phylogeny-based contamination detection tool in mtDNA and WGS studies.

## Software Information

| Property | Value |
|----------|-------|
| Version | 1.3.3 |
| Developer | Sebastian Schönherr, Hansi Weissensteiner, Lukas Forer (Genepi Innsbruck) |
| License | MIT License |
| GitHub | https://github.com/genepi/haplocheck |
| DOI | 10.1101/gr.256545.119 |
| PMID | 33452015 |

## Overview

Haplocheck detects in-sample contamination in mtDNA and whole-genome sequencing (WGS) studies by analyzing the mitochondrial DNA content. It identifies contamination by detecting phylogenetically incompatible mitochondrial haplotypes observable as heteroplasmic (polymorphic) sites.

### Key Features

- Detects contamination down to 1% level (with sufficient coverage)
- Works with both mtDNA-targeted and WGS data
- Provides interactive HTML reports with phylogenetic tree visualization
- Can be used as a proxy for nuclear DNA contamination detection
- Fast processing: ~2,500 samples in <2 hours

## Workflow

```
BAM/CRAM (mtDNA aligned)
         │
         ▼
   Mutserve Call
         │
         ▼
    VCF (variants)
         │
         ├──────────────────┐
         │                  │
         ▼                  ▼
    Haplocheck         Haplogrep3
         │                  │
         ▼                  ▼
 Contamination      Haplogroup
    Report          Classification
```

## Input Requirements

| Format | Requirements |
|--------|-------------|
| VCF | Homoplasmies coded as "1/1", heteroplasmies as "0/1" with AF tag |
| Source | Mutserve Call output or GATK MuTect2 mitochondrial pipeline |

## Output Files

| File | Description |
|------|-------------|
| contamination.txt | Main report with contamination status, level, and haplogroups |
| contamination.raw.txt | Extended metrics (optional) |
| report.html | Interactive HTML report with phylogenetic trees (optional) |

## Contamination Report Columns

| Column | Description |
|--------|-------------|
| Sample | Sample identifier |
| Contamination Status | YES, NO, or ND (not detectable) |
| Distance | Phylogenetic distance between major/minor haplogroups |
| Contamination Level | Estimated contamination percentage |
| Sample Coverage | Mean mtDNA coverage |
| Major Haplogroup | Dominant haplogroup |
| Minor Haplogroup | Contaminating haplogroup |

## Best Practice Parameters

Based on literature research (PMID: 33452015):

| Parameter | Recommendation | Description |
|-----------|----------------|-------------|
| Coverage | ≥100x for 10% | ≥600x for 1% contamination detection |
| Quality | Haplogroup quality ≥0.5 | Required for reliable detection |
| Distance | Phylogenetic distance ≥2 | Minimum distance between haplogroups |

### Coverage Requirements for Detection

| Contamination Level | Minimum Coverage |
|--------------------|------------------|
| 10% | 100x |
| 5% | 200x |
| 1% | 600x |

## Contamination Scenarios

Haplocheck detects three contamination scenarios:

1. **Scenario A**: Two haplotypes branch into two different lineages
2. **Scenario B**: Minor haplotype is ancestral to major (same lineage)
3. **Scenario C**: Major haplotype is ancestral to minor (same lineage)

## Benchmark Performance

According to García-Olivares et al. (2021) Sci Rep (PMID: 34654896):

- Haplocheck stands out as the most complete tool for mtDNA analysis
- Accurate for both whole-genome sequencing (WGS) and whole-exome sequencing (WES)
- Successfully tested with Nanopore long-read sequencing data

## Docker Container

Build using the Dockerfile in this directory:

```bash
cd docker
docker build -t omniverse/haplocheck:1.3.3 .
```

## File Structure

```
haplocheck/
├── docker/
│   └── Dockerfile
├── haplocheck.xml
├── tool_conf.xml
├── README.md
└── README_CN.md
```

## Related Tools

- **Mutserve**: mtDNA variant caller (generates input VCF for Haplocheck)
- **Haplogrep3**: mtDNA haplogroup classification
- **mtDNA-Server 2**: Complete mtDNA analysis pipeline

## Limitations

- Cannot detect contamination between samples with identical haplogroups
- Very rare mega-NUMTs could cause false positive results
- Ancient DNA requires higher coverage due to DNA degradation

## Citations

If you use this tool in your research, please cite:

> Weissensteiner H, Forer L, Fendt L, Kheirkhah A, Salas A, Kronenberg F, Schoenherr S. 
> Contamination detection in sequencing studies using the mitochondrial phylogeny. 
> Genome Res. 2021;31:309-316. doi:10.1101/gr.256545.119

## Links

- Web Service: https://mitoverse.i-med.ac.at
- GitHub: https://github.com/genepi/haplocheck
- Documentation: https://mitoverse.readthedocs.io/haplocheck/haplocheck/

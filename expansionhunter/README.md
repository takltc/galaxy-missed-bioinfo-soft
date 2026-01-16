# ExpansionHunter Galaxy Wrapper

[中文版](README_CN.md)

Galaxy integration for the Short Tandem Repeat (STR) expansion detection tool.

## Software Information

| Property | Value |
|----------|-------|
| Version | 5.0.0 |
| Developer | Illumina |
| License | Apache License 2.0 |
| DOI | 10.1101/gr.225672.117, 10.1093/bioinformatics/btz431 |
| PMID | 28887402, 31134279 |

## Overview

ExpansionHunter estimates the size of short tandem repeat (STR) expansions from PCR-free whole-genome sequencing data. It is widely used for:

- **Clinical Genetics**: Diagnosis of repeat expansion disorders
- **Fragile X Syndrome**: FMR1 gene CGG repeat detection
- **Huntington's Disease**: HTT gene CAG repeat detection
- **ALS (Amyotrophic Lateral Sclerosis)**: C9orf72 gene GGGGCC repeat
- **Spinocerebellar Ataxias**: Detection of multiple SCA subtypes
- **Friedreich's Ataxia**: FXN gene GAA repeat

## Input Formats

| Format | Description |
|--------|-------------|
| BAM/CRAM | PCR-free WGS aligned reads (must be sorted and indexed) |
| FASTA | Reference genome (must match alignment reference) |
| JSON | Variant catalog defining repeat loci to detect |

## Analysis Modes

| Mode | Description |
|------|-------------|
| Seeking | Uses BAM index to locate specific reads, best for small catalogs (<100 loci) |
| Streaming | Single-pass read of entire file, best for large catalogs, higher memory |

## Key Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| sex | female | Sample sex, only affects repeats on sex chromosomes |
| analysis_mode | seeking | Analysis mode selection |
| min_locus_coverage | 10 | Minimum coverage depth at loci |
| region_extension_length | 1000 | Extension length for searching informative reads |

## Output Files

| File Type | Description |
|-----------|-------------|
| VCF | Standard VCF format genotype results |
| JSON | Detailed analysis results with additional information |
| BAM (optional) | BAMlet containing realigned reads |

## Docker Container

Build custom image:

```bash
cd docker
docker build -t expansionhunter:5.0.0 .
```

## File Structure

```
expansionhunter/
├── docker/
│   └── Dockerfile
├── expansionhunter.xml
├── tool_conf.xml
├── test-data/
├── README.md
└── README_CN.md
```

## Variant Catalogs

Illumina provides pre-built catalogs for common pathogenic repeats:
- https://github.com/Illumina/RepeatCatalogs

## Citations

If you use this tool in your research, please cite:

> Dolzhenko E, et al. Detection of long repeat expansions from PCR-free whole-genome sequence data. Genome Res. 2017;27(11):1895-1903. doi:10.1101/gr.225672.117

> Dolzhenko E, et al. ExpansionHunter: a sequence-graph based tool to analyze variation in short tandem repeat regions. Bioinformatics. 2019;35(22):4754-4756. doi:10.1093/bioinformatics/btz431

## Links

- GitHub: https://github.com/Illumina/ExpansionHunter
- Documentation: https://github.com/Illumina/ExpansionHunter/tree/master/docs
- RepeatCatalogs: https://github.com/Illumina/RepeatCatalogs

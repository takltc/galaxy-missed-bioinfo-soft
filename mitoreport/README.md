# MitoReport Galaxy Wrapper

[中文版](README_CN.md)

Galaxy integration for MitoReport - a comprehensive tool for mitochondrial DNA variant analysis and clinical interpretation.

## Software Information

| Property | Value |
|----------|-------|
| Version | 1.2.3 |
| Developer | Bioinformatics Methods Group, Murdoch Childrens Research Institute (MCRI) |
| License | Open Source |
| GitHub | https://github.com/bioinfomethods/mitoreport |
| Demo | https://bioinfomethods.github.io/mitoreport/examples/mitoreport-MITOREPORT-TEST-SAMPLE/index.html |

## Overview

MitoReport is an application for Mitochondrial DNA variants analysis that generates interactive HTML reports for clinical interpretation. It integrates:

- MitoMap variant annotations
- gnomAD population frequencies
- Heteroplasmy analysis
- Deletion detection
- Maternal heteroplasmy comparison

## Tool Components

### 1. MitoReport (mitoreport)

Main analysis tool that generates interactive reports from:

- VEP-annotated VCF files
- BAM files with mtDNA reads
- MitoMap annotations
- gnomAD population frequencies

### 2. MitoReport Download (mitoreport_download)

Utility tool to download the latest MitoMap annotations from https://mitomap.org

## Workflow

```
                    ┌──────────────────┐
                    │  MitoReport      │
                    │  Download        │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ MitoMap JSON     │
                    └────────┬─────────┘
                             │
┌──────────────────┐         │         ┌──────────────────┐
│ VEP-annotated    │         │         │ gnomAD mtDNA     │
│ VCF              ├─────────┼─────────┤ VCF              │
└──────────────────┘         │         └──────────────────┘
                             │
┌──────────────────┐         │         ┌──────────────────┐
│ Proband BAM      ├─────────┼─────────┤ Control BAMs     │
└──────────────────┘         │         │ (optional)       │
                             │         └──────────────────┘
┌──────────────────┐         │
│ Maternal VCF     ├─────────┘
│ (optional)       │
└──────────────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    MitoReport    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Interactive HTML │
                    │ Report           │
                    └──────────────────┘
```

## Input Requirements

| Input | Format | Required | Description |
|-------|--------|----------|-------------|
| VCF | VCF/VCF.GZ | Yes | VEP-annotated mitochondrial variants |
| Sample Name | Text | Yes | Sample identifier |
| BAM | BAM | Yes | Aligned reads with mtDNA |
| MitoMap JSON | JSON | Yes | Annotations from MitoReport Download |
| gnomAD VCF | VCF/VCF.GZ | Yes | Population frequency data |
| Control BAMs | BAM | No | Reference samples for deletion normalization |
| Maternal VCF | VCF/VCF.GZ | No | For heteroplasmy inheritance analysis |
| Maternal Sample | Text | No | Sample name in maternal VCF |

## Output Files

| File | Format | Description |
|------|--------|-------------|
| Interactive Report | HTML | Main output with searchable variant table |
| Full Report Archive | TAR.GZ | Complete output directory for offline use |

## Key Features

### Variant Annotation
- Integration with MitoMap disease associations
- gnomAD population frequencies
- VEP functional annotations
- Haplogroup marker information

### Heteroplasmy Analysis
- Quantification of variant allele frequencies
- Visual representation of heteroplasmy levels
- Comparison with maternal sample (if provided)

### Deletion Detection
- Large-scale mtDNA deletion analysis
- Normalization using control samples
- Visual deletion plots

## Best Practice Parameters

Based on UK Best Practice Guidelines (PMID: 36513735):

| Parameter | Recommendation | Description |
|-----------|----------------|-------------|
| Coverage | ≥500x | Minimum for reliable heteroplasmy detection |
| VAF Threshold | 1-5% | For clinical variant detection |
| Control Samples | ≥3 | For accurate deletion normalization |

### Recommended Workflow

1. Run **Haplocheck** first to check for contamination
2. Use **Mutserve** for variant calling (heteroplasmy threshold 1-5%)
3. Annotate variants with **VEP**
4. Download MitoMap annotations with **MitoReport Download**
5. Generate report with **MitoReport**

## Docker Container

Build using the Dockerfile in this directory:

```bash
cd docker
docker build -t omniverse/mitoreport:1.2.3 .
```

## Resource Files

MitoReport requires external resource files:

1. **gnomAD mtDNA VCF**: `gnomad.genomes.v3.1.sites.chrM.vcf.bgz`
   - Download from: https://gnomad.broadinstitute.org/downloads#v3-mitochondrial-dna
   
2. **MitoMap Annotations**: Generated by MitoReport Download tool

3. **Control BAMs** (optional): From 1000 Genomes or your own data

## File Structure

```
mitoreport/
├── docker/
│   └── Dockerfile
├── mitoreport.xml
├── mitoreport_download.xml
├── tool_conf.xml
├── README.md
└── README_CN.md
```

## Related Tools

- **Mutserve**: mtDNA variant calling (heteroplasmy detection)
- **Haplocheck**: Contamination detection (run before MitoReport)
- **Haplogrep3**: Haplogroup classification
- **VEP**: Variant effect annotation

## Clinical Applications

- Primary mitochondrial disease diagnosis
- Heteroplasmy monitoring
- Carrier testing
- Research studies on mtDNA variation

## Credits

MitoReport is developed by the Bioinformatics Methods group at the Murdoch Childrens Research Institute (MCRI), with contributions from:

- Victorian Clinical Genetics Services (VCGS)
- Australian Genomics Health Alliance
- Brain and Mitochondrial Research Group at MCRI

## Citations

If you use this tool in your research, please cite:

> Bioinformatics Methods Group. MitoReport: Interpretation software for mitochondrial variants. GitHub. https://github.com/bioinfomethods/mitoreport

For mtDNA analysis best practices:

> Mavraki E, et al. Genetic testing for mitochondrial disease: the United Kingdom best practice guidelines. Eur J Hum Genet. 2023;31:148-163. doi:10.1038/s41431-022-01249-w

## Links

- GitHub: https://github.com/bioinfomethods/mitoreport
- Demo: https://bioinfomethods.github.io/mitoreport/examples/
- MitoMap: https://mitomap.org/MITOMAP
- gnomAD mtDNA: https://gnomad.broadinstitute.org/downloads#v3-mitochondrial-dna

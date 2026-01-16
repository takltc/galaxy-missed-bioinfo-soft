# Mutserve Galaxy Wrapper

[中文版](README_CN.md)

Mutserve is a dedicated tool for mitochondrial DNA (mtDNA) variant detection, capable of detecting both homoplasmic and heteroplasmic sites.

## Software Information

| Property | Value |
|----------|-------|
| Version | 2.0.0-rc15 |
| Developer | Sebastian Schönherr, Hansi Weissensteiner, Lukas Forer (Genepi Innsbruck) |
| License | MIT License |
| GitHub | https://github.com/seppinho/mutserve |
| DOI | 10.1101/gr.256545.119 |
| PMID | 33452015 |

## Tool Components

### 1. Mutserve Call (mutserve_call)
Detects mtDNA variants from BAM/CRAM files:
- Homoplasmic variants: Present in all mtDNA copies
- Heteroplasmic variants: Present in only some mtDNA copies

### 2. Mutserve Annotate (mutserve_annotate)
Functional annotation of detected variants:
- Gene/region assignment
- Amino acid changes
- tRNA/rRNA annotations

## Workflow

```
BAM/CRAM (mtDNA aligned)
         │
         ▼
   Mutserve Call
         │
         ├──→ VCF (main output)
         │
         └──→ Raw Data (optional)
                  │
                  ▼
         Mutserve Annotate
                  │
                  ▼
         Annotated Variants
```

## Best Practice Parameters

Based on literature research (PMID: 35350246):

| Parameter | Recommended Value | Description |
|-----------|-------------------|-------------|
| heteroplasmy_level | 0.01-0.05 | Heteroplasmy detection threshold (1-5%) |
| mapQ | 20 | Minimum mapping quality |
| baseQ | 20 | Minimum base quality |
| alignQ | 30 | Minimum alignment quality |

### Heteroplasmy Threshold Selection

- **1% (0.01)**: High sensitivity, suitable for research purposes
- **5% (0.05)**: Balanced sensitivity and specificity, recommended for clinical applications
- **10% (0.10)**: High specificity, suitable for contamination-sensitive studies

## Benchmark Performance

According to systematic evaluation by Ip et al. (2022) Front Genet:
- Mutserve performs best on synthetic benchmark datasets (F1 score = 0.74)
- Homoplasmic variant detection is highly accurate and consistent
- Heteroplasmic variant detection is stable at 1-5% thresholds

## Docker Container

Build using the Dockerfile in this directory:
```bash
cd docker
docker build -t omniverse/mutserve:2.0.0-rc15 .
```

## Reference Sequence

Recommended to use rCRS (revised Cambridge Reference Sequence):
- Sequence: NC_012920.1
- Length: 16,569 bp
- Download: https://raw.githubusercontent.com/seppinho/mutserve/master/files/rCRS.fasta

## File Structure

```
mutserve/
├── docker/
│   └── Dockerfile
├── test-data/
├── mutserve_call.xml
├── mutserve_annotate.xml
├── tool_conf.xml
├── README.md
└── README_CN.md
```

## Citations

If you use this tool in your research, please cite:

> Weissensteiner H, Forer L, Fendt L, Kheirkhah A, Salas A, Kronenberg F, Schoenherr S. Contamination detection in sequencing studies using the mitochondrial phylogeny. Genome Res. 2021;31:309-316. doi:10.1101/gr.256545.119

> Weissensteiner H, Forer L, Fuchsberger C, Schöpf B, Kloss-Brandstätter A, Specht G, Kronenberg F, Schönherr S. mtDNA-Server: next-generation sequencing data analysis of human mitochondrial DNA in the cloud. Nucleic Acids Res. 2016;44:W64-9. doi:10.1093/nar/gkw247

## Related Tools

- **Haplocheck**: Contamination detection using Mutserve
- **Haplogrep**: mtDNA haplogroup classification
- **mtDNA-Server 2**: Complete mtDNA analysis pipeline

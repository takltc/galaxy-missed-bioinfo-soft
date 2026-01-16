# ExpansionHunter Denovo Galaxy Wrapper

[中文版](README_CN.md)

ExpansionHunter Denovo (EHdn) is a suite of tools for detecting novel short tandem repeat (STR) expansions.

## Software Information

| Property | Value |
|----------|-------|
| Version | 0.9.0 |
| Developer | Illumina |
| License | Apache License 2.0 |
| DOI | 10.1186/s13059-020-02017-z |
| PMID | 32345345 |

## Tool Components

### 1. Profile (expansionhunter_denovo_profile)
Generates STR profiles from BAM/CRAM files, including:
- Anchored in-repeat reads (Anchored IRRs)
- Paired in-repeat reads (Paired IRRs)

### 2. Merge (expansionhunter_denovo_merge)
Combines STR profiles from multiple samples for cohort analysis.

### 3. Locus Analysis (expansionhunter_denovo_locus)
Statistical analysis based on genomic loci:
- Case-Control analysis
- Outlier analysis

### 4. Motif Analysis (expansionhunter_denovo_motif)
Statistical analysis based on repeat motifs:
- Identifies overall enrichment of specific motifs
- Suitable when specific locations are unknown

## Workflow

```
BAM/CRAM files
      │
      ▼
   Profile (per sample)
      │
      ▼
   Merge (combine all)
      │
      ▼
  Locus/Motif Analysis
      │
      ▼
  Ranked candidate expansions
```

## Best Practice Parameters

Based on recommendations from Dolzhenko et al. (2020):

| Parameter | Recommended Value | Description |
|-----------|-------------------|-------------|
| min-anchor-mapq | 50 | Minimum MAPQ for anchor reads |
| max-irr-mapq | 40 | Maximum MAPQ for in-repeat reads |
| Sequencing depth | 30-40x | Whole genome sequencing |
| Read length | 100-200bp | Short-read sequencing |

## Docker Container

Using Bioconda pre-built image:
```bash
docker pull quay.io/biocontainers/expansionhunterdenovo:0.9.0--h6ac36c1_11
```

Or build using the Dockerfile in this directory:
```bash
cd docker
docker build -t expansionhunterdenovo:0.9.0 .
```

> **Note**: The custom Dockerfile uses an independent conda environment with Python 3.9 to resolve `backports.lzma` dependency issues.

## File Structure

```
expansionhunter_denovo/
├── docker/
│   └── Dockerfile
├── expansionhunter_denovo_profile.xml
├── expansionhunter_denovo_merge.xml
├── expansionhunter_denovo_locus.xml
├── expansionhunter_denovo_motif.xml
├── tool_conf.xml
├── README.md
└── README_CN.md
```

## Citations

If you use this tool in your research, please cite:

> Dolzhenko E, Bennett MF, Richmond PA, et al. ExpansionHunter Denovo: a computational method for locating known and novel repeat expansions in short-read sequencing data. Genome Biol. 2020;21(1):102. doi:10.1186/s13059-020-02017-z

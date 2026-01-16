# MitoZ Galaxy Wrapper

[中文版](README_CN.md)

MitoZ is a comprehensive toolkit for animal mitochondrial genome assembly, annotation, and visualization.

## Software Information

| Property | Value |
|----------|-------|
| Version | 3.6 |
| Developer | Guanliang Meng (BGI-Shenzhen) |
| License | GPL-3.0 |
| DOI | 10.1093/nar/gkz173 |
| PMID | 30864657 |
| GitHub | https://github.com/linzhi2013/MitoZ |

## Tool Components

### MitoZ All-in-One (mitoz_all)

One-stop solution from raw FASTQ data to complete mitochondrial genome annotation:

1. **Data Filtering**: Clean raw data using fastp
2. **De novo Assembly**: Assembly using MEGAHIT or SPAdes
3. **Sequence Identification**: Identify mitochondrial sequences using HMM profiles
4. **Gene Annotation**: Annotate PCGs, tRNAs, and rRNAs
5. **Visualization**: Generate Circos plots

## Workflow

```
Raw FASTQ files (PE or SE)
         │
         ▼
    Data Filtering (fastp)
         │
         ▼
    De novo Assembly (MEGAHIT/SPAdes)
         │
         ▼
    Mitogenome Identification (HMMER)
         │
         ▼
    Gene Annotation (PCGs + tRNAs + rRNAs)
         │
         ▼
    Visualization (Circos)
         │
         ▼
    Annotated Mitogenome + GenBank + Circos Plot
```

## Supported Taxonomic Groups

| Clade | Genetic Code | Description |
|-------|--------------|-------------|
| Chordata | 2 | Vertebrates (mammals, birds, reptiles, amphibians, fish) |
| Arthropoda | 5 | Arthropods (insects, crustaceans, arachnids) |

## Best Practice Parameters

Based on Meng et al. (2019) paper and author recommendations:

| Parameter | Recommended Value | Description |
|-----------|-------------------|-------------|
| data_size | 0.3-3 Gbp | Try small data first, increase if failed |
| kmers_megahit | 59 79 99 119 141 | Prefer larger k-mers |
| fastq_read_length | 100-200bp | Short-read sequencing |
| memory | 50 GB | MEGAHIT maximum memory |

## Input Formats

- **FASTQ**: Paired-end or Single-end data
- **Compression**: Supports gzip format (.gz)
- **Platform**: Illumina, BGI-SEQ and other short-read platforms

## Output Files

| File | Format | Description |
|------|--------|-------------|
| mitogenome.fasta | FASTA | Assembled mitochondrial genome sequence |
| annotation.gbf | GenBank | Complete gene annotation file |
| visualization.svg | SVG | Circos visualization (vector) |
| visualization.png | PNG | Circos visualization (raster) |
| cds.fasta | FASTA | Protein-coding gene sequences |
| trna.fasta | FASTA | tRNA gene sequences |
| rrna.fasta | FASTA | rRNA gene sequences |
| summary.txt | TXT | Assembly and annotation statistics |
| overlap_info.txt | TXT | Circular verification information |

## Docker Container

Using official pre-built image:
```bash
docker pull guanliangmeng/mitoz:3.6
```

Or build using the Dockerfile in this directory:
```bash
cd docker
docker build -t mitoz:3.6 .
```

## Usage Examples

### Basic Usage (Paired-end data)
```bash
mitoz all \
    --outprefix sample1 \
    --thread_number 16 \
    --clade Chordata \
    --genetic_code 2 \
    --fq1 sample1_R1.fq.gz \
    --fq2 sample1_R2.fq.gz \
    --fastq_read_length 150 \
    --data_size_for_mt_assembly 3,0 \
    --assembler megahit \
    --kmers_megahit 59 79 99 119 141 \
    --memory 50 \
    --requiring_taxa Chordata
```

### Quick Test with Small Data
```bash
mitoz all \
    --outprefix sample1 \
    --thread_number 8 \
    --clade Chordata \
    --genetic_code 2 \
    --fq1 sample1_R1.fq.gz \
    --fq2 sample1_R2.fq.gz \
    --fastq_read_length 150 \
    --data_size_for_mt_assembly 0.3,0 \
    --assembler megahit \
    --kmers_megahit 43 71 99 \
    --memory 8
```

## Troubleshooting

### 1. Incomplete Mitochondrial Genome
- Try using less data (0.3 Gbp)
- Try different k-mer sizes

### 2. Missing tRNA Annotations
- Ensure shell is bash
- Check MitoZ version (recommend 3.6)

### 3. Out of Memory
- Reduce `--memory` parameter
- Reduce `--data_size_for_mt_assembly`

## File Structure

```
mitoz/
├── docker/
│   └── Dockerfile
├── mitoz_all.xml
├── tool_conf.xml
├── README.md
└── README_CN.md
```

## Citations

If you use this tool in your research, please cite:

> Meng G, Li Y, Yang C, Liu S. MitoZ: a toolkit for animal mitochondrial genome 
> assembly, annotation and visualization. Nucleic Acids Research. 2019;47(11):e63.
> https://doi.org/10.1093/nar/gkz173

## Related Software Citations

MitoZ internally calls multiple software packages, please also cite:
- fastp (data filtering)
- MEGAHIT/SPAdes (assembly)
- HMMER (sequence identification)
- Circos (visualization)
- See: https://github.com/linzhi2013/MitoZ/wiki/Citations

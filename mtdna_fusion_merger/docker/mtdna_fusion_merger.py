#!/usr/bin/env python3
"""
mtDNA Fusion Merger - 基于 mtDNA-Server 2 融合模式的变异合并工具

实现 PMID:38709886 (Weissensteiner et al., NAR 2024) 中描述的融合策略:
- SNVs: 优先使用 Mutserve (更高准确性)
- INDELs: 优先使用 Mutect2 (Mutserve INDEL 支持有限)
- 位置冲突时: INDEL 调用优先于 SNV

输入: Mutserve VCF + Mutect2 VCF
输出: 融合后的 VCF + JSON 报告
"""

import argparse
import gzip
import json
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class Variant:
    chrom: str
    pos: int
    ref: str
    alt: str
    qual: float
    filter_status: str
    info: dict
    format_fields: list
    sample_data: list
    source: str
    is_indel: bool = field(init=False)
    
    def __post_init__(self):
        self.is_indel = len(self.ref) != len(self.alt) or len(self.ref) > 1

    @property
    def key(self) -> tuple:
        return (self.chrom, self.pos, self.ref, self.alt)
    
    @property
    def position_key(self) -> tuple:
        return (self.chrom, self.pos)


@dataclass
class FusionStats:
    mutserve_total: int = 0
    mutect2_total: int = 0
    mutserve_snvs: int = 0
    mutserve_indels: int = 0
    mutect2_snvs: int = 0
    mutect2_indels: int = 0
    fusion_snvs_from_mutserve: int = 0
    fusion_indels_from_mutect2: int = 0
    both_callers: int = 0
    mutserve_only: int = 0
    mutect2_only: int = 0
    conflicts_resolved: int = 0
    final_variants: int = 0


def parse_vcf(vcf_path: Path, source: str) -> tuple[list[str], list[Variant]]:
    header_lines: list[str] = []
    variants: list[Variant] = []
    
    with open(vcf_path, 'rt') as f:
        content = f.read()
    
    if str(vcf_path).endswith('.gz'):
        with gzip.open(vcf_path, 'rt') as f:
            content = f.read()
    
    for raw_line in content.split('\n'):
        line = raw_line.strip()
        if line.startswith('#'):
            header_lines.append(line)
            continue
        
        if not line:
            continue
            
        fields = line.split('\t')
        if len(fields) < 8:
            continue
        
        chrom, pos, vid, ref, alt, qual, filt, info = fields[:8]
        format_fields = fields[8].split(':') if len(fields) > 8 else []
        sample_data = [s.split(':') for s in fields[9:]] if len(fields) > 9 else []
        
        info_dict: dict = {}
        for item in info.split(';'):
            if '=' in item:
                k, v = item.split('=', 1)
                info_dict[k] = v
            else:
                info_dict[item] = True
        
        for alt_allele in alt.split(','):
            variants.append(Variant(
                chrom=chrom,
                pos=int(pos),
                ref=ref,
                alt=alt_allele,
                qual=float(qual) if qual != '.' else 0.0,
                filter_status=filt,
                info=info_dict.copy(),
                format_fields=format_fields.copy(),
                sample_data=[s.copy() for s in sample_data],
                source=source
            ))
    
    return header_lines, variants


def calculate_confidence(variant: Variant, in_both: bool) -> float:
    if in_both:
        return 1.0
    if variant.source == 'mutserve':
        return 0.85 if not variant.is_indel else 0.70
    return 0.80 if variant.is_indel else 0.60


def fusion_merge(
    mutserve_variants: list[Variant],
    mutect2_variants: list[Variant],
    stats: FusionStats
) -> list[Variant]:
    mutserve_by_key = {v.key: v for v in mutserve_variants}
    mutect2_by_key = {v.key: v for v in mutect2_variants}
    
    mutserve_by_pos = defaultdict(list)
    mutect2_by_pos = defaultdict(list)
    
    for v in mutserve_variants:
        mutserve_by_pos[v.position_key].append(v)
    for v in mutect2_variants:
        mutect2_by_pos[v.position_key].append(v)
    
    stats.mutserve_total = len(mutserve_variants)
    stats.mutect2_total = len(mutect2_variants)
    stats.mutserve_snvs = sum(1 for v in mutserve_variants if not v.is_indel)
    stats.mutserve_indels = sum(1 for v in mutserve_variants if v.is_indel)
    stats.mutect2_snvs = sum(1 for v in mutect2_variants if not v.is_indel)
    stats.mutect2_indels = sum(1 for v in mutect2_variants if v.is_indel)
    
    final_variants = []
    processed_keys = set()
    
    for v in mutect2_variants:
        if v.is_indel:
            v.info['FUSION_SOURCE'] = 'mutect2'
            v.info['FUSION_CONFIDENCE'] = str(calculate_confidence(v, v.key in mutserve_by_key))
            if v.key in mutserve_by_key:
                v.info['BOTH_CALLERS'] = 'true'
                stats.both_callers += 1
            else:
                stats.mutect2_only += 1
            final_variants.append(v)
            processed_keys.add(v.key)
            stats.fusion_indels_from_mutect2 += 1
            
            mutserve_at_pos = mutserve_by_pos.get(v.position_key, [])
            for mv in mutserve_at_pos:
                if not mv.is_indel and mv.key not in processed_keys:
                    stats.conflicts_resolved += 1
                    processed_keys.add(mv.key)
    
    for v in mutserve_variants:
        if v.key in processed_keys:
            continue
        
        if not v.is_indel:
            v.info['FUSION_SOURCE'] = 'mutserve'
            v.info['FUSION_CONFIDENCE'] = str(calculate_confidence(v, v.key in mutect2_by_key))
            if v.key in mutect2_by_key:
                v.info['BOTH_CALLERS'] = 'true'
                stats.both_callers += 1
            else:
                stats.mutserve_only += 1
            final_variants.append(v)
            processed_keys.add(v.key)
            stats.fusion_snvs_from_mutserve += 1
        else:
            if v.key not in mutect2_by_key:
                v.info['FUSION_SOURCE'] = 'mutserve'
                v.info['FUSION_CONFIDENCE'] = str(calculate_confidence(v, False))
                final_variants.append(v)
                processed_keys.add(v.key)
                stats.mutserve_only += 1
    
    final_variants.sort(key=lambda x: (x.chrom, x.pos))
    stats.final_variants = len(final_variants)
    
    return final_variants


def write_vcf(
    output_path: Path,
    header_lines: list[str],
    variants: list[Variant],
    mode: str
) -> None:
    fusion_header_lines = [
        '##INFO=<ID=FUSION_SOURCE,Number=1,Type=String,Description="Source caller in fusion mode (mutserve/mutect2)">',
        '##INFO=<ID=FUSION_CONFIDENCE,Number=1,Type=Float,Description="Fusion confidence score (0-1)">',
        '##INFO=<ID=BOTH_CALLERS,Number=0,Type=Flag,Description="Variant called by both callers">',
        f'##mtdna_fusion_merger_mode={mode}',
        '##mtdna_fusion_merger_version=1.0.0',
        '##mtdna_fusion_merger_reference=PMID:38709886'
    ]
    
    output_lines: list[str] = []
    
    for line in header_lines:
        if line.startswith('#CHROM'):
            for fh in fusion_header_lines:
                output_lines.append(fh)
        output_lines.append(line)
    
    for v in variants:
        info_str = ';'.join(
            f'{k}={v_val}' if v_val is not True else k 
            for k, v_val in v.info.items()
        )
        format_str = ':'.join(v.format_fields) if v.format_fields else 'GT'
        samples_str = '\t'.join(':'.join(s) for s in v.sample_data) if v.sample_data else '0/1'
        
        line = f'{v.chrom}\t{v.pos}\t.\t{v.ref}\t{v.alt}\t{v.qual}\t{v.filter_status}\t{info_str}\t{format_str}\t{samples_str}'
        output_lines.append(line)
    
    with open(output_path, 'w') as f:
        f.write('\n'.join(output_lines) + '\n')


def main():
    parser = argparse.ArgumentParser(
        description='mtDNA Fusion Merger - Merge Mutserve and Mutect2 variant calls using fusion mode',
        epilog='Reference: Weissensteiner et al. NAR 2024 (PMID:38709886)'
    )
    parser.add_argument('--mutserve-vcf', required=True, type=Path, help='Mutserve VCF file')
    parser.add_argument('--mutect2-vcf', required=True, type=Path, help='Mutect2 VCF file')
    parser.add_argument('--output', required=True, type=Path, help='Output VCF file')
    parser.add_argument('--report', type=Path, help='Output JSON report file')
    parser.add_argument('--mode', choices=['fusion', 'intersection', 'union'], default='fusion',
                        help='Merge mode: fusion (default), intersection, or union')
    
    args = parser.parse_args()
    
    if not args.mutserve_vcf.exists():
        sys.exit(f'Error: Mutserve VCF not found: {args.mutserve_vcf}')
    if not args.mutect2_vcf.exists():
        sys.exit(f'Error: Mutect2 VCF not found: {args.mutect2_vcf}')
    
    mutserve_header, mutserve_variants = parse_vcf(args.mutserve_vcf, 'mutserve')
    mutect2_header, mutect2_variants = parse_vcf(args.mutect2_vcf, 'mutect2')
    
    stats = FusionStats()
    stats.mutserve_total = len(mutserve_variants)
    stats.mutect2_total = len(mutect2_variants)
    stats.mutserve_snvs = sum(1 for v in mutserve_variants if not v.is_indel)
    stats.mutserve_indels = sum(1 for v in mutserve_variants if v.is_indel)
    stats.mutect2_snvs = sum(1 for v in mutect2_variants if not v.is_indel)
    stats.mutect2_indels = sum(1 for v in mutect2_variants if v.is_indel)
    
    if args.mode == 'fusion':
        final_variants = fusion_merge(mutserve_variants, mutect2_variants, stats)
    elif args.mode == 'intersection':
        mutserve_keys = {v.key for v in mutserve_variants}
        mutect2_keys = {v.key for v in mutect2_variants}
        common_keys = mutserve_keys & mutect2_keys
        final_variants = [v for v in mutserve_variants if v.key in common_keys]
        stats.both_callers = len(final_variants)
        stats.final_variants = len(final_variants)
    else:
        all_variants = {v.key: v for v in mutect2_variants}
        all_variants.update({v.key: v for v in mutserve_variants})
        final_variants = sorted(all_variants.values(), key=lambda x: (x.chrom, x.pos))
        stats.final_variants = len(final_variants)
    
    write_vcf(args.output, mutserve_header, final_variants, args.mode)
    
    if args.report:
        report = {
            'mode': args.mode,
            'version': '1.0.0',
            'reference': 'PMID:38709886',
            'statistics': {
                'mutserve': {
                    'total': stats.mutserve_total,
                    'snvs': stats.mutserve_snvs,
                    'indels': stats.mutserve_indels
                },
                'mutect2': {
                    'total': stats.mutect2_total,
                    'snvs': stats.mutect2_snvs,
                    'indels': stats.mutect2_indels
                },
                'fusion_result': {
                    'snvs_from_mutserve': stats.fusion_snvs_from_mutserve,
                    'indels_from_mutect2': stats.fusion_indels_from_mutect2,
                    'both_callers': stats.both_callers,
                    'mutserve_only': stats.mutserve_only,
                    'mutect2_only': stats.mutect2_only,
                    'conflicts_resolved': stats.conflicts_resolved,
                    'final_total': stats.final_variants
                }
            }
        }
        with open(args.report, 'w') as f:
            json.dump(report, f, indent=2)
    
    print(f'Fusion merge complete: {stats.final_variants} variants')
    print(f'  SNVs from Mutserve: {stats.fusion_snvs_from_mutserve}')
    print(f'  INDELs from Mutect2: {stats.fusion_indels_from_mutect2}')
    print(f'  Both callers: {stats.both_callers}')
    print(f'  Conflicts resolved: {stats.conflicts_resolved}')


if __name__ == '__main__':
    main()

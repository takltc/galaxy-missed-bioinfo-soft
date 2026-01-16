#!/usr/bin/env python3
"""
mtDNA Fusion Merger 测试脚本

测试 fusion mode 变异合并逻辑：
1. SNVs 优先使用 Mutserve
2. INDELs 优先使用 Mutect2
3. 位置冲突时 INDEL 优先于 SNV
4. 置信度评分计算

基于 PMID:38709886 (mtDNA-Server 2) 的融合策略
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def run_fusion_merger(mutserve_vcf: Path, mutect2_vcf: Path, output_vcf: Path, report_json: Path, mode: str = 'fusion') -> int:
    """运行 mtdna_fusion_merger.py"""
    script_path = Path(__file__).parent.parent / 'mtdna_fusion_merger.py'
    
    cmd = [
        sys.executable, str(script_path),
        '--mutserve-vcf', str(mutserve_vcf),
        '--mutect2-vcf', str(mutect2_vcf),
        '--output', str(output_vcf),
        '--report', str(report_json),
        '--mode', mode
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"STDERR: {result.stderr}")
        print(f"STDOUT: {result.stdout}")
    return result.returncode


def parse_vcf_variants(vcf_path: Path) -> list[dict]:
    """解析 VCF 文件中的变异"""
    variants = []
    with open(vcf_path) as f:
        for line in f:
            if line.startswith('#'):
                continue
            fields = line.strip().split('\t')
            if len(fields) < 8:
                continue
            
            info_dict = {}
            for item in fields[7].split(';'):
                if '=' in item:
                    k, v = item.split('=', 1)
                    info_dict[k] = v
                else:
                    info_dict[item] = True
            
            variants.append({
                'chrom': fields[0],
                'pos': int(fields[1]),
                'ref': fields[3],
                'alt': fields[4],
                'filter': fields[6],
                'info': info_dict
            })
    return variants


def test_fusion_mode_basic():
    """测试基本的 fusion mode 功能"""
    print("=" * 60)
    print("Test 1: Basic Fusion Mode")
    print("=" * 60)
    
    test_data_dir = Path(__file__).parent / 'data'
    mutserve_vcf = test_data_dir / 'mutserve_test.vcf'
    mutect2_vcf = test_data_dir / 'mutect2_test.vcf'
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_vcf = Path(tmpdir) / 'output.vcf'
        report_json = Path(tmpdir) / 'report.json'
        
        # 运行融合
        ret = run_fusion_merger(mutserve_vcf, mutect2_vcf, output_vcf, report_json)
        assert ret == 0, f"Fusion merger failed with code {ret}"
        
        # 验证输出文件存在
        assert output_vcf.exists(), "Output VCF not created"
        assert report_json.exists(), "Report JSON not created"
        
        # 解析报告
        with open(report_json) as f:
            report = json.load(f)
        
        print(f"\nStatistics:")
        print(f"  Mutserve total: {report['statistics']['mutserve']['total']}")
        print(f"  Mutect2 total: {report['statistics']['mutect2']['total']}")
        print(f"  Mutect2 INDELs: {report['statistics']['mutect2']['indels']}")
        print(f"  Final variants: {report['statistics']['fusion_result']['final_total']}")
        print(f"  SNVs from Mutserve: {report['statistics']['fusion_result']['snvs_from_mutserve']}")
        print(f"  INDELs from Mutect2: {report['statistics']['fusion_result']['indels_from_mutect2']}")
        print(f"  Both callers: {report['statistics']['fusion_result']['both_callers']}")
        
        # 验证统计数据合理性
        assert report['statistics']['mutserve']['total'] > 0, "No Mutserve variants parsed"
        assert report['statistics']['mutect2']['total'] > 0, "No Mutect2 variants parsed"
        assert report['statistics']['mutect2']['indels'] > 0, "No Mutect2 INDELs found"
        assert report['statistics']['fusion_result']['final_total'] > 0, "No final variants"
        
        # 解析输出 VCF
        variants = parse_vcf_variants(output_vcf)
        
        # 验证所有变异都有 FUSION_SOURCE
        for v in variants:
            assert 'FUSION_SOURCE' in v['info'], f"Missing FUSION_SOURCE at pos {v['pos']}"
            assert 'FUSION_CONFIDENCE' in v['info'], f"Missing FUSION_CONFIDENCE at pos {v['pos']}"
        
        # 统计来源
        mutserve_count = sum(1 for v in variants if v['info'].get('FUSION_SOURCE') == 'mutserve')
        mutect2_count = sum(1 for v in variants if v['info'].get('FUSION_SOURCE') == 'mutect2')
        
        print(f"\nOutput VCF analysis:")
        print(f"  Total variants: {len(variants)}")
        print(f"  From Mutserve: {mutserve_count}")
        print(f"  From Mutect2: {mutect2_count}")
        
        print("\n[PASS] Basic fusion mode test passed")
        return True


def test_indel_priority():
    """测试 INDEL 优先规则"""
    print("\n" + "=" * 60)
    print("Test 2: INDEL Priority Rule")
    print("=" * 60)
    
    test_data_dir = Path(__file__).parent / 'data'
    mutserve_vcf = test_data_dir / 'mutserve_test.vcf'
    mutect2_vcf = test_data_dir / 'mutect2_test.vcf'
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_vcf = Path(tmpdir) / 'output.vcf'
        report_json = Path(tmpdir) / 'report.json'
        
        ret = run_fusion_merger(mutserve_vcf, mutect2_vcf, output_vcf, report_json)
        assert ret == 0
        
        variants = parse_vcf_variants(output_vcf)
        
        # 检查所有 INDEL 都来自 Mutect2
        indel_sources = []
        for v in variants:
            is_indel = len(v['ref']) != len(v['alt']) or len(v['ref']) > 1
            if is_indel:
                source = v['info'].get('FUSION_SOURCE', 'unknown')
                indel_sources.append((v['pos'], source))
                print(f"  INDEL at {v['pos']}: {v['ref']}->{v['alt']} from {source}")
        
        # Mutect2 中的 INDEL 位置
        mutect2_indel_positions = {302, 310, 955, 960, 5132, 12308, 16183}
        
        for pos, source in indel_sources:
            if pos in mutect2_indel_positions:
                assert source == 'mutect2', f"INDEL at {pos} should be from mutect2, got {source}"
        
        print(f"\n  Total INDELs in output: {len(indel_sources)}")
        print("\n[PASS] INDEL priority test passed")
        return True


def test_snv_priority():
    """测试 SNV 优先使用 Mutserve 规则"""
    print("\n" + "=" * 60)
    print("Test 3: SNV Priority Rule")
    print("=" * 60)
    
    test_data_dir = Path(__file__).parent / 'data'
    mutserve_vcf = test_data_dir / 'mutserve_test.vcf'
    mutect2_vcf = test_data_dir / 'mutect2_test.vcf'
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_vcf = Path(tmpdir) / 'output.vcf'
        report_json = Path(tmpdir) / 'report.json'
        
        ret = run_fusion_merger(mutserve_vcf, mutect2_vcf, output_vcf, report_json)
        assert ret == 0
        
        variants = parse_vcf_variants(output_vcf)
        
        # 两个工具都调用的 SNV 位置
        common_snv_positions = {73, 152, 263, 489, 750, 1438, 4769, 7028, 8860, 9540, 11719, 14766, 15326, 16189, 16519}
        
        snv_sources = {}
        for v in variants:
            is_snv = len(v['ref']) == len(v['alt']) == 1
            if is_snv and v['pos'] in common_snv_positions:
                snv_sources[v['pos']] = v['info'].get('FUSION_SOURCE', 'unknown')
        
        print("\n  Common SNVs source check:")
        for pos, source in sorted(snv_sources.items()):
            status = "OK" if source == 'mutserve' else "WARN"
            print(f"    Position {pos}: {source} [{status}]")
        
        # SNVs 应该优先来自 Mutserve
        mutserve_snvs = sum(1 for s in snv_sources.values() if s == 'mutserve')
        print(f"\n  SNVs from Mutserve: {mutserve_snvs}/{len(snv_sources)}")
        
        assert mutserve_snvs == len(snv_sources), "Some common SNVs not from Mutserve"
        
        print("\n[PASS] SNV priority test passed")
        return True


def test_confidence_scores():
    """测试置信度评分"""
    print("\n" + "=" * 60)
    print("Test 4: Confidence Scores")
    print("=" * 60)
    
    test_data_dir = Path(__file__).parent / 'data'
    mutserve_vcf = test_data_dir / 'mutserve_test.vcf'
    mutect2_vcf = test_data_dir / 'mutect2_test.vcf'
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_vcf = Path(tmpdir) / 'output.vcf'
        report_json = Path(tmpdir) / 'report.json'
        
        ret = run_fusion_merger(mutserve_vcf, mutect2_vcf, output_vcf, report_json)
        assert ret == 0
        
        variants = parse_vcf_variants(output_vcf)
        
        confidence_distribution = {'1.0': 0, '0.85': 0, '0.80': 0, '0.70': 0, '0.60': 0, 'other': 0}
        
        for v in variants:
            conf = v['info'].get('FUSION_CONFIDENCE', '0')
            if conf in confidence_distribution:
                confidence_distribution[conf] += 1
            else:
                confidence_distribution['other'] += 1
                
            both = 'BOTH_CALLERS' in v['info']
            source = v['info'].get('FUSION_SOURCE', '')
            is_indel = len(v['ref']) != len(v['alt']) or len(v['ref']) > 1
            
            # 验证置信度规则
            if both:
                assert conf == '1.0', f"Both callers should have conf=1.0, got {conf}"
            elif source == 'mutserve' and not is_indel:
                assert conf == '0.85', f"Mutserve SNV should have conf=0.85, got {conf}"
            elif source == 'mutect2' and is_indel:
                assert conf == '0.8' or conf == '0.80', f"Mutect2 INDEL should have conf=0.80, got {conf}"
        
        print("\n  Confidence distribution:")
        for conf, count in confidence_distribution.items():
            if count > 0:
                print(f"    {conf}: {count}")
        
        print("\n[PASS] Confidence scores test passed")
        return True


def test_intersection_mode():
    """测试 intersection 模式"""
    print("\n" + "=" * 60)
    print("Test 5: Intersection Mode")
    print("=" * 60)
    
    test_data_dir = Path(__file__).parent / 'data'
    mutserve_vcf = test_data_dir / 'mutserve_test.vcf'
    mutect2_vcf = test_data_dir / 'mutect2_test.vcf'
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_vcf = Path(tmpdir) / 'output.vcf'
        report_json = Path(tmpdir) / 'report.json'
        
        ret = run_fusion_merger(mutserve_vcf, mutect2_vcf, output_vcf, report_json, mode='intersection')
        assert ret == 0
        
        with open(report_json) as f:
            report = json.load(f)
        
        variants = parse_vcf_variants(output_vcf)
        
        print(f"\n  Intersection result: {len(variants)} variants")
        print(f"  Both callers count: {report['statistics']['fusion_result']['both_callers']}")
        
        # Intersection 应该只包含两个工具都调用的变异
        assert len(variants) == report['statistics']['fusion_result']['both_callers']
        
        print("\n[PASS] Intersection mode test passed")
        return True


def test_union_mode():
    """测试 union 模式"""
    print("\n" + "=" * 60)
    print("Test 6: Union Mode")
    print("=" * 60)
    
    test_data_dir = Path(__file__).parent / 'data'
    mutserve_vcf = test_data_dir / 'mutserve_test.vcf'
    mutect2_vcf = test_data_dir / 'mutect2_test.vcf'
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_vcf = Path(tmpdir) / 'output.vcf'
        report_json = Path(tmpdir) / 'report.json'
        
        ret = run_fusion_merger(mutserve_vcf, mutect2_vcf, output_vcf, report_json, mode='union')
        assert ret == 0
        
        with open(report_json) as f:
            report = json.load(f)
        
        variants = parse_vcf_variants(output_vcf)
        
        print(f"\n  Union result: {len(variants)} variants")
        print(f"  Mutserve total: {report['statistics']['mutserve']['total']}")
        print(f"  Mutect2 total: {report['statistics']['mutect2']['total']}")
        
        # Union 应该包含所有唯一变异
        # 由于可能有重复，数量应该 <= mutserve + mutect2
        max_possible = report['statistics']['mutserve']['total'] + report['statistics']['mutect2']['total']
        assert len(variants) <= max_possible
        assert len(variants) >= max(report['statistics']['mutserve']['total'], report['statistics']['mutect2']['total'])
        
        print("\n[PASS] Union mode test passed")
        return True


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("mtDNA Fusion Merger Test Suite")
    print("Based on PMID:38709886 (mtDNA-Server 2)")
    print("=" * 60)
    
    tests = [
        test_fusion_mode_basic,
        test_indel_priority,
        test_snv_priority,
        test_confidence_scores,
        test_intersection_mode,
        test_union_mode,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except AssertionError as e:
            print(f"\n[FAIL] {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"\n[ERROR] {test.__name__}: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Test Summary: {passed}/{len(tests)} passed")
    print("=" * 60)
    
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())

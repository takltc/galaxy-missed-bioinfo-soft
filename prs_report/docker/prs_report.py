#!/usr/bin/env python3
"""
PRS Report Generator
Generate HTML reports and radar charts for PRS results.
"""
import argparse
import json
import math
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def generate_radar_chart(risk_data: List[Dict], output_path: str) -> None:
    if not risk_data:
        return
    
    sample = risk_data[0]
    categories = ['Cardiovascular', 'Type 2 Diabetes', 'Breast Cancer', 
                  'Prostate Cancer', 'Alzheimer', 'Coronary Artery']
    
    percentile = sample.get('percentile', 50)
    values = [percentile] * len(categories)
    
    N = len(categories)
    angles = [n / float(N) * 2 * math.pi for n in range(N)]
    angles += angles[:1]
    values += values[:1]
    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    
    ax.plot(angles, values, 'o-', linewidth=2, color='#3b82f6')
    ax.fill(angles, values, alpha=0.25, color='#3b82f6')
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, size=10)
    ax.set_ylim(0, 100)
    
    risk_zones = [
        (0, 25, '#22c55e', 0.1),
        (25, 75, '#f59e0b', 0.1),
        (75, 90, '#ea580c', 0.1),
        (90, 100, '#dc2626', 0.1)
    ]
    
    for r_min, r_max, color, alpha in risk_zones:
        theta = np.linspace(0, 2*np.pi, 100)
        r_inner = np.ones(100) * r_min
        r_outer = np.ones(100) * r_max
        ax.fill_between(theta, r_inner, r_outer, alpha=alpha, color=color)
    
    ax.set_title('Polygenic Risk Score Profile', size=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(output_path, format='svg', bbox_inches='tight')
    plt.close()


from jinja2 import Environment, FileSystemLoader

def generate_html_report(prs_summary: List[Dict], percentiles: Dict, risk_categories: Dict, 
                         recommendations: Dict, include_radar: bool, 
                         include_lifestyle: bool, output_path: str, radar_path: str = "") -> None:
    # Setup Jinja2 environment
    template_dir = os.environ.get('PRS_TEMPLATE_DIR', '/usr/local/share/prs_report')
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('report_template.html')
    
    results = risk_categories.get('results', [])
    rec_results = recommendations.get('recommendations', [])
    rec_map = {r['sample_id']: r['recommendations'] for r in rec_results}
    
    # Enrich results with recommendations
    for sample in results:
        sample['recommendations'] = rec_map.get(sample['sample_id'], [])
    
    radar_img = os.path.basename(radar_path) if radar_path else None
    
    render_vars = {
        "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M'),
        "results": results,
        "prs_summary": prs_summary[:10], # Top 10 thresholds
        "metadata": percentiles.get('metadata', {}),
        "include_radar": include_radar,
        "include_lifestyle": include_lifestyle,
        "radar_img": radar_img
    }
    
    html_out = template.render(**render_vars)
    
    with open(output_path, 'w') as f:
        f.write(html_out)


def generate_summary_json(prs_summary: List[Dict], percentiles: Dict, risk_categories: Dict,
                          recommendations: Dict, output_path: str) -> None:
    summary = {
        "generated_at": datetime.now().isoformat(),
        "version": "1.0.0",
        "metadata": percentiles.get('metadata', {}),
        "risk_thresholds": risk_categories.get('risk_thresholds', {}),
        "results": []
    }
    
    risk_results = risk_categories.get('results', [])
    rec_results = recommendations.get('recommendations', [])
    
    rec_map = {r['sample_id']: r['recommendations'] for r in rec_results}
    
    for sample in risk_results:
        sample_summary = {
            **sample,
            "recommendations": rec_map.get(sample['sample_id'], [])
        }
        summary['results'].append(sample_summary)
    
    with open(output_path, 'w') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)


import pandas as pd

def parse_prsice_summary(file_path: str) -> List[Dict]:
    """Parse PRSice-2 summary TSV file."""
    try:
        df = pd.read_csv(file_path, sep='\t')
        return df.to_dict(orient='records')
    except Exception as e:
        print(f"Warning: Could not parse PRSice summary: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description='Generate PRS report')
    parser.add_argument('--prs-summary', required=True, help='PRS summary TSV (from PRSice-2)')
    parser.add_argument('--percentiles', required=True, help='Percentiles JSON')
    parser.add_argument('--risk-categories', required=True, help='Risk categories JSON')
    parser.add_argument('--recommendations', required=True, help='Recommendations JSON')
    parser.add_argument('--include-radar', action='store_true', help='Include radar chart')
    parser.add_argument('--include-lifestyle', action='store_true', help='Include lifestyle advice')
    parser.add_argument('--output-html', required=True, help='Output HTML report')
    parser.add_argument('--output-json', required=True, help='Output summary JSON')
    parser.add_argument('--output-radar', help='Output radar chart SVG')
    
    args = parser.parse_args()
    
    # Parse PRSice summary (TSV)
    prs_summary_data = parse_prsice_summary(args.prs_summary)
    
    with open(args.percentiles, 'r') as f:
        percentiles = json.load(f)
    
    with open(args.risk_categories, 'r') as f:
        risk_categories = json.load(f)
    
    with open(args.recommendations, 'r') as f:
        recommendations = json.load(f)
    
    if args.include_radar and args.output_radar:
        generate_radar_chart(risk_categories.get('results', []), args.output_radar)
    
    generate_html_report(
        prs_summary_data, percentiles, risk_categories, recommendations,
        args.include_radar, args.include_lifestyle,
        args.output_html, args.output_radar
    )
    
    generate_summary_json(prs_summary_data, percentiles, risk_categories, recommendations, args.output_json)
    
    print(f"HTML report generated: {args.output_html}")
    print(f"Summary JSON generated: {args.output_json}")
    if args.output_radar:
        print(f"Radar chart generated: {args.output_radar}")


if __name__ == '__main__':
    main()

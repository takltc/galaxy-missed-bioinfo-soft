#!/usr/bin/env python3
"""
PRS Percentile Calculator
Calculate population percentiles for polygenic risk scores.
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


def calculate_percentiles(prs_file: str, population: str, reference_size: int, output_file: str) -> None:
    prs_df = pd.read_csv(prs_file, sep='\t')
    
    score_col = None
    for col in ['PRS', 'SCORE', 'Score', 'prs', 'score', 'SCORESUM']:
        if col in prs_df.columns:
            score_col = col
            break
    
    if score_col is None:
        score_col = prs_df.columns[-1]
    
    id_col = None
    for col in ['IID', 'FID', 'ID', 'Sample', 'SAMPLE']:
        if col in prs_df.columns:
            id_col = col
            break
    
    if id_col is None:
        id_col = prs_df.columns[0]
    
    scores = prs_df[score_col].values
    mean_score = np.mean(scores)
    std_score = np.std(scores)
    
    z_scores = (scores - mean_score) / std_score if std_score > 0 else np.zeros_like(scores)
    percentiles = stats.norm.cdf(z_scores) * 100
    
    results = []
    for idx, row in prs_df.iterrows():
        sample_id = str(row[id_col])
        score = float(row[score_col])
        z = float(z_scores[idx])
        pct = float(percentiles[idx])
        
        results.append({
            "sample_id": sample_id,
            "prs_score": round(score, 6),
            "z_score": round(z, 4),
            "percentile": round(pct, 2),
            "population": population,
            "reference_size": reference_size
        })
    
    output = {
        "metadata": {
            "population": population,
            "reference_size": reference_size,
            "mean_score": round(mean_score, 6),
            "std_score": round(std_score, 6),
            "n_samples": len(results)
        },
        "results": results
    }
    
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Calculated percentiles for {len(results)} samples")
    print(f"Output written to {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Calculate PRS percentiles')
    parser.add_argument('--prs', required=True, help='PRS scores file (TSV format)')
    parser.add_argument('--population', default='EAS', help='Reference population')
    parser.add_argument('--reference-size', type=int, default=10000, help='Reference population size')
    parser.add_argument('--output', required=True, help='Output JSON file')
    
    args = parser.parse_args()
    
    calculate_percentiles(args.prs, args.population, args.reference_size, args.output)


if __name__ == '__main__':
    main()

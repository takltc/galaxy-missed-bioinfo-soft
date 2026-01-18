#!/usr/bin/env python3
"""
PRS Risk Interpreter
Interpret PRS percentiles and generate risk categories with recommendations.
"""
import argparse
import json
import sys
from typing import Dict, List, Any


RISK_CATEGORIES = {
    "very_high": {
        "percentile_min": 95,
        "label": "Very High Risk",
        "label_zh": "极高风险",
        "color": "#dc2626",
        "action": "specialist_referral",
        "description": "Significantly elevated genetic risk. Recommend specialist consultation.",
        "description_zh": "遗传风险显著升高。建议专科会诊。"
    },
    "high": {
        "percentile_min": 90,
        "label": "High Risk",
        "label_zh": "高风险",
        "color": "#ea580c",
        "action": "enhanced_screening",
        "description": "Elevated genetic risk. Enhanced screening recommended.",
        "description_zh": "遗传风险升高。建议加强筛查。"
    },
    "elevated": {
        "percentile_min": 75,
        "label": "Elevated Risk",
        "label_zh": "风险升高",
        "color": "#f59e0b",
        "action": "lifestyle_modification",
        "description": "Moderately elevated risk. Lifestyle modifications recommended.",
        "description_zh": "风险中度升高。建议调整生活方式。"
    },
    "average": {
        "percentile_min": 25,
        "label": "Average Risk",
        "label_zh": "平均风险",
        "color": "#22c55e",
        "action": "standard_screening",
        "description": "Population average risk. Standard screening recommended.",
        "description_zh": "风险处于人群平均水平。建议标准筛查。"
    },
    "low": {
        "percentile_min": 0,
        "label": "Low Risk",
        "label_zh": "低风险",
        "color": "#3b82f6",
        "action": "standard_screening",
        "description": "Below average genetic risk. Standard screening recommended.",
        "description_zh": "遗传风险低于平均水平。建议标准筛查。"
    }
}


LIFESTYLE_RECOMMENDATIONS = {
    "cardiovascular": [
        "Regular aerobic exercise (150 min/week)",
        "Heart-healthy diet (Mediterranean or DASH)",
        "Blood pressure monitoring",
        "Lipid panel testing annually",
        "Smoking cessation if applicable"
    ],
    "diabetesT2": [
        "Maintain healthy body weight",
        "Regular physical activity",
        "Limit refined carbohydrates",
        "Annual fasting glucose testing",
        "HbA1c monitoring if elevated risk"
    ],
    "breastCancer": [
        "Regular mammography screening",
        "Clinical breast exams",
        "Maintain healthy weight",
        "Limit alcohol consumption",
        "Consider genetic counseling for very high risk"
    ],
    "default": [
        "Maintain healthy lifestyle",
        "Regular health checkups",
        "Balanced diet and exercise",
        "Discuss results with healthcare provider"
    ]
}


def get_risk_category(percentile: float, custom_thresholds: Dict = None) -> Dict:
    thresholds = custom_thresholds or RISK_CATEGORIES
    
    for category, info in sorted(thresholds.items(), key=lambda x: -x[1]["percentile_min"]):
        if percentile >= info["percentile_min"]:
            return {
                "category": category,
                **info
            }
    
    return {
        "category": "low",
        **RISK_CATEGORIES["low"]
    }


def get_recommendations(category: str, disease: str = None) -> List[str]:
    if disease and disease in LIFESTYLE_RECOMMENDATIONS:
        base_recs = LIFESTYLE_RECOMMENDATIONS[disease]
    else:
        base_recs = LIFESTYLE_RECOMMENDATIONS["default"]
    
    if category in ["very_high", "high"]:
        base_recs = ["Schedule appointment with specialist"] + base_recs
    
    return base_recs


def interpret_results(percentile_file: str, thresholds: Dict, output_categories: str, output_recommendations: str) -> None:
    with open(percentile_file, 'r') as f:
        percentile_data = json.load(f)
    
    results = []
    all_recommendations = []
    
    for sample in percentile_data.get("results", []):
        percentile = sample["percentile"]
        sample_id = sample["sample_id"]
        
        risk_info = get_risk_category(percentile, thresholds)
        
        sample_result = {
            "sample_id": sample_id,
            "percentile": percentile,
            "prs_score": sample.get("prs_score"),
            "z_score": sample.get("z_score"),
            "risk_category": risk_info["category"],
            "risk_label": risk_info["label"],
            "risk_label_zh": risk_info["label_zh"],
            "risk_color": risk_info["color"],
            "action": risk_info["action"],
            "description": risk_info["description"],
            "description_zh": risk_info["description_zh"]
        }
        results.append(sample_result)
        
        recommendations = get_recommendations(risk_info["category"])
        all_recommendations.append({
            "sample_id": sample_id,
            "risk_category": risk_info["category"],
            "recommendations": recommendations
        })
    
    with open(output_categories, 'w') as f:
        json.dump({
            "metadata": percentile_data.get("metadata", {}),
            "risk_thresholds": {k: v["percentile_min"] for k, v in RISK_CATEGORIES.items()},
            "results": results
        }, f, indent=2, ensure_ascii=False)
    
    with open(output_recommendations, 'w') as f:
        json.dump({
            "recommendations": all_recommendations
        }, f, indent=2, ensure_ascii=False)
    
    print(f"Interpreted {len(results)} samples")
    print(f"Risk categories written to {output_categories}")
    print(f"Recommendations written to {output_recommendations}")


def main():
    parser = argparse.ArgumentParser(description='Interpret PRS percentiles')
    parser.add_argument('--percentiles', required=True, help='Percentile results JSON file')
    parser.add_argument('--threshold-high', type=float, default=90, help='High risk threshold')
    parser.add_argument('--threshold-elevated', type=float, default=75, help='Elevated risk threshold')
    parser.add_argument('--threshold-average', type=float, default=25, help='Average risk threshold')
    parser.add_argument('--output-categories', required=True, help='Output risk categories JSON')
    parser.add_argument('--output-recommendations', required=True, help='Output recommendations JSON')
    
    args = parser.parse_args()
    
    custom_thresholds = None
    if args.threshold_high != 90 or args.threshold_elevated != 75 or args.threshold_average != 25:
        custom_thresholds = {
            "very_high": {**RISK_CATEGORIES["very_high"], "percentile_min": 95},
            "high": {**RISK_CATEGORIES["high"], "percentile_min": args.threshold_high},
            "elevated": {**RISK_CATEGORIES["elevated"], "percentile_min": args.threshold_elevated},
            "average": {**RISK_CATEGORIES["average"], "percentile_min": args.threshold_average},
            "low": {**RISK_CATEGORIES["low"], "percentile_min": 0}
        }
    
    interpret_results(args.percentiles, custom_thresholds, args.output_categories, args.output_recommendations)


if __name__ == '__main__':
    main()

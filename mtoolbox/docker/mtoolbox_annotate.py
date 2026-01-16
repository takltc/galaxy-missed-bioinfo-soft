#!/usr/bin/env python3
"""
MToolBox Annotation Entry Point for Galaxy
Based on MToolBox v1.2.1 (PMID:25028726)
"""

import argparse
import json
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

# Add MToolBox to sys.path to import datatypes
MTOOLBOX_PATH_ENV = os.environ.get("MTOOLBOX_PATH", "/opt/mtoolbox/MToolBox")
MTOOLBOX_PATH = Path(MTOOLBOX_PATH_ENV)

if MTOOLBOX_PATH.exists():
    sys.path.insert(0, str(MTOOLBOX_PATH))
else:
    # Try finding it relative to this script
    script_dir = Path(__file__).parent.absolute()
    local_mtoolbox = script_dir / "MToolBox"
    if local_mtoolbox.exists():
        sys.path.insert(0, str(local_mtoolbox))

try:
    from classifier.datatypes2 import SNP_MixIn, Insertion, Deletion
except ImportError as e:
    print(f"Error: Could not import MToolBox modules from {sys.path[0]}: {e}", file=sys.stderr)
    sys.exit(1)

MTOOLBOX_VERSION = "1.2.1"
PMID = "25028726"
MTOOLBOX_DATA_DIR = os.environ.get("MTOOLBOX_DATA_DIR", "/opt/mtoolbox/MToolBox/data")

# Global variable to store column indices derived from patho_table header
PATHO_COLUMN_MAP = {}

# --- Copied from MToolBox/variants_functional_annotation.py ---
# mt coding loci. Used to discriminate coding/non-coding regions for novel variants
MT_CODING_LOCI = [
    'MT-CO1', 'MT-CO2', 'MT-CO3', 'MT-ND1', 'MT-ND2', 'MT-ND3', 
    'MT-ND4', 'MT-ND5', 'MT-ND6', 'MT-ND4L', 'MT-ATP8', 'MT-ATP6', 'MT-CYB'
]

def check_mutation_effect(event, sitevar_row):
    """
    Check if variant maps to coding regions and assign syn/frameshift if novel.
    Based on MToolBox variants_functional_annotation.py logic.
    """
    # sitevar_row indices: 0=Locus, 1=NtVar, 2=CodonPos, 3=AaChange, 4=AaVar
    if len(sitevar_row) > 0 and sitevar_row[0] in MT_CODING_LOCI:
        # Ensure list is long enough to hold AaChange
        while len(sitevar_row) <= 3:
            sitevar_row.append(None)
            
        mutation_type = event.__class__.__name__
        if mutation_type not in ["Insertion", "Deletion"]:
            sitevar_row[3] = "syn"
        else:
            sitevar_row[3] = "frameshift"
    return sitevar_row

def pprint2datatype(event):
    """
    Convert string event to MToolBox datatype.
    Copied from variants_functional_annotation.py to avoid import issues.
    """
    if '(' in event: # ambiguity
        event = event.split('(')[0]
    if event[-1] == "d": #514-515d
        e = event[:-1].split('-')
        if len(e) == 1:
            mut = Deletion("%d-%dd" % (int(e[0]), int(e[0])))
        else:
            mut = Deletion("%d-%dd" % (int(e[0]), int(e[1])))
    elif '.' in event: #310.CC
        e = event.split('.')
        mut = Insertion("%d.%s" % (int(e[0]), e[1]))
    else: #15746C
        pos = int(event[:-1])
        var = event[-1]
        mut = SNP_MixIn()
        mut.start = pos
        mut.change = var
    return mut

def fillPathoDict2(inhandle, d, separator, listindex):
    for line in inhandle:
        x = line.strip().split(separator)
        if len(x) < 1: continue
        a = pprint2datatype(x[0])
        b = x[listindex:]
        for ind, i in enumerate(b):
            try:
                i = float(i)
                b[ind] = i
            except:
                pass
        try:
            b[2] = int(b[2])
        except:
            pass
        d.setdefault(a, []).append(b)
    return d

def fillSiteVarDict(inhandle, d, separator, listindex):
    for line in inhandle:
        x = line.strip().split(separator)
        if len(x) < 1: continue
        try:
            a = int(x[0])
        except ValueError:
            continue
        b = []
        b.extend(x[listindex:])
        d[a] = b
    return d

# --- End Copied Code ---

def load_mtoolbox_data(data_dir: str) -> Tuple[Dict, Dict]:
    """
    Load MToolBox data. Dynamically parses header to map columns.
    """
    patho_file = Path(data_dir) / "patho_table.txt"
    site_file = Path(data_dir) / "sitevar_modified.txt"
    
    d = {}
    g = {}
    
    if patho_file.exists():
        print("Parsing pathogenicity table...", file=sys.stderr)
        with open(patho_file, 'r', encoding='utf-8', errors='ignore') as f:
            all_lines = f.readlines()
            
        if not all_lines:
            print("Error: patho_table.txt is empty", file=sys.stderr)
            sys.exit(1)
            
        # Parse header to build column map
        # Header line example: "	Nt Position	Locus	Nt Variability..." (starts with TAB)
        # We must use rstrip() because strip() would remove the leading empty field (Variant ID placeholder)
        header_cols = all_lines[0].rstrip().split('\t')
        
        # We start from index 2 because fillPathoDict2 slices x[2:]
        # So header_cols[2] corresponds to value list index 0
        global PATHO_COLUMN_MAP
        PATHO_COLUMN_MAP = {}
        
        for i, col_name in enumerate(header_cols[2:]):
            # Normalize column name to snake_case key
            # e.g. "Mitomap Associated Disease(s)" -> "mitomap_associated_disease"
            key = col_name.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_").replace("-", "_").replace("&", "_")
            
            # Map common variations just in case
            if key == "clinvar": key = "clinvar"
            if key == "dbsnp_id": key = "dbsnp"
            if key == "omim_link": key = "omim"
            if key == "mamit_trna_link": key = "mamit_trna"
            if key == "mitomap_associated_diseases": key = "mitomap_associated_disease"
            
            PATHO_COLUMN_MAP[key] = i
            
        # Verify critical columns exist
        critical_keys = ["mitomap_associated_disease", "mitomap_homoplasmy", "clinvar"]
        for k in critical_keys:
            if k not in PATHO_COLUMN_MAP:
                print(f"Warning: Critical column '{k}' not found in patho_table header. ACMG classification may fail.", file=sys.stderr)

        lines = all_lines[1:]
        d = fillPathoDict2(lines, d, '\t', 2)
        print(f"Loaded {len(d)} variant annotations from patho_table.txt", file=sys.stderr)
    else:
        print(f"Warning: Patho table not found at {patho_file}", file=sys.stderr)
    
    if site_file.exists():
        print("Parsing variability data...", file=sys.stderr)
        with open(site_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()[1:]
        g = fillSiteVarDict(lines, g, '\t', 1)
        for pos in g.keys():
            try:
                g[pos][1] = float(g[pos][1])
            except (ValueError, TypeError, IndexError):
                pass
            try:
                g[pos][4] = float(g[pos][4])
            except (ValueError, TypeError, IndexError):
                pass
        print(f"Loaded {len(g)} site annotations from sitevar_modified.txt", file=sys.stderr)
    else:
        print(f"Warning: Site var table not found at {site_file}", file=sys.stderr)
    
    return d, g

def vcf_to_mtoolbox_string(pos: int, ref: str, alt: str) -> str:
    """
    Convert VCF variant to MToolBox string format.
    """
    if len(ref) == 1 and len(alt) == 1:
        # SNP
        return f"{pos}{alt}"
    
    if len(ref) > len(alt):
        # Deletion
        common = os.path.commonprefix([ref, alt])
        prefix_len = len(common)
        del_seq = ref[prefix_len:]
        start = pos + prefix_len
        end = start + len(del_seq) - 1
        
        if start == end:
            return f"{start}d"
        else:
            return f"{start}-{end}d"
            
    if len(ref) < len(alt):
        # Insertion
        common = os.path.commonprefix([ref, alt])
        prefix_len = len(common)
        ins_seq = alt[prefix_len:]
        ins_pos = pos + prefix_len - 1
        return f"{ins_pos}.{ins_seq}"
        
    return f"{pos}{alt}"

def get_annotation(pos: int, ref: str, alt: str, d: Dict, g: Dict) -> Dict[str, Any]:
    """Get annotation for a variant."""
    mt_str = vcf_to_mtoolbox_string(pos, ref, alt)
    
    try:
        mt_obj = pprint2datatype(mt_str)
    except Exception:
        mt_obj = None
    
    result = {
        "position": pos,
        "ref": ref,
        "alt": alt,
        "variant_id": f"m.{pos}{ref}>{alt}",
        "mtoolbox_id": mt_str
    }
    
    # Check if variant is in patho_table (known pathogenic/annotated variants)
    if mt_obj and mt_obj in d:
        patho_data = d[mt_obj][0] # d values are lists of lists
        
        # PATHO_COLUMN_MAP is populated during load_mtoolbox_data
        for key, idx in PATHO_COLUMN_MAP.items():
            if idx < len(patho_data):
                val = patho_data[idx]
                if val == 'NA' or val == '':
                    val = None
                result[key] = val
    
    # Fallback: Check sitevar (positional data) if not fully annotated
    # This logic mimics MToolBox's behavior for novel variants
    elif pos in g:
        # Create a copy of site data to avoid modifying the global dict
        site_data = list(g[pos]) # [Locus, NtVar, CodonPos, AaChange, AaVar, ...]
        
        # Apply MToolBox logic for novel variants in coding regions
        if mt_obj:
            site_data = check_mutation_effect(mt_obj, site_data)
        
        # Map site_data to result fields
        # Note: site_data indices align with the beginning of PATHO_HEADER
        # Locus=0, NtVar=1, CodonPos=2, AaChange=3, AaVar=4
        if len(site_data) > 0: result["locus"] = site_data[0]
        if len(site_data) > 1: result["nt_variability"] = site_data[1]
        if len(site_data) > 2: result["codon_position"] = site_data[2]
        if len(site_data) > 3: result["aa_change"] = site_data[3]
        if len(site_data) > 4: result["aa_variability"] = site_data[4]
        if len(site_data) > 5: result["trna_annotation"] = site_data[5]
        
    return result

def determine_acmg_class(annotation: Dict) -> str:
    """
    ACMG/AMP mtDNA classification (PMID:32906214)
    """
    mitomap = annotation.get("mitomap_associated_disease")
    mitomap_homoplasmy = annotation.get("mitomap_homoplasmy")
    
    clinvar = annotation.get("clinvar")
    clinvar_pathogenic = False
    clinvar_benign = False
    
    if clinvar and isinstance(clinvar, str):
        clinvar_lower = clinvar.lower()
        if "pathogenic" in clinvar_lower and "likely" not in clinvar_lower and "conflict" not in clinvar_lower:
            clinvar_pathogenic = True
        if "benign" in clinvar_lower and "likely" not in clinvar_lower and "conflict" not in clinvar_lower:
            clinvar_benign = True

    polyphen = annotation.get("polyphen_2_humvar_prob")
    try:
        polyphen_score = float(polyphen) if polyphen else None
    except (ValueError, TypeError):
        polyphen_score = None

    if (mitomap and mitomap != 'NA' and mitomap_homoplasmy == 'Y') or clinvar_pathogenic:
        return "Pathogenic"

    if (mitomap and mitomap != 'NA') or (polyphen_score and polyphen_score >= 0.85):
        return "Likely_pathogenic"

    if polyphen_score is not None and polyphen_score < 0.15:
        return "Likely_benign"

    if clinvar_benign:
        return "Benign"
        
    return "VUS"

def process_vcf(input_vcf: str, output_vcf: str, output_json: str, output_html: str,
                data_dir: str, include_mitomap: bool, include_clinvar: bool,
                max_frequency: float, apply_acmg: bool):
    
    d, g = load_mtoolbox_data(data_dir)
    
    annotations_list = []
    stats = {
        "total_variants": 0,
        "snvs": 0,
        "indels": 0,
        "pathogenic": 0,
        "likely_pathogenic": 0,
        "vus": 0,
        "benign": 0,
        "with_mitomap_disease": 0,
        "filtered_by_frequency": 0,
    }
    
    header_lines = []
    variant_lines = []
    
    with open(input_vcf, "r") as f:
        for line in f:
            if line.startswith("##"):
                header_lines.append(line.rstrip())
            elif line.startswith("#CHROM"):
                header_lines.append('##INFO=<ID=MTOOLBOX_LOCUS,Number=1,Type=String,Description="Gene locus from MToolBox">')
                header_lines.append('##INFO=<ID=MTOOLBOX_VARIABILITY,Number=1,Type=Float,Description="Nucleotide variability from HmtDB">')
                if include_mitomap:
                    header_lines.append('##INFO=<ID=MITOMAP_DISEASE,Number=1,Type=String,Description="Disease association from MITOMAP">')
                if include_clinvar:
                    header_lines.append('##INFO=<ID=CLINVAR,Number=1,Type=String,Description="ClinVar classification">')
                if apply_acmg:
                    header_lines.append('##INFO=<ID=ACMG_CLASS,Number=1,Type=String,Description="ACMG classification (PMID:32906214)">')
                header_lines.append('##INFO=<ID=POLYPHEN2,Number=1,Type=String,Description="PolyPhen-2 prediction">')
                header_lines.append('##INFO=<ID=PHYLOP,Number=1,Type=Float,Description="PhyloP conservation score">')
                header_lines.append(line.rstrip())
            else:
                fields = line.rstrip().split("\t")
                if len(fields) < 8:
                    continue
                
                chrom, pos_str, id_, ref, alt, qual, filter_, info = fields[:8]
                
                try:
                    pos = int(pos_str)
                except ValueError:
                    continue
                
                info_dict = {}
                if info and info != ".":
                    for field in info.split(";"):
                        if "=" in field:
                            key, value = field.split("=", 1)
                            info_dict[key] = value
                
                af = info_dict.get("AF", "0.0")
                try:
                    af_val = float(af)
                except ValueError:
                    af_val = 0.0
                
                if af_val > max_frequency:
                    stats["filtered_by_frequency"] += 1
                    continue
                
                for alt_allele in alt.split(","):
                    stats["total_variants"] += 1
                    
                    if len(ref) == 1 and len(alt_allele) == 1:
                        stats["snvs"] += 1
                    else:
                        stats["indels"] += 1
                    
                    annotation = get_annotation(pos, ref, alt_allele, d, g)
                    
                    if apply_acmg:
                        annotation["acmg_class"] = determine_acmg_class(annotation)
                        acmg = annotation["acmg_class"]
                        if acmg == "Pathogenic":
                            stats["pathogenic"] += 1
                        elif acmg == "Likely_pathogenic":
                            stats["likely_pathogenic"] += 1
                        elif acmg == "VUS":
                            stats["vus"] += 1
                        else:
                            stats["benign"] += 1
                    
                    mitomap_disease = annotation.get("mitomap_associated_disease")
                    if mitomap_disease and mitomap_disease != 'NA':
                        stats["with_mitomap_disease"] += 1
                    
                    annotations_list.append(annotation)
                    
                    new_info_parts = [info] if info != "." else []
                    
                    if annotation.get("locus"):
                        new_info_parts.append(f"MTOOLBOX_LOCUS={annotation['locus']}")
                    
                    if annotation.get("nt_variability") is not None:
                        new_info_parts.append(f"MTOOLBOX_VARIABILITY={annotation['nt_variability']}")
                    
                    if include_mitomap and mitomap_disease and mitomap_disease != 'NA':
                        safe_disease = str(mitomap_disease).replace(";", ",").replace(" ", "_").replace("=", ":")
                        new_info_parts.append(f"MITOMAP_DISEASE={safe_disease}")
                    
                    if include_clinvar and annotation.get("clinvar") and annotation.get("clinvar") != 'NA':
                         safe_clinvar = str(annotation['clinvar']).replace(";", ",").replace(" ", "_").replace("=", ":")
                         new_info_parts.append(f"CLINVAR={safe_clinvar}")
                    
                    polyphen = annotation.get("polyphen_2_humvar_prob")
                    if polyphen and polyphen != 'NA':
                        new_info_parts.append(f"POLYPHEN2={polyphen}")
                    
                    phylop = annotation.get("phylop100way")
                    if phylop and phylop != 'NA':
                        new_info_parts.append(f"PHYLOP={phylop}")
                    
                    if apply_acmg:
                        new_info_parts.append(f"ACMG_CLASS={annotation['acmg_class']}")
                    
                    fields[7] = ";".join(new_info_parts) if new_info_parts else "."
                    variant_lines.append("\t".join(fields))
    
    with open(output_vcf, "w") as f:
        for line in header_lines:
            f.write(line + "\n")
        for line in variant_lines:
            f.write(line + "\n")
    
    report = {
        "tool": "MToolBox",
        "version": MTOOLBOX_VERSION,
        "pmid": PMID,
        "data_source": data_dir,
        "timestamp": datetime.now().isoformat(),
        "statistics": stats,
        "databases": {
            "patho_table_variants": len(d),
            "sitevar_positions": len(g),
            "mitomap": include_mitomap,
            "clinvar": include_clinvar,
        },
        "parameters": {
            "max_frequency": max_frequency,
            "apply_acmg": apply_acmg,
        },
        "annotations": annotations_list,
    }
    
    with open(output_json, "w") as f:
        json.dump(report, f, indent=2, default=str)
    
    generate_html_report(report, output_html)
    
    return stats

def generate_html_report(report: dict, output_html: str):
    stats = report["statistics"]
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>MToolBox Annotation Report</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
        .stat-card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; }}
        .stat-card.pathogenic {{ background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); }}
        .stat-card.benign {{ background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%); }}
        .stat-value {{ font-size: 2.5em; font-weight: bold; }}
        .stat-label {{ font-size: 0.9em; opacity: 0.9; margin-top: 5px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #3498db; color: white; }}
        tr:hover {{ background: #f5f5f5; }}
        .pathogenic {{ color: #e74c3c; font-weight: bold; }}
        .vus {{ color: #f39c12; }}
        .benign {{ color: #27ae60; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #7f8c8d; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>MToolBox Annotation Report</h1>
        <p><strong>Version:</strong> {report['version']} | 
           <strong>PMID:</strong> <a href="https://pubmed.ncbi.nlm.nih.gov/{report['pmid']}/">{report['pmid']}</a> |
           <strong>Generated:</strong> {report['timestamp']}</p>
        <p><strong>Data source:</strong> {report['data_source']} 
           ({report['databases']['patho_table_variants']} variants, {report['databases']['sitevar_positions']} positions)</p>
        
        <h2>Summary Statistics</h2>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{stats['total_variants']}</div>
                <div class="stat-label">Total Variants</div>
            </div>
            <div class="stat-card pathogenic">
                <div class="stat-value">{stats['pathogenic']}</div>
                <div class="stat-label">Pathogenic</div>
            </div>
            <div class="stat-card pathogenic">
                <div class="stat-value">{stats['likely_pathogenic']}</div>
                <div class="stat-label">Likely Pathogenic</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['with_mitomap_disease']}</div>
                <div class="stat-label">With MITOMAP Disease</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['vus']}</div>
                <div class="stat-label">VUS</div>
            </div>
        </div>
        
        <h2>Annotated Variants</h2>
        <table>
            <thead>
                <tr>
                    <th>Variant</th>
                    <th>Locus</th>
                    <th>MITOMAP Disease</th>
                    <th>PolyPhen-2</th>
                    <th>ACMG</th>
                </tr>
            </thead>
            <tbody>
"""
    
    for ann in report["annotations"][:100]:
        disease = ann.get("mitomap_associated_disease") or "-"
        if disease == 'NA':
            disease = "-"
        acmg = ann.get("acmg_class", "VUS")
        acmg_style = "pathogenic" if acmg in ("Pathogenic", "Likely_pathogenic") else ("vus" if acmg == "VUS" else "benign")
        polyphen = ann.get("polyphen_2_humvar_prob") or "-"
        if polyphen == 'NA':
            polyphen = "-"
        disease_display = str(disease)[:50] + ("..." if len(str(disease)) > 50 else "")
        
        html += f"""                <tr>
                    <td>{ann['variant_id']}</td>
                    <td>{ann.get('locus') or '-'}</td>
                    <td class="{'pathogenic' if disease != '-' else ''}">{disease_display}</td>
                    <td>{polyphen}</td>
                    <td class="{acmg_style}">{acmg}</td>
                </tr>
"""
    
    html += f"""            </tbody>
        </table>
        
        <div class="footer">
            <p><strong>Reference:</strong> Calabrese C, et al. MToolBox: a highly automated pipeline for heteroplasmy 
               annotation and prioritization analysis of human mitochondrial variants. Bioinformatics. 2014.
               <a href="https://pubmed.ncbi.nlm.nih.gov/25028726/">PMID:25028726</a>
            </p>
        </div>
    </div>
</body>
</html>"""
    
    with open(output_html, "w") as f:
        f.write(html)

def main():
    parser = argparse.ArgumentParser(
        description="MToolBox Annotate - mtDNA variant annotation using MToolBox data files (PMID:25028726)"
    )
    
    parser.add_argument("--input-vcf", required=True)
    parser.add_argument("--output-vcf", required=True)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-html", required=True)
    parser.add_argument("--data-dir", default=MTOOLBOX_DATA_DIR,
                        help=f"MToolBox data directory (default: {MTOOLBOX_DATA_DIR})")
    parser.add_argument("--include-mitomap", action="store_true")
    parser.add_argument("--include-hmtdb", action="store_true")
    parser.add_argument("--include-clinvar", action="store_true")
    parser.add_argument("--include-gnomad-mtdna", action="store_true")
    parser.add_argument("--max-frequency", type=float, default=1.0)
    parser.add_argument("--haplogroup", default=None)
    parser.add_argument("--apply-acmg-criteria", action="store_true")
    parser.add_argument("--nomenclature", default="rCRS")
    parser.add_argument("--reference", default="rCRS")
    parser.add_argument("--version", action="version", version=f"MToolBox Annotate {MTOOLBOX_VERSION}")
    
    args = parser.parse_args()
    
    if not Path(args.input_vcf).exists():
        print(f"Error: Input VCF file not found: {args.input_vcf}", file=sys.stderr)
        sys.exit(1)
    
    stats = process_vcf(
        input_vcf=args.input_vcf,
        output_vcf=args.output_vcf,
        output_json=args.output_json,
        output_html=args.output_html,
        data_dir=args.data_dir,
        include_mitomap=args.include_mitomap,
        include_clinvar=args.include_clinvar,
        max_frequency=args.max_frequency,
        apply_acmg=args.apply_acmg_criteria,
    )
    
    print(f"MToolBox Annotation Complete")
    print(f"  Total variants: {stats['total_variants']}")
    print(f"  With MITOMAP disease: {stats['with_mitomap_disease']}")
    print(f"  Pathogenic: {stats['pathogenic']}")
    print(f"  Likely pathogenic: {stats['likely_pathogenic']}")
    print(f"  VUS: {stats['vus']}")

if __name__ == "__main__":
    main()

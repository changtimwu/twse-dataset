#!/usr/bin/env python3
"""
Query company_profiles.jsonl with simple filters — no Python scripting required.

Multiple filters are ANDed. The dataset is looked up in this order:
  1. --file PATH (explicit)
  2. ./company_profiles.jsonl  (current directory)
  3. ~/.claude/skills/twse-fetch/company_profiles.jsonl  (installed skill)

Examples
--------
  # 找出所有董事長為洪裕鈞的公司
  query_companies.py --chairman 洪裕鈞

  # 找出所有名字第一個字為「威」的公司
  query_companies.py --name-starts-with 威

  # 半導體業上市公司，按資本額排前 10 名
  query_companies.py --industry 半導體業 --market 上市公司 --top-by-capital 10

  # 主要業務提到 AI 的公司
  query_companies.py --mainbusiness-contains AI

  # 英文名含 "Bio"
  query_companies.py --english-name-contains Bio

  # 單一公司詳細資料
  query_companies.py --code 2330 --full
"""

import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_PATHS = [
    Path("company_profiles.jsonl"),
    Path.home() / ".claude/skills/twse-fetch/company_profiles.jsonl",
]


def find_dataset(explicit=None):
    if explicit:
        p = Path(explicit)
        if not p.exists():
            sys.exit(f"dataset not found: {p}")
        return p
    for p in DEFAULT_PATHS:
        if p.exists():
            return p
    sys.exit("company_profiles.jsonl not found; pass --file PATH "
             "or install the twse-fetch skill.")


def load(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def to_yuan(amount):
    """Parse '259,323,700,670元' → 259323700670."""
    m = re.search(r"([\d,]+)", amount or "")
    return int(m.group(1).replace(",", "")) if m else 0


def matches(r, args):
    if args.code and r.get("code") != args.code:
        return False
    if args.chairman and r.get("chairman") != args.chairman:
        return False
    if args.chairman_contains and args.chairman_contains not in r.get("chairman", ""):
        return False
    if args.president_contains and args.president_contains not in r.get("president", ""):
        return False
    if args.name_starts_with and not r.get("companyName", "").startswith(args.name_starts_with):
        return False
    if args.name_contains and args.name_contains not in r.get("companyName", ""):
        return False
    if args.english_name_contains and args.english_name_contains.lower() not in r.get("companyEnglishName", "").lower():
        return False
    if args.mainbusiness_contains and args.mainbusiness_contains not in r.get("mainBusiness", ""):
        return False
    if args.market and r.get("marketName") != args.market:
        return False
    if args.industry and r.get("industryCategory") != args.industry:
        return False
    if args.industry_contains and args.industry_contains not in r.get("industryCategory", ""):
        return False
    if args.foreign and r.get("foreignCompanyRegisterPlace", "-") in ("-", ""):
        return False
    return True


def print_row(r, full=False):
    abbr = r.get("companyEnglishAbbreviation") or r.get("companyAbbreviation") or ""
    print(f"  {r.get('code',''):>5}  {r.get('marketName','')[:5]}  "
          f"{r.get('companyName',''):24}  ({r.get('industryCategory','')})")
    en = r.get("companyEnglishName", "")
    if en:
        print(f"         en = {en}  ({abbr})")
    if full:
        for k in ("chairman", "president", "spokesperson", "establishDate",
                  "capitalAmount", "internetAddress", "address",
                  "accountingOffice", "mainBusiness"):
            v = r.get(k)
            if v:
                # truncate long business descriptions
                s = v if len(v) < 90 else v[:87] + "..."
                print(f"         {k} = {s}")


def main():
    parser = argparse.ArgumentParser(
        description="Query company_profiles.jsonl with simple filters.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__.split("Examples\n--------\n", 1)[1] if "Examples" in __doc__ else "",
    )
    parser.add_argument("--file", help="Path to company_profiles.jsonl (auto-detected if omitted).")
    parser.add_argument("--code", help="Exact stock code, e.g. 2330.")
    parser.add_argument("--chairman", help="Exact chairman name (e.g. 洪裕鈞).")
    parser.add_argument("--chairman-contains", help="Substring match on chairman name.")
    parser.add_argument("--president-contains", help="Substring match on president field.")
    parser.add_argument("--name-starts-with", help="Chinese companyName starts with this (e.g. 威).")
    parser.add_argument("--name-contains", help="Chinese companyName contains this substring.")
    parser.add_argument("--english-name-contains", help="Case-insensitive substring on companyEnglishName.")
    parser.add_argument("--mainbusiness-contains", help="Substring on mainBusiness description.")
    parser.add_argument("--market", choices=["上市公司", "上櫃公司", "興櫃公司"],
                        help="Market type.")
    parser.add_argument("--industry", help="Exact industry (e.g. 半導體業).")
    parser.add_argument("--industry-contains", help="Substring match on industry.")
    parser.add_argument("--foreign", action="store_true",
                        help="Only foreign-registered companies (-KY/-BM/...).")
    parser.add_argument("--top-by-capital", type=int, metavar="N",
                        help="After filtering, sort by paid-in capital desc and keep N.")
    parser.add_argument("--limit", type=int, default=50,
                        help="Max rows to print (default 50; ignored when --top-by-capital is set).")
    parser.add_argument("--full", action="store_true",
                        help="Print extra fields (chairman, capital, business, ...).")
    parser.add_argument("--count", action="store_true",
                        help="Only print the number of matches.")
    args = parser.parse_args()

    rows = load(find_dataset(args.file))
    matched = [r for r in rows if matches(r, args)]

    if args.top_by_capital:
        matched.sort(key=lambda r: -to_yuan(r.get("capitalAmount", "")))
        filtered_total = len(matched)
        matched = matched[: args.top_by_capital]
        print(f"在 {filtered_total} 家中取資本額前 {len(matched)} 名\n")
    else:
        print(f"找到 {len(matched)} 家公司\n")

    if args.count:
        return

    shown = matched if args.top_by_capital else matched[: args.limit]
    for r in shown:
        print_row(r, full=args.full)
        if args.top_by_capital:
            print(f"         capital = {to_yuan(r.get('capitalAmount',''))/1e8:.1f} 億元")

    if not args.top_by_capital and len(matched) > args.limit:
        print(f"\n  ... +{len(matched) - args.limit} more (raise --limit to see all)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Fetch full company profiles from the TWSE MOPS (Market Observation Post System).

The MOPS company-profile page (t05st03) is a JavaScript single-page app, so the
HTML page itself contains no data. This script calls the underlying JSON API that
the page uses. The API returns ~86 fields per company, each shaped as
{"value": ..., "isHidden": bool}. We keep every field whose isHidden is False
(the ~50 fields that actually carry data for an ordinary company) and write one
JSON object per company to a JSONL file.

Endpoint: POST https://mops.twse.com.tw/mops/api/t05st03  body {"companyId": "<code>"}
A browser-like User-Agent / Referer is required or the WAF rejects the request.
"""

import sys
import json
import time
import argparse
from pathlib import Path

import requests

API_URL = "https://mops.twse.com.tw/mops/api/t05st03"

# The WAF rejects requests without browser-like headers.
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Referer": "https://mops.twse.com.tw/mops/",
    "Origin": "https://mops.twse.com.tw",
}


def clean(value):
    """Coerce a field value to a trimmed string (drops trailing U+3000)."""
    if value is None:
        return ""
    return str(value).strip().strip("　").strip()


def fetch_profile(code, session=None, timeout=30):
    """
    Fetch one company's full profile from MOPS t05st03.

    Returns a dict containing the queried `code` plus every field whose
    isHidden flag is False. On failure, returns {"code": ..., "error": ...}.
    """
    code = str(code).strip()
    http = session or requests
    try:
        resp = http.post(
            API_URL, json={"companyId": code}, headers=HEADERS, timeout=timeout
        )
        data = resp.json()
    except ValueError:
        return {"code": code, "error": "non-JSON response (likely WAF block)"}
    except requests.RequestException as exc:
        return {"code": code, "error": f"request failed: {exc}"}

    if data.get("code") != 200 or not isinstance(data.get("result"), dict):
        return {"code": code,
                "error": data.get("message", "no result (not a company? ETF/fund?)")}

    record = {"code": code}
    for field, cell in data["result"].items():
        if isinstance(cell, dict) and not cell.get("isHidden", False):
            record[field] = clean(cell.get("value"))
    return record


def read_codes(args):
    """Collect stock codes from positional args and/or an --input file."""
    codes = list(args.codes)
    if args.input:
        text = Path(args.input).read_text(encoding="utf-8")
        for token in text.replace(",", " ").split():
            token = token.strip()
            if token:
                codes.append(token)
    seen, unique = set(), []
    for c in codes:
        if c not in seen:
            seen.add(c)
            unique.append(c)
    return unique


def main():
    parser = argparse.ArgumentParser(
        description="Fetch full TWSE company profiles from MOPS into JSONL."
    )
    parser.add_argument("codes", nargs="*", help="Stock codes, e.g. 2330 2317 8299")
    parser.add_argument("--input", help="File of stock codes (whitespace/comma-separated).")
    parser.add_argument("--output", default="company_profiles.jsonl",
                        help="Output JSONL path (default: company_profiles.jsonl).")
    parser.add_argument("--delay", type=float, default=0.3,
                        help="Seconds between requests (default: 0.3).")
    args = parser.parse_args()

    codes = read_codes(args)
    if not codes:
        parser.error("no stock codes provided (give codes or --input FILE)")

    print(f"Fetching {len(codes)} company profile(s) from MOPS...")
    session = requests.Session()
    failures = 0
    with open(args.output, "w", encoding="utf-8") as out:
        for i, code in enumerate(codes, 1):
            record = fetch_profile(code, session=session)
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
            out.flush()
            if "error" in record:
                failures += 1
                print(f"  [{i}/{len(codes)}] {code}: ERROR - {record['error']}")
            else:
                print(f"  [{i}/{len(codes)}] {code}: "
                      f"{record.get('companyEnglishName','')} "
                      f"({len(record) - 1} fields)")
            if i < len(codes) and args.delay:
                time.sleep(args.delay)

    print(f"\nSaved {len(codes)} record(s) to {args.output} "
          f"({len(codes) - failures} ok, {failures} failed)")


if __name__ == "__main__":
    main()

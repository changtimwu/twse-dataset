#!/usr/bin/env python3
"""
Keep company_profiles.jsonl up to date with newly listed / OTC stocks.

Monthly workflow:
  1. Download the live TWSE ISIN lists for listed (strMode=2) and OTC
     (strMode=4) stocks, and extract the current set of ordinary 4-digit
     company codes (the 股票 section).
  2. Compare against the codes already in company_profiles.jsonl.
  3. Fetch MOPS profiles for any *new* codes and add them.
     With --refresh-all (or --refresh-older-than DAYS) existing records are
     re-fetched too, so changed fields (spokesperson, capital, ...) stay current.
  4. Report companies that are no longer listed (delisted); remove them with
     --prune, otherwise they are kept untouched.

The merged file is rewritten sorted by code. Each fetched record carries a
`fetched_at` date so staleness can be tracked across runs.

Typical use (run once a month):
  python3 refresh_company_profiles.py
  python3 refresh_company_profiles.py --dry-run      # preview changes only
  python3 refresh_company_profiles.py --refresh-all  # also re-fetch existing
"""

import sys
import json
import time
import argparse
from pathlib import Path
from datetime import date, datetime, timedelta

import requests
from bs4 import BeautifulSoup

# Reuse the single-company fetcher.
from fetch_company_profile import fetch_profile

ISIN_URL = "https://isin.twse.com.tw/isin/C_public.jsp?strMode={mode}"
ISIN_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}
# strMode -> human label, for the modes that list ordinary companies.
DEFAULT_MODES = {2: "listed (上市)", 4: "OTC (上櫃)"}


def fetch_current_codes(mode, timeout=30, retries=3):
    """Return the set of 4-digit company codes in the 股票 section of an ISIN list."""
    last_exc = None
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(ISIN_URL.format(mode=mode),
                                headers=ISIN_HEADERS, timeout=timeout)
            break
        except requests.RequestException as exc:
            last_exc = exc
            if attempt < retries:
                time.sleep(2 * attempt)  # back off and retry
    else:
        raise RuntimeError(f"ISIN strMode={mode} unreachable after "
                           f"{retries} attempts: {last_exc}")
    try:
        html = resp.content.decode("cp950")
    except UnicodeDecodeError:
        html = resp.content.decode("big5", errors="ignore")
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table")
    if not tables:
        return set()
    table = max(tables, key=lambda t: len(t.find_all("tr")))

    codes, section = set(), None
    for tr in table.find_all("tr"):
        cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
        nonempty = [c for c in cells if c]
        if not nonempty:
            continue
        if len(nonempty) == 1:          # a colspan section header row
            section = nonempty[0]
            continue
        if section != "股票":            # only ordinary stocks, not warrants/ETFs/...
            continue
        code = cells[0].split("　")[0].strip()
        if code.isdigit() and len(code) == 4:
            codes.add(code)
    return codes


def load_profiles(path):
    """Load existing profiles into {code: record}, preserving only company records."""
    records = {}
    if not Path(path).exists():
        return records
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            if "error" in r:            # never persist error lines in the dataset
                continue
            code = r.get("stockId") or r.get("code")
            records[code] = r
    return records


def is_stale(record, cutoff_date):
    """True if the record has no fetched_at or was fetched before cutoff_date."""
    stamp = record.get("fetched_at")
    if not stamp:
        return True
    try:
        return datetime.strptime(stamp, "%Y-%m-%d").date() < cutoff_date
    except ValueError:
        return True


def write_profiles(path, records):
    """Write records to JSONL sorted by code (shorter codes first, then lexically)."""
    with open(path, "w", encoding="utf-8") as f:
        for code in sorted(records, key=lambda c: (len(c), c)):
            f.write(json.dumps(records[code], ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Refresh company_profiles.jsonl with newly listed/OTC stocks."
    )
    parser.add_argument("--file", default="company_profiles.jsonl",
                        help="Profiles JSONL to update in place (default: company_profiles.jsonl).")
    parser.add_argument("--modes", default="2,4",
                        help="Comma-separated ISIN strModes to scan (default: 2,4 = listed + OTC).")
    parser.add_argument("--refresh-all", action="store_true",
                        help="Re-fetch every currently-listed company, not just new ones.")
    parser.add_argument("--refresh-older-than", type=int, metavar="DAYS",
                        help="Also re-fetch existing records whose fetched_at is older than DAYS.")
    parser.add_argument("--prune", action="store_true",
                        help="Remove records for companies no longer listed (delisted).")
    parser.add_argument("--dry-run", action="store_true",
                        help="Report what would change without fetching or writing.")
    parser.add_argument("--delay", type=float, default=0.3,
                        help="Seconds between MOPS requests (default: 0.3).")
    args = parser.parse_args()

    modes = [int(m) for m in args.modes.split(",") if m.strip()]
    today = date.today().isoformat()

    # 1. Current codes from the live ISIN lists.
    current = set()
    for mode in modes:
        label = DEFAULT_MODES.get(mode, f"strMode={mode}")
        codes = fetch_current_codes(mode)
        print(f"  ISIN strMode={mode} ({label}): {len(codes)} company codes")
        current |= codes
    print(f"Current total company codes: {len(current)}")

    # 2. Diff against existing file.
    existing = load_profiles(args.file)
    existing_codes = set(existing.keys())
    new_codes = sorted(current - existing_codes, key=lambda c: (len(c), c))
    delisted = sorted(existing_codes - current, key=lambda c: (len(c), c))

    # Decide which existing codes to re-fetch.
    refresh = set()
    if args.refresh_all:
        refresh = current & existing_codes
    elif args.refresh_older_than is not None:
        cutoff = date.today() - timedelta(days=args.refresh_older_than)
        refresh = {c for c in current & existing_codes if is_stale(existing[c], cutoff)}

    to_fetch = sorted(set(new_codes) | refresh, key=lambda c: (len(c), c))

    print(f"\nExisting records: {len(existing)}")
    print(f"New (to add):     {len(new_codes)}")
    print(f"To re-fetch:      {len(refresh)}")
    print(f"Delisted:         {len(delisted)}"
          + ("  (will prune)" if args.prune else "  (kept)"))
    if delisted:
        print(f"  delisted codes: {', '.join(delisted[:30])}"
              + (" ..." if len(delisted) > 30 else ""))

    if args.dry_run:
        print("\n[dry-run] no fetching or writing performed.")
        return

    if not to_fetch and not (args.prune and delisted):
        print("\nNothing to do — company_profiles.jsonl is already up to date.")
        return

    # 3. Fetch new / refreshed codes.
    session = requests.Session()
    added = updated = failed = 0
    for i, code in enumerate(to_fetch, 1):
        rec = fetch_profile(code, session=session)
        if "error" in rec:
            failed += 1
            print(f"  [{i}/{len(to_fetch)}] {code}: ERROR - {rec['error']}")
        else:
            rec["fetched_at"] = today
            if code in existing_codes:
                updated += 1
            else:
                added += 1
            existing[code] = rec
        if i < len(to_fetch) and args.delay:
            time.sleep(args.delay)

    # 4. Prune delisted if requested.
    pruned = 0
    if args.prune:
        for code in delisted:
            existing.pop(code, None)
            pruned += 1

    write_profiles(args.file, existing)
    print(f"\nDone. added={added} updated={updated} failed={failed} "
          f"pruned={pruned}  total now={len(existing)}")
    print(f"Wrote {args.file}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Fetch all TWSE market data categories and save as CSV files.
"""

import subprocess
import sys
from pathlib import Path


def fetch_all_modes():
    """Fetch all available TWSE market modes."""

    modes = {
        '1': 'Public Company Bonds',
        '2': 'Listed Stocks',
        '3': 'Convertible Bonds',
        '4': 'OTC Stocks',
        '5': 'Emerging Stocks',
        '6': 'Futures & Options',
        '8': 'Innovation Board',
    }

    results = {}

    for mode, description in modes.items():
        url = f"https://isin.twse.com.tw/isin/C_public.jsp?strMode={mode}"
        print(f"\n{'='*70}")
        print(f"Fetching strMode={mode}: {description}")
        print('='*70)

        try:
            # Import and use the fetch function
            import fetch_twse_stocks
            output_file = fetch_twse_stocks.fetch_twse_stocks(url)
            results[mode] = {
                'description': description,
                'output': output_file,
                'status': 'Success'
            }
        except Exception as e:
            print(f"Error fetching mode {mode}: {e}")
            results[mode] = {
                'description': description,
                'output': None,
                'status': f'Error: {str(e)}'
            }

    # Print summary
    print(f"\n{'='*70}")
    print("SUMMARY")
    print('='*70)

    success_count = sum(1 for r in results.values() if r['status'] == 'Success')

    for mode in sorted(results.keys()):
        result = results[mode]
        status_symbol = '✓' if result['status'] == 'Success' else '✗'
        print(f"[{status_symbol}] Mode {mode}: {result['description']}")
        if result['output']:
            print(f"     -> {result['output']}")

    print(f"\nTotal: {success_count}/{len(results)} modes fetched successfully")
    return results


if __name__ == '__main__':
    results = fetch_all_modes()

    # Exit with error code if any fetch failed
    if any(r['status'] != 'Success' for r in results.values()):
        sys.exit(1)

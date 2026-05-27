#!/usr/bin/env python3
"""
Fetch stock list from TWSE (Taiwan Stock Exchange) and save as CSV.
Supports different strMode values for different stock categories.
"""

import requests
from bs4 import BeautifulSoup
import csv
import sys
from pathlib import Path


def fetch_twse_stocks(url, output_file=None):
    """
    Fetch stock list from TWSE URL and save as CSV.

    Args:
        url: TWSE URL to fetch
        output_file: Output CSV filename (optional, derived from strMode if not provided)

    Returns:
        Path to saved CSV file
    """
    # Parse strMode from URL to determine category
    if 'strMode=' in url:
        str_mode = url.split('strMode=')[1].split('&')[0]
    else:
        str_mode = '2'

    # Determine output filename if not provided
    if output_file is None:
        mode_names = {
            '1': 'twse_bonds',
            '2': 'twse_listed_stocks',
            '3': 'twse_convertible_bonds',
            '4': 'twse_otc_stocks',
            '5': 'twse_emerging_stocks',
            '6': 'twse_futures_options',
            '8': 'twse_innovation_board',
        }
        output_file = f"{mode_names.get(str_mode, f'twse_mode_{str_mode}')}.csv"

    print(f"Fetching from: {url}")
    print(f"strMode: {str_mode}")

    # Fetch page
    response = requests.get(url, timeout=30)

    # Decode using cp950 (Extended Big5 for Traditional Chinese)
    try:
        html_text = response.content.decode('cp950')
        print("Decoded with cp950")
    except:
        html_text = response.content.decode('big5', errors='ignore')
        print("Decoded with big5 (with error handling)")

    # Parse HTML
    soup = BeautifulSoup(html_text, 'html.parser')

    # Find all tables
    tables = soup.find_all('table')
    print(f"Found {len(tables)} tables")

    if not tables:
        print("Error: No tables found")
        return None

    # Get the largest table (should be the stock list)
    table = max(tables, key=lambda t: len(t.find_all('tr')))
    rows_count = len(table.find_all('tr'))
    print(f"Selected table with {rows_count} rows")

    # Extract all rows
    all_rows = []
    for tr in table.find_all('tr'):
        cols = tr.find_all(['td', 'th'])
        row = [col.get_text(strip=True) for col in cols]
        if row:
            all_rows.append(row)

    print(f"Extracted {len(all_rows)} rows")

    # Show first few rows
    print(f"\nFirst 3 rows:")
    for row in all_rows[:3]:
        print(f"  {row}")

    # Save to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(all_rows)

    print(f"\nSaved to {output_file}")
    return output_file


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python fetch_twse_stocks.py <url> [output_file]")
        print("\nExamples:")
        print("  python fetch_twse_stocks.py 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=2'")
        print("  python fetch_twse_stocks.py 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=4' otc_stocks.csv")
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    fetch_twse_stocks(url, output_file)

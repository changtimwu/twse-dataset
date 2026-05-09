# TWSE Dataset

Taiwan Stock Exchange (TWSE) stock listing data collected from the official ISIN database.

## Data Files

All CSV files contain Taiwan Stock Exchange data organized by market category:

- **twse_mode_1.csv** — Public Company Bonds (strMode=1)
  - 294 rows
  - Government and corporate bonds

- **twse_stock_list.csv** — Listed Stocks (strMode=2)
  - 32,110 rows
  - All stocks actively listed on the Taiwan Stock Exchange

- **twse_mode_3.csv** — Convertible Bonds (strMode=3)
  - 3,244 rows
  - Corporate convertible bonds with maturity dates and interest rates

- **twse_mode_4.csv** — OTC/Emerging Stocks (strMode=4)
  - 10,640 rows
  - OTC (over-the-counter) and emerging stock warrants

- **twse_mode_5.csv** — Emerging Stocks (strMode=5)
  - 348 rows
  - Emerging company stocks (興櫃)

- **twse_mode_6.csv** — Futures & Options (strMode=6)
  - 10,393 rows
  - Futures contracts and options

- **twse_mode_8.csv** — Innovation Board (strMode=8)
  - 135 rows
  - Innovation board stocks (創櫃板)

## Columns

All CSV files contain the following columns:

- **有價證券代號及名稱** — Stock Code and Name
- **國際證券辨識號碼(ISIN Code)** — ISIN Code
- **上市日** — Listing Date
- **市場別** — Market Type (上市/上櫃)
- **產業別** — Industry Classification
- **CFICode** — Classification of Financial Instruments Code
- **備註** — Remarks/Notes

## Scripts

### fetch_twse_stocks.py

Fetches TWSE stock data from the official database and saves as CSV.

**Usage:**
```bash
python3 fetch_twse_stocks.py <url> [output_file]
```

**Examples:**
```bash
# Fetch listed stocks (default)
python3 fetch_twse_stocks.py "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2"

# Fetch OTC stocks
python3 fetch_twse_stocks.py "https://isin.twse.com.tw/isin/C_public.jsp?strMode=4" otc_stocks.csv
```

**Supported strMode values:**
- `1` — Public Company Bonds
- `2` — Listed Stocks (上市)
- `3` — Convertible Bonds
- `4` — OTC Stocks (上櫃)
- `5` — Emerging Stocks (興櫃)
- `6` — Futures & Options
- `8` — Innovation Board (創櫃板)

## Data Source

Data is fetched from the official Taiwan Stock Exchange ISIN database:
https://isin.twse.com.tw/isin/C_public.jsp

## Encoding

The data uses cp950 encoding (Extended Big5 for Traditional Chinese) on the source website, automatically converted to UTF-8 in the CSV files.

## Requirements

```bash
pip install requests beautifulsoup4
```

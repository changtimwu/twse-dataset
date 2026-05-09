# TWSE Dataset

Taiwan Stock Exchange (TWSE) stock listing data collected from the official ISIN database.

## Data Files

- **twse_stock_list.csv** — Listed stocks on TWSE (strMode=2)
  - 32,110 rows including headers and category headers
  - Contains all stocks actively listed on the Taiwan Stock Exchange

- **twse_otc_stocks.csv** — OTC/Emerging stocks (strMode=4)
  - 10,640 rows including headers and category headers
  - Contains OTC (over-the-counter) and emerging stock warrants

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
- `2` — Listed Stocks (上市)
- `4` — OTC/Emerging Stocks (上櫃)

## Data Source

Data is fetched from the official Taiwan Stock Exchange ISIN database:
https://isin.twse.com.tw/isin/C_public.jsp

## Encoding

The data uses cp950 encoding (Extended Big5 for Traditional Chinese) on the source website, automatically converted to UTF-8 in the CSV files.

## Requirements

```bash
pip install requests beautifulsoup4
```

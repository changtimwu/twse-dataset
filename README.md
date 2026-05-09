# TWSE Dataset

Taiwan Stock Exchange (TWSE) stock listing data collected from the official ISIN database.

## 🎯 TWSE Fetcher Skill

A reusable Claude Code skill for fetching TWSE data is available in your home directory!

**Installed location:** `~/.claude/skills/twse-fetch/`

### Quick Start with the Skill

```bash
# Fetch listed stocks
python3 ~/.claude/skills/twse-fetch/fetch_twse_stocks.py \
  "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2"

# Or fetch all market categories at once
cd ~/.claude/skills/twse-fetch && python3 fetch_all_twse_modes.py
```

### Skill Features

- ✅ Fetch any market category (7 modes supported)
- ✅ Automatic encoding detection (cp950 → UTF-8)
- ✅ Single mode or batch fetching
- ✅ Standalone scripts, easily portable
- ✅ Complete documentation included

**See the skill documentation:**
- Full guide: `cat ~/.claude/skills/twse-fetch/SKILL.md`
- Quick start: `cat ~/.claude/skills/twse-fetch/QUICKSTART.md`

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

The scripts are available in two locations:

1. **In this repository** — `fetch_twse_stocks.py` (local copy)
2. **In the skill directory** — `~/.claude/skills/twse-fetch/` (preferred for reuse)

### fetch_twse_stocks.py

Fetches TWSE stock data from the official database and saves as CSV.

**Usage from skill directory (recommended):**
```bash
python3 ~/.claude/skills/twse-fetch/fetch_twse_stocks.py <url> [output_file]
```

**Usage from this repository:**
```bash
python3 fetch_twse_stocks.py <url> [output_file]
```

**Examples:**
```bash
# Fetch listed stocks
python3 ~/.claude/skills/twse-fetch/fetch_twse_stocks.py \
  "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2"

# Fetch OTC stocks with custom output
python3 ~/.claude/skills/twse-fetch/fetch_twse_stocks.py \
  "https://isin.twse.com.tw/isin/C_public.jsp?strMode=4" otc_stocks.csv
```

### fetch_all_twse_modes.py

Batch fetch all 7 market categories in one command.

```bash
cd ~/.claude/skills/twse-fetch && python3 fetch_all_twse_modes.py
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

## Integration & Skill Setup

### Using the Installed Skill

The TWSE Fetcher is installed as a Claude Code skill in your home directory:

```bash
# View the full skill documentation
cat ~/.claude/skills/twse-fetch/SKILL.md

# View quick start guide
cat ~/.claude/skills/twse-fetch/QUICKSTART.md

# Copy scripts to your project
cp ~/.claude/skills/twse-fetch/fetch_twse_stocks.py /path/to/your/project/

# Or use directly from the skill directory
python3 ~/.claude/skills/twse-fetch/fetch_twse_stocks.py <url>
```

### Installing Requirements

If you haven't installed dependencies yet:

```bash
# Option 1: Run the skill installer
bash ~/.claude/skills/twse-fetch/install.sh

# Option 2: Manual installation
pip install requests beautifulsoup4
```

### Use in Your Projects

```bash
# Method 1: Copy the script to your project
cp ~/.claude/skills/twse-fetch/fetch_twse_stocks.py ~/my-finance-project/
cd ~/my-finance-project
python3 fetch_twse_stocks.py "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2"

# Method 2: Use from skill directory
python3 ~/.claude/skills/twse-fetch/fetch_twse_stocks.py <url> ~/my-finance-project/data.csv

# Method 3: Add skill directory to PATH
export PATH="~/.claude/skills/twse-fetch:$PATH"
fetch_twse_stocks.py <url>
```

## Requirements

```bash
pip install requests beautifulsoup4
```

Or use the included installation script:

```bash
bash ~/.claude/skills/twse-fetch/install.sh
```

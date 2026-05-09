# TWSE Dataset

Taiwan Stock Exchange (TWSE) stock listing data collected from the official ISIN database.

## 🎯 TWSE Fetcher Skill

A professional Claude Code skill for fetching TWSE data with standard installation.

### ⚡ Install (One-Liner)

```bash
curl -fsSL https://raw.githubusercontent.com/changtimwu/twse-dataset/main/install-skill.sh | bash
```

This installs to `~/.claude/skills/twse-fetch/` with all dependencies.

### 📖 Installation Options

| Method | Command |
|--------|---------|
| **Curl one-liner** (recommended) | `curl -fsSL https://raw.githubusercontent.com/changtimwu/twse-dataset/main/install-skill.sh \| bash` |
| **Local script** | `bash install-skill.sh` |
| **Manual git clone** | `git clone https://github.com/changtimwu/twse-dataset.git ~/.claude/skills/twse-fetch` |
| **Project copy** | `cp fetch_twse_stocks.py /path/to/project/` |

See [INSTALLATION.md](INSTALLATION.md) for detailed installation instructions.

### 🚀 Quick Start

After installation:

```bash
# Fetch listed stocks
python3 ~/.claude/skills/twse-fetch/fetch_twse_stocks.py \
  "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2"

# Or fetch all market categories at once
cd ~/.claude/skills/twse-fetch && python3 fetch_all_twse_modes.py
```

### ✨ Skill Features

- ✅ **7 market categories** — Stocks, bonds, futures, options, emerging, innovation board
- ✅ **Automatic encoding** — cp950 detected and converted to UTF-8
- ✅ **Batch & single fetch** — Fetch one mode or all at once
- ✅ **Portable scripts** — Copy to any project, runs standalone
- ✅ **Complete docs** — SKILL.md, QUICKSTART.md, full examples
- ✅ **Standard manifest** — skill-manifest.json for easy discovery

### 📚 Documentation

- **Full guide:** `~/.claude/skills/twse-fetch/SKILL.md` (or [SKILL.md](SKILL.md) in this repo)
- **Quick start:** `~/.claude/skills/twse-fetch/QUICKSTART.md` 
- **Installation:** [INSTALLATION.md](INSTALLATION.md) — Multiple installation methods
- **Manifest:** [skill-manifest.json](skill-manifest.json) — Skill metadata

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

## Integration & Advanced Usage

### After Installation

```bash
# View the full skill documentation
cat ~/.claude/skills/twse-fetch/SKILL.md

# View quick start guide
cat ~/.claude/skills/twse-fetch/QUICKSTART.md

# Check skill metadata
cat ~/.claude/skills/twse-fetch/skill-manifest.json
```

### Use in Your Projects

```bash
# Method 1: Copy the script to your project
cp ~/.claude/skills/twse-fetch/fetch_twse_stocks.py ~/my-finance-project/
cd ~/my-finance-project
python3 fetch_twse_stocks.py "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2"

# Method 2: Use directly from skill directory
python3 ~/.claude/skills/twse-fetch/fetch_twse_stocks.py <url> ~/my-project/data.csv

# Method 3: Add skill directory to PATH
export PATH="~/.claude/skills/twse-fetch:$PATH"
fetch_twse_stocks.py "https://isin.twse.com.tw/isin/C_public.jsp?strMode=4"

# Method 4: Use in Python scripts
import sys
sys.path.insert(0, os.path.expanduser('~/.claude/skills/twse-fetch'))
from fetch_twse_stocks import fetch_twse_stocks

output = fetch_twse_stocks("https://isin.twse.com.tw/isin/C_public.jsp?strMode=2")
```

## Requirements

Automatically installed by the installer script. Manual installation:

```bash
pip install requests beautifulsoup4
```

See [INSTALLATION.md](INSTALLATION.md) for troubleshooting and alternative installation methods.

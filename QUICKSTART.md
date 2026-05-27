# TWSE Fetcher - Quick Start

## Installation

The skill is already installed in `~/.claude/skills/twse-fetch/`

### Setup dependencies (one-time)
```bash
pip install -r ~/.claude/skills/twse-fetch/requirements.txt
```

## Usage

### Option 1: Fetch a Single Mode

```bash
cd ~/.claude/skills/twse-fetch
python3 fetch_twse_stocks.py "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2"
```

**With custom output filename:**
```bash
python3 fetch_twse_stocks.py "https://isin.twse.com.tw/isin/C_public.jsp?strMode=4" my_otc_stocks.csv
```

### Option 2: Fetch All Modes at Once

```bash
cd ~/.claude/skills/twse-fetch
python3 fetch_all_twse_modes.py
```

This will create 7 CSV files for all available market categories.

## Available Modes

| Mode | Category | Output File |
|------|----------|-------------|
| 1 | Public Bonds | twse_bonds.csv |
| 2 | Listed Stocks | twse_listed_stocks.csv |
| 3 | Convertible Bonds | twse_convertible_bonds.csv |
| 4 | OTC Stocks | twse_otc_stocks.csv |
| 5 | Emerging Stocks | twse_emerging_stocks.csv |
| 6 | Futures & Options | twse_futures_options.csv |
| 8 | Innovation Board | twse_innovation_board.csv |

## Examples

### Fetch just the primary market (listed stocks)
```bash
python3 ~/.claude/skills/twse-fetch/fetch_twse_stocks.py "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2" ~/data/stocks.csv
```

### Fetch bonds in your project directory
```bash
cd ~/my-finance-project
python3 ~/.claude/skills/twse-fetch/fetch_twse_stocks.py "https://isin.twse.com.tw/isin/C_public.jsp?strMode=1"
```

### Create a data directory with all TWSE data
```bash
mkdir -p ~/twse-data
cd ~/twse-data
python3 ~/.claude/skills/twse-fetch/fetch_all_twse_modes.py
ls -lh twse_*.csv
```

## Integration with Your Projects

### Method 1: Direct script copy
```bash
cp ~/.claude/skills/twse-fetch/fetch_twse_stocks.py /path/to/your/project/
cd /path/to/your/project
python3 fetch_twse_stocks.py <url>
```

### Method 2: Use from skill directory
```bash
python3 ~/.claude/skills/twse-fetch/fetch_twse_stocks.py <url>
```

### Method 3: Add to PATH (optional)
```bash
export PATH="~/.claude/skills/twse-fetch:$PATH"
```

## Output Format

Each CSV contains:
- **有價證券代號及名稱** — Security code and name
- **國際證券辨識號碼(ISIN Code)** — ISIN code
- **上市日/發行日/登錄日** — Listing/publication date (varies by mode)
- **市場別** — Market type
- **產業別** — Industry classification
- **CFICode** — Classification code
- **備註** — Remarks/notes

## Troubleshooting

**ImportError: No module named 'requests' or 'bs4'**
```bash
pip install requests beautifulsoup4
```

**Connection timeout**
- TWSE servers usually respond within a few seconds
- Check your internet connection
- Try again after a moment

**Encoding issues in output**
- Output is always UTF-8
- If you need cp950, remove the encoding parameter in the script

## Need Help?

See `SKILL.md` in the skill directory for complete documentation and technical details.

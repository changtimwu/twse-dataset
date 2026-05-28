---
name: TWSE Data Fetcher
description: Fetch Taiwan Stock Exchange data from the official ISIN database (CSV) and full company profiles from MOPS (JSONL)
type: utility
---

# TWSE Data Fetcher Skill

Fetch stock listing data from the Taiwan Stock Exchange (TWSE) official ISIN
database (CSV), and full per-company profiles from the MOPS (Market Observation
Post System) company-profile API (JSONL).

## Overview

This skill provides a streamlined workflow for fetching various categories of TWSE data:
- Listed stocks
- OTC/Emerging stocks  
- Convertible bonds
- Public bonds
- Futures & options
- Innovation board stocks
- **Full company profiles** (English name, capital, people, contacts, business) via MOPS

## Supported Market Categories (strMode)

| Mode | Category | Description |
|------|----------|-------------|
| 1 | Public Bonds | Government and corporate bonds |
| 2 | Listed Stocks | Primary market equities |
| 3 | Convertible Bonds | Corporate convertible securities |
| 4 | OTC Stocks | Over-the-counter and emerging stocks |
| 5 | Emerging Stocks | 興櫃 emerging board |
| 6 | Futures & Options | Derivatives and futures contracts |
| 8 | Innovation Board | 創櫃板 innovation board |

## Quick Start

### Fetch a Single Mode

```bash
python3 fetch_twse_stocks.py "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2"
```

### Fetch All Modes

```bash
python3 fetch_all_twse_modes.py
```

This will create CSV files for all available modes in the current directory.

## Output Format

All CSV files include these columns:
- **有價證券代號及名稱** — Security code and name
- **國際證券辨識號碼(ISIN Code)** — ISIN identifier
- Listing/publication dates
- Market type and industry classification
- CFI codes for classification
- Additional remarks/notes

## Company Profiles (MOPS)

The ISIN database provides only Chinese names. To obtain **English names** and
the full company profile, use `fetch_company_profile.py`, which queries the MOPS
company-profile API (`t05st03`). The MOPS web page is a JavaScript single-page
app and serves no data in its HTML, so the script calls the JSON API directly
(it sends browser-like headers required to pass the MOPS WAF).

```bash
# Explicit stock codes
python3 fetch_company_profile.py 2330 2317 8299

# From a file of codes (whitespace/comma-separated), custom output
python3 fetch_company_profile.py --input company_codes.txt --output profiles.jsonl
```

**Output:** JSONL — one JSON object per company. Each object always includes the
queried `code`; failed lookups (ETFs/warrants/funds are not in the company table)
produce `{"code": ..., "error": ...}`.

The API exposes ~86 fields each shaped as `{"value": ..., "isHidden": bool}`; the
script keeps every field whose `isHidden` is `false` (~50–69 per company).

**Core fields present for every company** (ROC-calendar dates, `yyy/mm/dd`):

| Field | Meaning |
|-------|---------|
| `code` / `stockId` | Stock code (queried / returned) |
| `companyName` / `companyAbbreviation` | Chinese full name / abbreviation |
| `companyEnglishName` / `companyEnglishAbbreviation` | English full name / abbreviation |
| `beforeChangeName` / `beforeChangeAbbreviation` | Previous name / abbreviation (if renamed) |
| `enterpriseUnifiedNumber` | Unified business (tax) number |
| `marketName` | Market type (上市公司 / 上櫃公司 / 興櫃公司) |
| `industryCategory` | Industry classification |
| `reportType` | Financial-report type (合併 / 個別) |
| `establishDate` / `publishDate` | Incorporation / public-offering date |
| `listingDate` / `OTCDate` / `ROTCDate` | TWSE listing / OTC / emerging-board date |
| `chairman` / `president` | Chairman / president |
| `spokesperson`, `spokespersonTitle`, `spokespersonTelephone` | Spokesperson + title + phone |
| `subSpokesperson` | Deputy spokesperson |
| `accounting1` / `accounting2` | Accounting officers |
| `investorLiaison`, `investorLiaisonTitle`, `investorLiaisonEmail`, `investorLiaisonTelephone` | Investor-relations contact |
| `capitalAmount` | Paid-in capital |
| `commonStockAmount` / `commonStockPrice` | Common-stock shares / par value |
| `specialStockAmount` / `haveSpecialStock` | Preferred-stock shares / flag |
| `haveCompanyBonds` | Has corporate bonds (flag) |
| `commonStockDistribute` / `commonStockLevel` | Dividend frequency / approval level |
| `address` / `englishAddress_County` / `englishAddress_Street` | Chinese / English address |
| `telephone` / `faxNumber` / `email` | Phone / fax / email |
| `internetAddress` / `corporateGovernanceLink` / `mops_url_1` / `mops_url_2` | Website / governance / ESG report URLs |
| `accountingOffice` | Auditing (CPA) firm |
| `stockTransferAgency`, `transferAddress`, `transferAgencyTelephone` | Stock-transfer agent + address + phone |
| `foreignCompanyRegisterPlace` | Foreign place of registration (`-` if none) |
| `mainBusiness` | Main business description |
| `note` | Remarks |

**Conditional fields** appear only for certain companies:

- *Innovation board / technology*: `isTechnology`, `applyDate`, `approvedDate`, `approvedOrganization`, `industryRiskDescription`
- *Startups*: `isPublishedAndStartup`, `startupRiskDescription`
- *Financial-report metadata*: `annualFinancialReport`, `semi_annualFinancialReport`, `firstSeasonFinancialReport`, `thirdSeasonFinancialReport`, `reviewAccountingOffice`, `reviewAccounting1`, `reviewAccounting2`, `financialReportRule`, `perUnitAmount`, `keepOrganization`, `depositOrganization`
- *TDR (Taiwan Depositary Receipts)*: `isTDR`, `TDR_Stock`, `TDR_StockMarket`
- *Litigation agent*: `lawsuitAgentName`, `lawsuitAgentEnglishName`, `lawsuitTelephone`, `lawsuitAddress`, `lawsuitEnglishAddress`

MOPS API endpoint: `POST https://mops.twse.com.tw/mops/api/t05st03` with body
`{"companyId": "<code>"}`.

### Querying the dataset

`query_companies.py` answers common natural-language questions against
`company_profiles.jsonl` without any Python scripting. Filters are ANDed; the
dataset is auto-located in the current directory or the installed skill dir.

```bash
# 找出所有董事長為洪裕鈞的公司
python3 query_companies.py --chairman 洪裕鈞

# 找出所有名字第一個字為「威」的公司
python3 query_companies.py --name-starts-with 威

# 半導體業上市公司，按資本額排前 10 名
python3 query_companies.py --industry 半導體業 --market 上市公司 --top-by-capital 10

# 主要業務提到 AI 的公司
python3 query_companies.py --mainbusiness-contains AI

# 英文名含 "Bio"
python3 query_companies.py --english-name-contains Bio

# 單一公司詳細資料
python3 query_companies.py --code 2330 --full

# 最近上櫃 / 最近興櫃 / 最早設立的公司
python3 query_companies.py --market 上櫃公司 --newest-by OTCDate --limit 10
python3 query_companies.py --market 興櫃公司 --newest-by ROTCDate --limit 10
python3 query_companies.py --oldest-by establishDate --limit 5

# 只要統計數字
python3 query_companies.py --market 興櫃公司 --industry 生技醫療業 --count
```

Available filters: `--code`, `--chairman` / `--chairman-contains`,
`--president-contains`, `--name-starts-with` / `--name-contains`,
`--english-name-contains`, `--mainbusiness-contains`, `--market`,
`--industry` / `--industry-contains`, `--foreign`, `--top-by-capital`,
`--newest-by FIELD` / `--oldest-by FIELD` (any date field — `OTCDate`,
`ROTCDate`, `establishDate`, `listingDate`, `publishDate`, …), `--full`,
`--count`. Run `query_companies.py --help` for the full list.

For ad-hoc queries the CLI doesn't cover (e.g. interlocking directorates,
market × industry cross-tabs, oldest companies), load the JSONL in Python and
filter directly — see `EXAMPLES.md` for ready-made recipes.

### Keeping profiles up to date (monthly)

`refresh_company_profiles.py` keeps a `company_profiles.jsonl` current as new
stocks are listed. It downloads the live ISIN lists for listed (`strMode=2`),
OTC (`strMode=4`) and emerging (`strMode=5`) stocks, diffs the company codes
against the file, and fetches MOPS profiles for any new companies. (Listed/OTC
lists are sectioned — only the 股票 section is taken; emerging is a flat list.)

```bash
python3 refresh_company_profiles.py                  # add newly listed/OTC companies
python3 refresh_company_profiles.py --dry-run         # preview changes only
python3 refresh_company_profiles.py --refresh-all      # also re-fetch existing records
python3 refresh_company_profiles.py --refresh-older-than 90
```

- Adds new companies; `--refresh-all` / `--refresh-older-than DAYS` re-fetch
  existing records (via each record's `fetched_at`).
- Reports delisted companies; keeps them by default, removes with `--prune`.
- Rewrites the file sorted by code, stamping `fetched_at` on fetched records.

Schedule monthly via cron, e.g. `0 6 1 * * cd <dir> && python3 refresh_company_profiles.py`.

## Data Source

Official Taiwan Stock Exchange ISIN Database:
https://isin.twse.com.tw/isin/C_public.jsp

## Technical Details

- **Encoding:** cp950 (Extended Big5 for Traditional Chinese)
- **Output Encoding:** UTF-8 CSV
- **Dependencies:** requests, beautifulsoup4
- **Python Version:** 3.6+

## Typical Workflow

1. **Assess requirements** — Decide which market categories you need
2. **Choose fetch method** — Single mode or all modes
3. **Run fetcher** — Execute Python script
4. **Verify output** — Check CSV file contents
5. **Process data** — Use CSV in your analysis/pipeline

## Common Tasks

### Fetch just listed stocks
```bash
python3 fetch_twse_stocks.py "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2" listed_stocks.csv
```

### Fetch bonds with custom output
```bash
python3 fetch_twse_stocks.py "https://isin.twse.com.tw/isin/C_public.jsp?strMode=1" bonds.csv
```

### Setup in a project
```bash
cp fetch_twse_stocks.py /path/to/project/
python3 /path/to/project/fetch_twse_stocks.py <url>
```

## Files

- `fetch_twse_stocks.py` — Single mode ISIN-list fetcher (CSV)
- `fetch_all_twse_modes.py` — Batch ISIN fetcher for all modes
- `fetch_company_profile.py` — MOPS company-profile fetcher (JSONL)
- `refresh_company_profiles.py` — Monthly updater for company_profiles.jsonl
- `query_companies.py` — Filter the dataset from the command line
- `SKILL.md` — This file

## Requirements

```bash
pip install requests beautifulsoup4
```

## Troubleshooting

**Encoding errors:**
- The fetcher automatically detects cp950 encoding
- Output is always UTF-8 for compatibility

**Network timeouts:**
- TWSE server is usually responsive
- Try again if you hit temporary connectivity issues
- You can increase timeout in the script if needed

**Missing data:**
- Some modes may have fewer rows than others
- Empty sections appear as category header rows
- Filter them in post-processing if needed

## Integration

This skill is designed to work with:
- Data processing pipelines
- Financial analysis workflows  
- ETL processes
- Dataset creation and maintenance

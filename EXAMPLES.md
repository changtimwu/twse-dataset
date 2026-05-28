# Skill in Action — Querying `company_profiles.jsonl`

Examples of natural-language questions answered by the **twse-fetch** skill.
For common patterns the skill ships a query CLI (`query_companies.py`); for
ad-hoc questions, load the JSONL and write a one-line filter (any LLM-paired
workflow does this automatically).

**Dataset:** 2,315 companies (1,078 listed 上市 · 889 OTC 上櫃 · 348 emerging 興櫃),
one JSON object per line.

---

## Querying with the CLI

`query_companies.py` answers the most common shapes of questions without any
scripting. Filters are ANDed; the dataset is auto-located.

### Q1.「找出所有董事長為洪裕鈞的公司」

```bash
python3 query_companies.py --chairman 洪裕鈞
```

```
找到 1 家公司

   6858  興櫃公司  愛比科技股份有限公司                (電腦及週邊設備業)
         en = IPEVO CORPORATION  (IPEVO)
```

### Q2.「找出所有名字第一個字為『威』的公司」

```bash
python3 query_companies.py --name-starts-with 威
```

```
找到 13 家公司

   2028  上市公司  威致鋼鐵工業股份有限公司              (鋼鐵工業)
         en = WEI CHIH STEEL INDUSTRIAL CO.,LTD.  (WEI CHIH)
   2388  上市公司  威盛電子股份有限公司                (半導體業)
         en = VIA TECHNOLOGIES, INC.  (VIA)
   3022  上市公司  威強電工業電腦股份有限公司             (電腦及週邊設備業)
         en = IEI Integration Corp.  (IEI)
   3260  上櫃公司  威剛科技股份有限公司                (半導體業)
         en = ADATA Technology Co., Ltd.  (ADATA)
   6756  上市公司  威鋒電子股份有限公司                (半導體業)
         en = VIA LABS, INC.  (VLI)
   7805  上櫃公司  威聯通科技股份有限公司               (數位雲端)
         en = QNAP Systems, Inc.  (QNAP)
   ... (+ 7 more)
```

### Q3.「半導體業上市公司，按資本額排前 5 名」

```bash
python3 query_companies.py --industry 半導體業 --market 上市公司 --top-by-capital 5
```

```
在 94 家中取資本額前 5 名

   2330  上市公司  台灣積體電路製造股份有限公司            (半導體業)
         en = Taiwan Semiconductor Manufacturing Co., Ltd.  (TSMC)
         capital = 2593.2 億元
   2303  上市公司  聯華電子股份有限公司                (半導體業)
         en = UNITED MICROELECTRONICS CORP.  (UMC)
         capital = 1257.7 億元
   2344  上市公司  華邦電子股份有限公司                (半導體業)
         en = Winbond Electronics Corporation  (WEC)
         capital = 450.0 億元
   3711  上市公司  日月光投資控股股份有限公司             (半導體業)
         en = ASE Technology Holding Co., Ltd.  (ASEH)
         capital = 446.1 億元
   6770  上市公司  力晶積成電子製造股份有限公司            (半導體業)
         en = Powerchip Semiconductor Manufacturing Corp.  (PSMC)
         capital = 424.4 億元
```

### Q4.「主要業務提到『AI / 人工智慧』的公司」

```bash
python3 query_companies.py --mainbusiness-contains AI
```

(26 hits across 上市/上櫃/興櫃 — ELAN, JETWELL, PAPAGO, oToBrite, …)

### Q5.「英文名含 Bio 的公司」

```bash
python3 query_companies.py --english-name-contains Bio
```

(Returns 24 biotech-named entities including SunWay Biotech, HANTECH Bio,
SYNBIO, …)

### Q6.「興櫃生技醫療公司有幾家？」

```bash
python3 query_companies.py --market 興櫃公司 --industry 生技醫療業 --count
```

```
找到 95 家公司
```

### Q7.「2330 台積電完整資料」

```bash
python3 query_companies.py --code 2330 --full
```

```
   2330  上市公司  台灣積體電路製造股份有限公司            (半導體業)
         en = Taiwan Semiconductor Manufacturing Co., Ltd.  (TSMC)
         chairman = 魏哲家
         president = 總裁: 魏哲家
         spokesperson = 黃仁昭
         establishDate = 76/02/21
         capitalAmount = 259,323,700,670元
         internetAddress = https://www.tsmc.com
         address = 新竹科學園區力行六路8號
         accountingOffice = 勤業眾信聯合會計師事務所
         mainBusiness = 依客戶之訂單與其提供之產品設計說明，以從事製造與銷售積體電路、以及其他...
```

### Q8.「外國公司（KY、BM…）」

```bash
python3 query_companies.py --foreign --count
```

```
找到 127 家公司
```

### Q9.「最近上櫃 / 最近興櫃公司」

```bash
python3 query_companies.py --market 上櫃公司 --newest-by OTCDate --limit 5
```

```
找到 889 家公司，按 OTCDate 排序（最新優先）

   7819  上櫃公司  精誠金融科技股份有限公司   (資訊服務業)   OTCDate = 2026-05-27
   6983  上櫃公司  華洋精機                  (其他電子業)   OTCDate = 2026-05-25
   7842  上櫃公司  天能綠電                  (綠能環保)     OTCDate = 2026-05-11
   7772  上櫃公司  耀穎光電                  (半導體業)     OTCDate = 2026-05-08
   3485  上櫃公司  敘豐企業                  (電子零組件業) OTCDate = 2026-05-06
```

```bash
python3 query_companies.py --market 興櫃公司 --newest-by ROTCDate --limit 5
```

```
   7898  興櫃公司  乾瞻科技  (半導體業)     ROTCDate = 2026-05-27
   7921  興櫃公司  台普威能源 (綠能環保)    ROTCDate = 2026-05-27
   7922  興櫃公司  源點科技  (綠能環保)     ROTCDate = 2026-05-22
   7920  興櫃公司  瀚陽生物科技 (化學生技)  ROTCDate = 2026-05-20
   7913  興櫃公司  通寶半導體設計 (半導體)  ROTCDate = 2026-05-15
```

`--newest-by` / `--oldest-by` works for any date field: `OTCDate`, `ROTCDate`,
`establishDate`, `listingDate`, `publishDate`, `applyDate`, `approvedDate`,
`changeApprovedDate`, `fetched_at`.

### Q10.「最近設立的公司」

```bash
python3 query_companies.py --newest-by establishDate --limit 10
```

```
找到 2315 家公司，按 establishDate 排序（最新優先）

   3717  上市公司  聯嘉光電投資控股  (汽車工業)         establishDate = 2025-08-15
   7918  興櫃公司  創鉅先進材料     (半導體業)         establishDate = 2025-03-14
   3716  上市公司  中化控股        (生技醫療業)        establishDate = 2024-09-02
   7832  興櫃公司  智新生技        (生技醫療業)        establishDate = 2023-06-02
   7779  興櫃公司  鍇睿國際數位     (運動休閒)         establishDate = 2022-12-30
   7795  上市公司  長廣精機        (電子零組件業)      establishDate = 2022-10-21
   7915  興櫃公司  廌家科技        (通信網路業)        establishDate = 2022-09-28
   3715  上市公司  定穎投資控股     (電子零組件業)      establishDate = 2022-08-25
   7744  上櫃公司  崴寶精密        (電子零組件業)      establishDate = 2022-06-30
   7847  興櫃公司  豊漁           (觀光餐旅)          establishDate = 2022-06-21
```

The top two — `3717 聯嘉光電投資控股` (Aug 2025) and `3716 中化控股` (Sep 2024) —
are newly-formed **holding companies** created when established operating
companies restructured into holdco groups; the `establishDate` here is the
holdco's incorporation, not the underlying business. The youngest *operating*
company on this list is `7918 創鉅先進材料 (XALLOY)`, a March-2025 semiconductor-
materials startup that reached 興櫃 the same year (`ROTCDate = 2026-05-11`).
The 興櫃-heavy mix is the same pattern from the market×industry cross-tab —
the emerging board is where young companies enter public markets first.

### CLI filter summary

| Filter | Purpose |
|--------|---------|
| `--code` | Exact stock code |
| `--chairman` / `--chairman-contains` | Chairman exact / substring |
| `--president-contains` | President substring |
| `--name-starts-with` / `--name-contains` | Chinese name |
| `--english-name-contains` | English name (case-insensitive) |
| `--mainbusiness-contains` | Main-business text |
| `--market` | `上市公司` / `上櫃公司` / `興櫃公司` |
| `--industry` / `--industry-contains` | Industry |
| `--foreign` | Foreign-registered only (-KY/-BM/…) |
| `--top-by-capital N` | Sort by paid-in capital desc, keep N |
| `--newest-by FIELD` / `--oldest-by FIELD` | Sort by a date field (`OTCDate`, `ROTCDate`, `establishDate`, …) |
| `--full` | Show extra fields (chairman, capital, business, …) |
| `--count` | Print only the match count |

Filters AND together. `query_companies.py --help` lists everything.

---

## Ad-hoc queries (load the JSONL)

For shapes the CLI doesn't cover, ask the LLM to write a short filter — or copy
one of these.

```python
import json
rows = [json.loads(l) for l in open('company_profiles.jsonl', encoding='utf-8')]
```

### Q9.「誰兼任最多家公司董事長？」(interlocking directorates)

```python
from collections import defaultdict
by_chair = defaultdict(list)
for r in rows:
    ch = r.get('chairman', '')
    if ch and not ch.endswith('公司'):
        by_chair[ch].append(r)

for ch, cs in sorted(by_chair.items(), key=lambda x: -len(x[1]))[:8]:
    if len(cs) < 4: break
    print(f"{ch} → {len(cs)}: " +
          ", ".join(f"{r['code']} {r['companyAbbreviation']}" for r in cs))
```

```
張祐銘 → 8: 1316 上曜, 3313 斐成, 4303 信立, 4714 永捷, 5314 世紀*, 6418 詠昇, 6624 萬年清, 8047 星雲
焦佑衡 → 8: 2492 華新科, 3311 閎暉, 5469 瀚宇博, 6173 信昌電, 6191 精成科, 6284 佳邦, 8110 華東, 8183 精星
徐旭東 → 6: 1102 亞泥, 1402 遠東新, 1710 東聯, 2606 裕民, 2903 遠百, 4904 遠傳
羅智先 → 6: 1216 統一, 1232 大統益, 1789 神隆, 2511 太子, 2912 統一超, 9907 統一實
苗豐強 → 4: 1229 聯華, 1313 聯成, 2347 聯強, 3706 神達
```

These clusters expose business groups — Far Eastern (徐旭東), Uni-President
(羅智先), Walsin (焦佑衡), MiTAC (苗豐強)…

### Q10.「半導體業會計師事務所市占？」

```python
from collections import Counter
semi = [r for r in rows if r['industryCategory'] == '半導體業']
firms = Counter(r['accountingOffice'] for r in semi if r.get('accountingOffice'))
total = sum(firms.values())
for office, n in firms.most_common(5):
    print(f"  {n:>3}  ({n/total*100:5.1f}%)  {office}")
```

```
 81  (34.9%)  勤業眾信聯合會計師事務所 (Deloitte)
 64  (27.6%)  資誠聯合會計師事務所     (PwC)
 36  (15.5%)  安侯建業聯合會計師事務所 (KPMG)
 31  (13.4%)  安永聯合會計師事務所     (EY)
```

Big-4 audit ~91% of semiconductor companies.

### Q11.「設立日期最久遠 / 最新的公司」

> Now a one-liner with the CLI:
> `python3 query_companies.py --oldest-by establishDate --limit 5`
> (or `--newest-by establishDate`). The Python below is the equivalent if you
> want full control over formatting.

```python
import re
def roc(d):
    m = re.match(r'(\d{1,3})/(\d{2})/(\d{2})', d or '')
    return f"{int(m.group(1))+1911}-{m.group(2)}-{m.group(3)}" if m else None

dated = [(roc(r['establishDate']), r) for r in rows if r.get('establishDate')]
dated = [t for t in dated if t[0]]

print("OLDEST")
for d, r in sorted(dated, key=lambda t: t[0])[:5]:
    print(f"  {d}  {r['code']}  {r['companyName']}  ({r['industryCategory']})")
```

```
OLDEST
  1940-05-01  2035  唐榮鐵工廠           (鋼鐵工業)
  1946-05-01  1722  台灣肥料             (化學工業)
  1946-07-01  2617  台灣航業             (航運業)
  1947-02-01  5521  工信工程             (建材營造)
  1948-03-12  2832  台灣產物保險         (金融保險業)
```

### Q12.「市場別 × 產業別 cross-tab」

```python
from collections import Counter
cells = Counter((r['marketName'], r['industryCategory']) for r in rows)
for (m, i), n in cells.most_common(8):
    print(f"  {m}  ×  {i}  →  {n}")
```

```
  上櫃公司  ×  半導體業        → 109
  上櫃公司  ×  電子零組件業    → 108
  上市公司  ×  電子零組件業    → 103
  興櫃公司  ×  生技醫療業      →  95     ← biotechs dominate 興櫃
  上櫃公司  ×  生技醫療業      →  95
  上市公司  ×  半導體業        →  94
```

### Q13.「法人董事長 (corporate-entity chairs)」

```python
corp = [r for r in rows if r.get('chairman', '').endswith(('公司', '有限'))]
print(f"{len(corp)} companies have a corporate-entity chair")
for r in corp[:5]:
    print(f"  {r['code']}  {r['companyName']:22}  ← {r['chairman']}")
```

```
21 companies have a corporate-entity chair
  1104  環球水泥                  ← 博智投資股份有限公司
  1220  台榮產業                  ← 倍安利投資有限公司
  1339  昭輝實業                  ← 禾翰投資股份有限公司
  1612  宏泰電工                  ← 久疆投資股份有限公司
  1903  士林紙業                  ← 臺實貿易股份有限公司
```

---

## `jq` one-liners

If you prefer the command line over Python:

```bash
# Chairman exact match
jq -c 'select(.chairman == "洪裕鈞") | {code, name: .companyName, en: .companyEnglishName}' company_profiles.jsonl

# Chinese name prefix (jq's startswith for the 威 query)
jq -c 'select(.companyName | startswith("威")) | {code, companyName, marketName}' company_profiles.jsonl

# English-name regex
jq -c 'select(.companyEnglishName | test("Bio"; "i")) | {code, en: .companyEnglishName}' company_profiles.jsonl

# All -KY Cayman holding companies
jq -c 'select(.foreignCompanyRegisterPlace | startswith("KY")) | {code, companyAbbreviation}' company_profiles.jsonl

# Companies per industry
jq -r '.industryCategory' company_profiles.jsonl | sort | uniq -c | sort -rn | head -15

# Export code + English name + market as CSV
jq -r '[.code, .companyEnglishName, .marketName] | @csv' company_profiles.jsonl > company_english.csv
```

---

## Refreshing the dataset

The numbers above are a snapshot. For the latest companies (new listings each month):

```bash
python3 refresh_company_profiles.py            # add newly listed/OTC/emerging
python3 refresh_company_profiles.py --dry-run  # preview only
```

See `README.md` and `SKILL.md` for the full workflow.

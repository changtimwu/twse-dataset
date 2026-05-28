# `company_profiles.jsonl` — Query Recipes

Practical examples of what you can answer with one filter on `company_profiles.jsonl`.

The dataset is **JSONL** — one JSON object per company. Every example below is a
plain Python script (no extra dependencies) or a `jq` one-liner. Outputs shown
are real results from the bundled dataset.

## Dataset shape

```
total companies: 2,315
  上市公司 (TWSE listed):    1,078
  上櫃公司 (TPEx OTC):         889
  興櫃公司 (emerging board):   348
```

Loading helper used by every recipe below:

```python
import json
rows = [json.loads(l) for l in open('company_profiles.jsonl', encoding='utf-8')]
```

---

## 1. 人物搜尋 — find a person across the public-company universe

> **Q.** 找出所有董事長為洪裕鈞的公司

```python
for r in rows:
    if r.get('chairman') == '洪裕鈞':
        print(r['code'], r['companyName'], '/', r['companyEnglishName'])
```

```
6858  愛比科技股份有限公司 / IPEVO CORPORATION
      market=興櫃公司  industry=電腦及週邊設備業  est=2007-06-13
```

Works the same for any role field: `president`, `spokesperson`,
`subSpokesperson`, `accounting1` / `accounting2`, `investorLiaison`, `chairman`.
A `grep "<name>" company_profiles.jsonl` scans every field at once.

---

## 2. Interlocking directorates — who chairs the most public companies?

```python
from collections import defaultdict
by_chair = defaultdict(list)
for r in rows:
    ch = r.get('chairman', '')
    if ch and not ch.endswith('公司'):     # skip corporate-entity chairs
        by_chair[ch].append(r)

for ch, cs in sorted(by_chair.items(), key=lambda x: -len(x[1]))[:8]:
    if len(cs) < 4: break
    print(f"{ch} → {len(cs)}:",
          ", ".join(f"{r['code']} {r['companyAbbreviation']}" for r in cs))
```

```
張祐銘 → 8: 1316 上曜, 3313 斐成, 4303 信立, 4714 永捷, 5314 世紀*, 6418 詠昇, 6624 萬年清, 8047 星雲
焦佑衡 → 8: 2492 華新科, 3311 閎暉, 5469 瀚宇博, 6173 信昌電, 6191 精成科, 6284 佳邦, 8110 華東, 8183 精星
徐旭東 → 6: 1102 亞泥, 1402 遠東新, 1710 東聯, 2606 裕民, 2903 遠百, 4904 遠傳
羅智先 → 6: 1216 統一, 1232 大統益, 1789 神隆, 2511 太子, 2912 統一超, 9907 統一實
吳亦圭 → 5: 1304 台聚, 1305 華夏, 1308 亞聚, 1309 台達化, 8121 越峰
莊永順 → 5: 5484 慧友, 6109 亞元, 6161 捷波, 6569 醫揚, 6579 研揚
羅森洲 → 5: 6462 神盾, 6684 安格, 6695 芯鼎, 7898 乾瞻, 8054 安國
苗豐強 → 4: 1229 聯華, 1313 聯成, 2347 聯強, 3706 神達
```

The clusters expose **business groups** straight from `chairman` —
徐旭東 (Far Eastern), 羅智先 (Uni-President), 嚴陳莉蓮 (Yulon), 苗豐強 (MiTAC),
焦佑衡 (Walsin), …

---

## 3. Top N by paid-in capital within an industry

```python
import re
def to_yuan(s):
    m = re.search(r'([\d,]+)', s or '')
    return int(m.group(1).replace(',', '')) if m else 0

semi = [r for r in rows if r['industryCategory'] == '半導體業']
for r in sorted(semi, key=lambda r: -to_yuan(r['capitalAmount']))[:10]:
    abbr = r['companyEnglishAbbreviation'] or r['companyAbbreviation']
    print(f"{r['code']}  {r['marketName'][:5]}  {abbr:14}  "
          f"{to_yuan(r['capitalAmount'])/1e8:>8.1f} 億元")
```

```
2330  上市公司  TSMC              2593.2 億元
2303  上市公司  UMC               1257.7 億元
2344  上市公司  WEC                450.0 億元
3711  上市公司  ASEH               446.1 億元
6770  上市公司  PSMC               424.4 億元
2408  上市公司  NTC                345.0 億元
2337  上市公司  Macronix           198.1 億元
5347  上櫃公司  VIS                186.7 億元
2454  上市公司  MediaTek           160.4 億元
2449  上市公司  KYEC               122.3 億元
```

Swap `半導體業` for any value from `industryCategory` to get the same view
for that sector.

---

## 4. Auditor market share within an industry

```python
from collections import Counter
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
  4  ( 1.7%)  國富浩華聯合會計師事務所 (Crowe)
```

Big-4 audit ~91% of semiconductor companies. The same query works on any subset.

---

## 5. Oldest / newest companies

```python
import re
def roc(d):
    m = re.match(r'(\d{1,3})/(\d{2})/(\d{2})', d or '')
    return f"{int(m.group(1))+1911}-{m.group(2)}-{m.group(3)}" if m else None

dated = [(roc(r['establishDate']), r) for r in rows]
dated = [t for t in dated if t[0]]

print("OLDEST")
for d, r in sorted(dated, key=lambda t: t[0])[:5]:
    print(f"  {d}  {r['code']}  {r['companyName']}  ({r['industryCategory']})")

print("\nNEWEST (emerging board only)")
em = [(d, r) for d, r in dated if r['marketName'] == '興櫃公司']
for d, r in sorted(em, key=lambda t: t[0], reverse=True)[:5]:
    print(f"  {d}  {r['code']}  {r['companyName']}  ({r['industryCategory']})")
```

```
OLDEST
  1940-05-01  2035  唐榮鐵工廠           (鋼鐵工業)
  1946-05-01  1722  台灣肥料             (化學工業)
  1946-07-01  2617  台灣航業             (航運業)
  1947-02-01  5521  工信工程             (建材營造)
  1948-03-12  2832  台灣產物保險         (金融保險業)

NEWEST (emerging board only)
  2025-03-14  7918  創鉅先進材料         (半導體業)
  2023-06-02  7832  智新生技             (生技醫療業)
  2022-12-30  7779  鍇睿國際數位         (運動休閒)
  2022-09-28  7915  廌家科技             (通信網路業)
  2022-06-21  7847  豊漁                 (觀光餐旅)
```

---

## 6. Keyword search in `mainBusiness`

```python
import re
ai = [r for r in rows if re.search(r'AI|人工智慧', r.get('mainBusiness', ''))]
print(f"{len(ai)} companies mention AI / 人工智慧 in their main business")
for r in ai[:6]:
    abbr = r['companyEnglishAbbreviation'] or r['companyAbbreviation']
    print(f"  {r['code']}  {r['marketName'][:5]}  {abbr:14}  {r['industryCategory']}")
```

```
26 companies mention AI / 人工智慧 in their main business
  1597  上市公司  cpc            電機機械
  2256  興櫃公司  oToBrite       其他電子業
  2359  上市公司  SOLOMON        其他電子業
  2458  上市公司  ELAN           半導體業
  3147  上櫃公司  JETWELL        資訊服務業
  3570  上櫃公司  OITC           資訊服務業
```

Try other keywords: `綠能|碳|再生能源`, `電動車|EV`, `5G`, `生技|藥`, `區塊鏈|crypto`.

---

## 7. Foreign-registered companies (-KY / -BM / -TH)

```python
from collections import Counter
fc = [r for r in rows
      if r.get('foreignCompanyRegisterPlace', '-') not in ('-', '')]
places = Counter(r['foreignCompanyRegisterPlace'] for r in fc)
print(f"foreign-registered: {len(fc)}; top places:")
for p, n in places.most_common(5):
    print(f"  {n:>4}  {p}")
```

```
foreign-registered: 127; top places:
   125  KY 開曼群島
     1  BM 百慕達群島
     1  TH 泰國
```

These are the "-KY" companies whose names you see suffixed with `-KY` in
trading apps — Cayman holding companies whose operations are mostly in
Taiwan/Asia.

---

## 8. Market × industry cross-tab

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
  興櫃公司  ×  生技醫療業      →  95
  上櫃公司  ×  生技醫療業      →  95
  上市公司  ×  半導體業        →  94
  上市公司  ×  光電業          →  68
  上市公司  ×  電腦及週邊設備業 → 64
```

Note 生技醫療業 dominates the **emerging board** — that's where many biotechs
sit before/instead of a full listing.

---

## 9. 法人董事長 — companies chaired by a corporate entity

```python
corp = [r for r in rows
        if r.get('chairman', '').endswith(('公司', '有限'))]
print(f"{len(corp)} companies have a corporate-entity chair")
for r in corp[:6]:
    print(f"  {r['code']}  {r['companyName']:22}  ← {r['chairman']}")
```

```
21 companies have a corporate-entity chair
  1104  環球水泥                  ← 博智投資股份有限公司
  1220  台榮產業                  ← 倍安利投資有限公司
  1339  昭輝實業                  ← 禾翰投資股份有限公司
  1612  宏泰電工                  ← 久疆投資股份有限公司
  1903  士林紙業                  ← 臺實貿易股份有限公司
  2615  萬海航運                  ← 久福花園股份有限公司
```

Useful for tracing holding-company structures.

---

## `jq` one-liners

If you prefer the command line:

```bash
# A. The trigger query — chairman == 洪裕鈞
jq -c 'select(.chairman == "洪裕鈞") | {code, name: .companyName, en: .companyEnglishName}' company_profiles.jsonl

# B. All semiconductors on the emerging board
jq -c 'select(.industryCategory == "半導體業" and .marketName == "興櫃公司")
        | {code, name: .companyAbbreviation, est: .establishDate}' company_profiles.jsonl

# C. Companies whose English name contains "Bio"
jq -c 'select(.companyEnglishName | test("Bio"; "i"))
        | {code, en: .companyEnglishName, market: .marketName}' company_profiles.jsonl

# D. All -KY (Cayman) holding companies
jq -c 'select(.foreignCompanyRegisterPlace | startswith("KY"))
        | {code, name: .companyAbbreviation}' company_profiles.jsonl

# E. Count companies per industry
jq -r '.industryCategory' company_profiles.jsonl | sort | uniq -c | sort -rn | head -15

# F. CSV of code + English name + market for spreadsheet import
jq -r '[.code, .companyEnglishName, .marketName] | @csv' company_profiles.jsonl > company_english.csv
```

---

## Refreshing the dataset

The numbers above are a snapshot. To get the latest companies (newly listed
each month):

```bash
python3 refresh_company_profiles.py            # add newly listed/OTC/emerging
python3 refresh_company_profiles.py --dry-run  # preview only
```

See `README.md` and `SKILL.md` for the full workflow.

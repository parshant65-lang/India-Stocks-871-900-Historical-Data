# India-Stocks-871-900-Historical-Data

Institutional Historical 1-Minute Market Data Archive for **India Equities (Constituents 871 to 900)** with automated daily cloud capture via GitHub Actions.

---

## 🏛️ Directory Hierarchy

```text
India-Stocks-871-900-Historical-Data/
├── .github/workflows/daily_ingest.yml
├── fetch_batch.py
├── README.md
├── <SYMBOL>/
│   └── 1m/
│       ├── README.md
│       └── <YYYY>/
│           └── <MM>/
│               ├── <SYMBOL>_1m_<YYYY-MM-DD>.csv
```

---

## ⏰ 4-Tier Automated Schedule (Mon–Fri)

| Trigger | Time (IST) | Cron (UTC) | Role |
|:---|:---:|:---:|:---|
| **Primary Trigger** | **15:45 IST** | `15 10 * * 1-5` | 15 mins post-market close |
| **Backup Trigger 1** | **16:45 IST** | `15 11 * * 1-5` | 1 hour safety net |
| **Backup Trigger 2** | **17:45 IST** | `15 12 * * 1-5` | 2 hours safety net |
| **Backup Trigger 3** | **18:45 IST** | `15 13 * * 1-5` | 3 hours safety net |

---

## 📦 Constituents (871 to 900)

| # | Symbol | Company Name | Yahoo Ticker |
|---|---|---|---|
| 871 | `CHEMFAB` | Chemfab Alkalis Limited | `CHEMFAB.NS` |
| 872 | `CHEMPLASTS` | Chemplast Sanmar Limited | `CHEMPLASTS.NS` |
| 873 | `CHEVIOT` | Cheviot Company Limited | `CHEVIOT.NS` |
| 874 | `CIFL` | Capital India Finance Limited | `CIFL.NS` |
| 875 | `CINELINE` | Cineline India Limited | `CINELINE.NS` |
| 876 | `CINEVISTA` | Cinevista Limited | `CINEVISTA.NS` |
| 877 | `CLEDUCATE` | CL Educate Limited | `CLEDUCATE.NS` |
| 878 | `CLSEL` | Chaman Lal Setia Exports Limited | `CLSEL.NS` |
| 879 | `CMLL` | Caliber Mining and Logistics Limited | `CMLL.NS` |
| 880 | `CMRGREEN` | CMR Green Technologies Limited | `CMRGREEN.NS` |
| 881 | `CMSINFO` | CMS Info Systems Limited | `CMSINFO.NS` |
| 882 | `CNL` | Creative Newtech Limited | `CNL.NS` |
| 883 | `COASTCORP` | Coastal Corporation Limited | `COASTCORP.NS` |
| 884 | `COCKERILL` | John Cockerill India Limited | `COCKERILL.NS` |
| 885 | `COFFEEDAY` | Coffee Day Enterprises Limited | `COFFEEDAY.NS` |
| 886 | `COMFINTE` | Comfort Intech Limited | `COMFINTE.NS` |
| 887 | `COMPEAU` | Competent Automobiles Company Limited | `COMPEAU.NS` |
| 888 | `COMPINFO` | Compuage Infocom Limited | `COMPINFO.NS` |
| 889 | `COMPUSOFT` | Compucom Software Limited | `COMPUSOFT.NS` |
| 890 | `COMSYN` | Commercial Syn Bags Limited | `COMSYN.NS` |
| 891 | `CONFIPET` | Confidence Petroleum India Limited | `CONFIPET.NS` |
| 892 | `CONSOFINVT` | Consolidated Finvest & Holdings Limited | `CONSOFINVT.NS` |
| 893 | `CONTROLPR` | Control Print Limited | `CONTROLPR.NS` |
| 894 | `CORALFINAC` | Coral India Finance & Housing Limited | `CORALFINAC.NS` |
| 895 | `CORDELIA` | Waterways Leisure Tourism Limited | `CORDELIA.NS` |
| 896 | `CORDSCABLE` | Cords Cable Industries Limited | `CORDSCABLE.NS` |
| 897 | `CORONA` | CORONA Remedies Limited | `CORONA.NS` |
| 898 | `COSMOFIRST` | COSMO FIRST LIMITED | `COSMOFIRST.NS` |
| 899 | `COUNCODOS` | Country Condo's Limited | `COUNCODOS.NS` |
| 900 | `CPCAP` | CP Capital Limited | `CPCAP.NS` |


---

## ⚡ 1-Line Pandas Stream Loader

```python
import pandas as pd

# Example: Stream CHEMFAB 1m data
url = "https://raw.githubusercontent.com/parshant65-lang/India-Stocks-871-900-Historical-Data/main/CHEMFAB/1m/2026/10/CHEMFAB_1m_2026-10-12.csv"
df = pd.read_csv(url)
print(df.head())
```
